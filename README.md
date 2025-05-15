# Parking Agent System

Project documentation goes here.

## Setup Instructions

1.  **Prerequisites:**
    *   Python 3.8+
    *   Docker (for running Milvus easily)
    *   An OpenAI API Key

2.  **Clone the Repository (if applicable) or Create Project Structure:**
    ```bash
    # git clone <repository_url>
    # cd parking_agent_system
    ```
    If starting from scratch, create the directory structure as shown above.

3.  **Set up Milvus:**
    The easiest way is using Docker:
    ```bash
    docker run -d --name milvus_standalone \
      -p 19530:19530 \
      -p 9091:9091 \
      milvusdb/milvus:v2.3.10-standalone 
      # Use a recent stable version, e.g. v2.3.10 or check Milvus docs for latest
    ```
    Ensure Milvus is running and accessible on `localhost:19530`.

4.  **Create Virtual Environment and Install Dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate    # Windows
    pip install -r requirements.txt
    ```

5.  **Set Up Environment Variables:**
    Create a `.env` file in the root `parking_agent_system/` directory with the following content:
    ```env
    OPENAI_API_KEY="your_openai_api_key_here"
    MILVUS_HOST="localhost"
    MILVUS_PORT="19530"
    MILVUS_COLLECTION_NAME="parking_conversations" 
    # Ensure this matches the one in milvus_connector.py if you change it
    ```
    Replace `"your_openai_api_key_here"` with your actual OpenAI API key.

6.  **Initialize Database and Milvus Collection:**
    *   **SQLite & Initial Data:** The FastAPI application's startup event and the `app/initial_data.py` script handle SQLite table creation and initial data population. Run this script once manually if needed, or rely on the FastAPI startup:
        ```bash
        python -m app.initial_data 
        ```
        (Ensure your `PYTHONPATH` is set or run from the root where `app` is a module, e.g., `PYTHONPATH=. python app/initial_data.py` if you have issues.)
        The FastAPI `startup_event` in `app/main.py` will also attempt to do this.

    *   **Milvus Collection:** The Milvus collection (`parking_conversations`) is created automatically when `milvus_utils/milvus_connector.py` is first imported or when its `create_milvus_collection_if_not_exists()` function is called (e.g., on FastAPI startup). You can also test/ensure its creation by running:
        ```bash
        python -m milvus_utils.milvus_connector
        ```

## Running the System

You need to run two components: the FastAPI backend and the Streamlit UI.

1.  **Run the FastAPI Backend:**
    Open a terminal, navigate to the project root (`parking_agent_system/`), activate the virtual environment, and run:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The backend will be accessible at `http://localhost:8000`. You can see API docs at `http://localhost:8000/docs`.

2.  **Run the Streamlit UI:**
    Open another terminal, navigate to the project root, activate the virtual environment, and run:
    ```bash
    streamlit run ui/app.py
    ```
    The UI will typically open automatically in your browser at `http://localhost:8501`.

## Using the System

1.  Open the Streamlit UI in your browser.
2.  Start chatting with the AI Parking Assistant.
    *   **Example Search Query:** "I need parking for my car near Downtown Garage A for 2 hours."
    *   **Example Follow-up (after search results):** "Book slot ID 1."
    *   **Missing Information:** If you say "I need parking", the agent will ask for location, vehicle type, etc.
    *   **Memory:** If you previously mentioned your vehicle type (e.g., "I have a two-wheeler"), the agent might remember it for subsequent queries in the same session.

## Dependencies

Key dependencies are listed in `requirements.txt`. This includes:

*   `fastapi`: For the backend API.
*   `uvicorn`: ASGI server for FastAPI.
*   `sqlalchemy`: For SQLite ORM.
*   `pydantic`: For data validation and settings management.
*   `python-dotenv`: For managing environment variables.
*   `openai`: OpenAI Python client library.
*   `langchain`, `langchain-openai`: For AI agent orchestration and LLM integration.
*   `pymilvus`: Python client for Milvus.
*   `streamlit`: For the user interface.
*   `tiktoken`: For token counting with OpenAI models.

(See `requirements.txt` for specific versions used if this project was versioned.)

## Further Development / Considerations

*   **Time-based Slot Availability:** The current booking system is simplistic (marks slot unavailable indefinitely). A real system needs to manage availability based on booking start/end times.
*   **User Authentication:** Implement proper user accounts instead of just session IDs.
*   **Date/Time Handling:** Currently assumes "today/now". Add full date/time parsing and handling for future bookings.
*   **Advanced Milvus Search:** Use partition keys for `session_id` if scaling to many users. More sophisticated querying.
*   **Error Handling & Resilience:** More robust error handling across all components.
*   **LLM Prompt Engineering:** Continuously refine prompts for better intent detection, parameter extraction, and conversational flow.
*   **Agent State Management:** The current agent's tool metadata (like `last_search_results`) is a simplification. For multi-user/session environments, this state needs to be managed per session (e.g., in a Redis cache or passed around).
*   **Testing:** Add unit and integration tests.
*   **Deployment:** Containerize with Docker Compose for easier deployment.