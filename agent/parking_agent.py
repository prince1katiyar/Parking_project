
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from .tools import list_of_tools
from .prompts import SYSTEM_PROMPT_TEMPLATE
from milvus_utils.milvus_connector import MilvusService
import uuid

load_dotenv()

class ParkingAgent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.llm = ChatOpenAI(
            temperature=0.1, 
            model_name="gpt-3.5-turbo-0125", 

            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.tools = list_of_tools
        self.milvus_service = MilvusService()

        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT_TEMPLATE.format(session_id=self.session_id)),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            HumanMessagePromptTemplate.from_template("{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        self.agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors="Check your output and make sure it conforms to the Tool input JSON schema.", 
            max_iterations=10 
        )
        print(f"ParkingAgent initialized for session: {self.session_id} with model {self.llm.model_name}")

    def _load_chat_history_from_milvus(self, query_for_context: str):

        raw_history = self.milvus_service.get_relevant_history(self.session_id, query_for_context, k=10) 
        chat_history_messages = []

        for item in reversed(raw_history): 
            if item['role'] == 'user':
                chat_history_messages.append(HumanMessage(content=item['content']))
            elif item['role'] == 'ai':
                chat_history_messages.append(AIMessage(content=item['content']))
 
        return chat_history_messages[-10:] 

    def invoke_agent(self, user_input: str):
        chat_history_for_prompt = self._load_chat_history_from_milvus(user_input)
        
        print(f"DEBUG AGENT: Session {self.session_id} - User Input: {user_input}")


        try:
            response = self.agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history_for_prompt,
            })
            agent_response_text = response.get("output", "Sorry, I encountered an issue processing your request.")

   
            agent_response_text = agent_response_text.replace("**", "")


        except Exception as e:
            print(f"ERROR AGENT: invoke_agent failed for session {self.session_id}: {e}")

            agent_response_text = "I'm sorry, I ran into an unexpected problem. Could you please try rephrasing or try again in a moment?"

        self.milvus_service.add_conversation_history(self.session_id, user_input, "user")
        self.milvus_service.add_conversation_history(self.session_id, agent_response_text, "ai")
        
        return agent_response_text