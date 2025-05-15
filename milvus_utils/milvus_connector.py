
import os
from pymilvus import connections, utility, Collection, CollectionSchema, FieldSchema, DataType
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


MILVUS_DATA_PATH = os.getenv("MILVUS_DATA_PATH", "./data/milvus_data") 
COLLECTION_NAME = "parking_conversations"
DIMENSION = 1536 
INDEX_FIELD_NAME = "embedding"
ID_FIELD_NAME = "id"
SESSION_ID_FIELD_NAME = "session_id"
TEXT_FIELD_NAME = "text"
ROLE_FIELD_NAME = "role" 
METRIC_TYPE = "L2" 

class MilvusService:
    def __init__(self):
        self.embeddings_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        self._connect()
        self._create_collection_if_not_exists()

    def _connect(self):
        try:
            print(f"Attempting to connect to Milvus Lite, data will be stored in: {MILVUS_DATA_PATH}")
            os.makedirs(MILVUS_DATA_PATH, exist_ok=True) 
            connections.connect(alias="default", uri=f"{MILVUS_DATA_PATH}/milvus_parking.db") 
            print("Successfully connected to Milvus Lite.")
        except Exception as e:
            print(f"Failed to connect to Milvus: {e}")
            raise

    def _create_collection_if_not_exists(self):
        if not utility.has_collection(COLLECTION_NAME, using="default"):
            print(f"Collection '{COLLECTION_NAME}' does not exist. Creating...")
            fields = [
                FieldSchema(name=ID_FIELD_NAME, dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name=SESSION_ID_FIELD_NAME, dtype=DataType.VARCHAR, max_length=255, description="User session ID"),
                FieldSchema(name=TEXT_FIELD_NAME, dtype=DataType.VARCHAR, max_length=65535, description="Conversation text"), 
                FieldSchema(name=ROLE_FIELD_NAME, dtype=DataType.VARCHAR, max_length=10, description="Role (user/ai)"),
                FieldSchema(name=INDEX_FIELD_NAME, dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
            ]
            schema = CollectionSchema(fields, description="Parking conversation history")
            self.collection = Collection(COLLECTION_NAME, schema=schema, using="default")
            self._create_index()
            print(f"Collection '{COLLECTION_NAME}' created and indexed.")
        else:
            print(f"Collection '{COLLECTION_NAME}' already exists.")
            self.collection = Collection(COLLECTION_NAME, using="default")

            if not self.collection.has_index():
                print(f"Index not found for collection '{COLLECTION_NAME}'. Creating index...")
                self._create_index()
            else:

                self.collection.load()


    def _create_index(self):
        index_params = {
            "metric_type": METRIC_TYPE,
            "index_type": "IVF_FLAT", 
            "params": {"nlist": 128}, 
        }
        self.collection.create_index(INDEX_FIELD_NAME, index_params)
        self.collection.load() 
        print(f"Index created for field '{INDEX_FIELD_NAME}' and collection loaded.")


    def add_conversation_history(self, session_id: str, text: str, role: str):
        if not text.strip(): 
            return None
        embedding = self.embeddings_model.embed_query(text)
        data = [
            [session_id],
            [text],
            [role],
            [embedding]
        ]
        try:

            insert_result = self.collection.insert(data)
            self.collection.flush() 

            return insert_result
        except Exception as e:
            print(f"Error inserting data into Milvus: {e}")
            return None

    def get_relevant_history(self, session_id: str, query_text: str, k: int = 5):
        if not query_text.strip():
            return []
        query_embedding = self.embeddings_model.embed_query(query_text)
        search_params = {
            "metric_type": METRIC_TYPE,
            "params": {"nprobe": 10}, 
        }

        expr = f"{SESSION_ID_FIELD_NAME} == '{session_id}'"
        
        try:

            results = self.collection.search(
                data=[query_embedding],
                anns_field=INDEX_FIELD_NAME,
                param=search_params,
                limit=k,
                expr=expr, 
                output_fields=[TEXT_FIELD_NAME, ROLE_FIELD_NAME, SESSION_ID_FIELD_NAME] 
            )

            history = []
            if results:
                for hit in results[0]: 

                    if hit.entity.get(SESSION_ID_FIELD_NAME) == session_id:
                        history.append({
                            "role": hit.entity.get(ROLE_FIELD_NAME),
                            "content": hit.entity.get(TEXT_FIELD_NAME)
                        })

            return history
        except Exception as e:
            print(f"Error searching Milvus: {e}")
            return []

if __name__ == "__main__":
    milvus_service = MilvusService()
    session_id = "test_session_123"
    milvus_service.add_conversation_history(session_id, "Hello, I need parking.", "user")
    milvus_service.add_conversation_history(session_id, "Sure, for what vehicle type and location?", "ai")
    milvus_service.add_conversation_history(session_id, "A car, near Downtown Mall.", "user")

    history = milvus_service.get_relevant_history(session_id, "What about parking duration?")
    print("\nRetrieved history for 'What about parking duration?':")
    for item in history:
        print(f"- {item['role']}: {item['content']}")

    history_other_session = milvus_service.get_relevant_history("other_session", "My car needs parking.")
    print(f"\nHistory for other_session: {history_other_session}")