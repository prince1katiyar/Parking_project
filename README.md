 <!-- # 🚗 AI-Powered Smart Parking System

Welcome to the AI-Powered Smart Parking System! This project revolutionizes how you find and book parking spots. Our intelligent assistant helps you check slot availability in real-time and provides a seamless booking experience. Say goodbye to parking hassles!

## 🌟 Core Features

-   **Smart Slot Checking:** Instantly find available parking spots near your destination.
-   **Seamless Booking:** Reserve your preferred parking slot directly through the assistant.
-   **Conversational AI:** Interact naturally with our AI assistant for all your parking needs.
-   **Personalized Experience:** The assistant can remember your preferences (like vehicle type) for future interactions within the same session.
-   **Real-time Updates (Conceptual):** Designed with the potential to integrate with real-time parking data.

## 🛠️ Tech Stack

-   **Backend API:** FastAPI
-   **AI Orchestration:** LangChain, LangChain-OpenAI
-   **Language Model:** OpenAI (GPT series)
-   **Vector Database:** Milvus (for semantic search, conversation memory)
-   **Database (Relational):** SQLite (managed by SQLAlchemy)
-   **User Interface:** Streamlit
-   **Server:** Uvicorn (for FastAPI)
-   **Environment Management:** Python-dotenv
-   **Containerization (for Milvus):** Docker

## 🚀 Getting Started

### Prerequisites

1.  **Python 3.8+**: Ensure Python is installed on your system.
2.  **Docker**: Required for easily running a Milvus instance. [Install Docker](https://docs.docker.com/get-docker/)
3.  **OpenAI API Key**: You'll need an API key from [OpenAI](https://platform.openai.com/).

### Setup Instructions

1.  **Clone the Repository (if applicable):**
    ```bash
    # git clone <your-repository-url>
    # cd ai-powered-smart-parking-system
    ```
    (If starting from scratch, create the project directory structure.)

2.  **Set Up Milvus with Docker:**
    This is the recommended way to run Milvus for development.
    ```bash
    docker run -d --name milvus_standalone \
      -p 19530:19530 \
      -p 9091:9091 \
      milvusdb/milvus:v2.3.10-standalone
    ```
    *(You can replace `v2.3.10-standalone` with a more recent stable version from [Milvus Docker Hub](https://hub.docker.com/r/milvusdb/milvus/tags). Ensure Milvus is running and accessible on `localhost:19530`.)*

3.  **Create Virtual Environment & Install Dependencies:**
    Navigate to your project root directory.
    ```bash
    python -m venv venv
    source venv/bin/activate  # For macOS/Linux
    # venv\Scripts\activate    # For Windows
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root directory (`ai-powered-smart-parking-system/.env`) with the following content:
    ```env
    OPENAI_API_KEY="your_openai_api_key_here"
    MILVUS_HOST="localhost"
    MILVUS_PORT="19530"
    MILVUS_COLLECTION_NAME="parking_conversations"
    # API_BASE_URL="http://localhost:8000" # Used by Streamlit to find FastAPI
    ```
    Replace `"your_openai_api_key_here"` with your actual OpenAI API key. The `MILVUS_COLLECTION_NAME` should match what's used in `milvus_utils/milvus_connector.py`.

5.  **Initialize Database & Milvus Collection:**
    *   **SQLite & Initial Data:** The FastAPI app handles SQLite table creation on startup. If needed, you can also run the initialization script manually:
        ```bash
        # Ensure you are in the project root
        python -m app.initial_data
        ```
    *   **Milvus Collection:** The specified Milvus collection is typically created automatically on application startup (e.g., when `milvus_connector.py` is used). You can also verify or create it:
        ```bash
        # Ensure you are in the project root
        python -m milvus_utils.milvus_connector
        ```

## ⚙️ Running the System

To bring the AI-Powered Smart Parking System to life, you need to run two main components: the FastAPI backend and the Streamlit UI.

1.  **Start the FastAPI Backend:**
    *   Open a terminal.
    *   Activate your virtual environment: `source venv/bin/activate`
    *   Navigate to the project root directory.
    *   Run Uvicorn:
        ```bash
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ```
    *   Keep this terminal running. The backend is now live at `http://localhost:8000`. API docs are usually at `http://localhost:8000/docs`.

2.  **Start the Streamlit User Interface:**
    *   Open a **new** terminal.
    *   Activate your virtual environment: `source venv/bin/activate`
    *   Navigate to the project root directory.
    *   Run Streamlit:
        ```bash
        streamlit run ui/app.py
        ```
    *   Keep this terminal running. The UI will typically open in your browser at `http://localhost:8501`.

## 💬 Using the System

Once both backend and UI are running:

1.  Open the Streamlit UI in your web browser (e.g., `http://localhost:8501`).
2.  Begin your conversation with the AI Parking Assistant!

    **Example Interactions:**
    *   🗣️ **User:** "I need parking for my SUV near City Center for 3 hours tomorrow."
    *   🤖 **Assistant:** (Provides available slots)
    *   🗣️ **User:** "Book slot ID 2 for me."
    *   🤖 **Assistant:** (Confirms booking or asks for more details)

    **Tips:**
    *   **Missing Information:** If you simply say "I need parking," the agent will guide you by asking for necessary details like location, vehicle type, duration, etc.
    *   **Conversational Memory:** The assistant can remember details from your current session (e.g., if you mentioned your vehicle type earlier).

## 📦 Key Dependencies

The project relies on several key Python libraries (full list in `requirements.txt`):

-   `fastapi` & `uvicorn`: For building and serving the backend API.
-   `sqlalchemy`: ORM for SQLite database interactions.
-   `pydantic`: Data validation and settings.
-   `python-dotenv`: Managing environment variables from `.env` files.
-   `openai`: Official Python client for OpenAI API.
-   `langchain`, `langchain-openai`: For the AI agent, memory, and LLM integration.
-   `pymilvus`: Python client for interacting with Milvus.
-   `streamlit`: For creating the interactive web UI.
-   `tiktoken`: For token counting, often used with OpenAI models.

## 🤔 Troubleshooting

-   **OpenAI API Errors:** Double-check your `OPENAI_API_KEY` in `.env`. Ensure your OpenAI account has active billing and sufficient credits.
-   **Milvus Connection Issues:** Verify the Milvus Docker container is running and accessible on `localhost:19530`. Check Docker logs for Milvus (`docker logs milvus_standalone`).
-   **`ModuleNotFoundError`**: Make sure your virtual environment is activated and you've run `pip install -r requirements.txt`.
-   **Streamlit UI Can't Connect to Backend:**
    *   Confirm the FastAPI backend (Step 1 in "Running the System") is running without errors.
    *   Ensure the `API_BASE_URL` (if explicitly used by Streamlit to call FastAPI) in `.env` or your Streamlit code points to `http://localhost:8000`.
    *   Check for firewall issues that might block local connections.




    ## 🏗️ System Architecture

    Below is a diagram illustrating the architecture of the AI-Powered Smart Parking System:

    ![System Architecture Diagram](docs/images/architecture_diagram.png)


    ## Check  Screenshot in docs Folder 


## 🤝 Contributing

Contributions are highly appreciated!
1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/YourAmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some YourAmazingFeature'`).
4.  Push to the Branch (`git push origin feature/YourAmazingFeature`).
5.  Open a Pull Request.

## 📜 License

Distributed under the MIT License. See `LICENSE` file for more information. (Create a `LICENSE` file if you haven't already).
 -->


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Smart Parking System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f7fa;
            color: #333;
            line-height: 1.6;
            margin: 0;
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        code {
            background-color: #ecf0f1;
            padding: 2px 4px;
            border-radius: 4px;
            font-size: 0.95em;
        }
        pre {
            background-color: #ecf0f1;
            padding: 1em;
            overflow-x: auto;
            border-radius: 8px;
        }
        a {
            color: #2980b9;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .section {
            margin-bottom: 2em;
        }
        ul {
            padding-left: 1.2em;
        }
    </style>
</head>
<body>

    <h1>🚗 AI-Powered Smart Parking System</h1>
    <p>Welcome to the AI-Powered Smart Parking System! This project revolutionizes how you find and book parking spots. Our intelligent assistant helps you check slot availability in real-time and provides a seamless booking experience. Say goodbye to parking hassles!</p>

    <div class="section">
        <h2>🌟 Core Features</h2>
        <ul>
            <li><strong>Smart Slot Checking:</strong> Instantly find available parking spots near your destination.</li>
            <li><strong>Seamless Booking:</strong> Reserve your preferred parking slot directly through the assistant.</li>
            <li><strong>Conversational AI:</strong> Interact naturally with our AI assistant for all your parking needs.</li>
            <li><strong>Personalized Experience:</strong> The assistant can remember your preferences (like vehicle type) for future interactions within the same session.</li>
            <li><strong>Real-time Updates (Conceptual):</strong> Designed with the potential to integrate with real-time parking data.</li>
        </ul>
    </div>

    <div class="section">
        <h2>🛠️ Tech Stack</h2>
        <ul>
            <li><strong>Backend API:</strong> FastAPI</li>
            <li><strong>AI Orchestration:</strong> LangChain, LangChain-OpenAI</li>
            <li><strong>Language Model:</strong> OpenAI (GPT series)</li>
            <li><strong>Vector Database:</strong> Milvus</li>
            <li><strong>Relational Database:</strong> SQLite (via SQLAlchemy)</li>
            <li><strong>User Interface:</strong> Streamlit</li>
            <li><strong>Server:</strong> Uvicorn</li>
            <li><strong>Env Management:</strong> Python-dotenv</li>
            <li><strong>Docker:</strong> Used to containerize Milvus</li>
        </ul>
    </div>

    <div class="section">
        <h2>🚀 Getting Started</h2>
        <h3>📦 Prerequisites</h3>
        <ul>
            <li><strong>Python 3.8+</strong></li>
            <li><strong>Docker:</strong> <a href="https://docs.docker.com/get-docker/" target="_blank">Install Docker</a></li>
            <li><strong>OpenAI API Key:</strong> <a href="https://platform.openai.com/" target="_blank">Get API Key</a></li>
        </ul>

        <h3>🔧 Setup Instructions</h3>
        <ol>
            <li><strong>Clone the Repository:</strong>
                <pre><code># git clone &lt;your-repository-url&gt;
# cd ai-powered-smart-parking-system</code></pre>
            </li>

            <li><strong>Run Milvus via Docker:</strong>
                <pre><code>docker run -d --name milvus_standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  milvusdb/milvus:v2.3.10-standalone</code></pre>
            </li>

            <li><strong>Create Virtual Environment & Install Dependencies:</strong>
                <pre><code>python -m venv venv
source venv/bin/activate  # For macOS/Linux
# venv\Scripts\activate    # For Windows
pip install -r requirements.txt</code></pre>
            </li>

            <li><strong>Create a <code>.env</code> file:</strong>
                <pre><code>OPENAI_API_KEY="your_openai_api_key_here"
MILVUS_HOST="localhost"
MILVUS_PORT="19530"
MILVUS_COLLECTION_NAME="parking_conversations"</code></pre>
            </li>

            <li><strong>Initialize SQLite and Milvus Collections:</strong>
                <pre><code>python -m app.initial_data
python -m milvus_utils.milvus_connector</code></pre>
            </li>
        </ol>
    </div>

    <div class="section">
        <h2>⚙️ Running the System</h2>
        <ol>
            <li><strong>Start FastAPI Backend:</strong>
                <pre><code>uvicorn app.main:app --reload --host 0.0.0.0 --port 8000</code></pre>
            </li>
            <li><strong>Start Streamlit UI:</strong>
                <pre><code>streamlit run ui/app.py</code></pre>
            </li>
        </ol>
    </div>

    <div class="section">
        <h2>💬 Example Interaction</h2>
        <ul>
            <li>🗣️ <strong>User:</strong> "I need parking for my SUV near City Center for 3 hours tomorrow."</li>
            <li>🤖 <strong>Assistant:</strong> (Provides available slots)</li>
            <li>🗣️ <strong>User:</strong> "Book slot ID 2 for me."</li>
            <li>🤖 <strong>Assistant:</strong> (Confirms booking or asks for more details)</li>
        </ul>
    </div>

    <div class="section">
        <h2>📦 Key Dependencies</h2>
        <ul>
            <li>FastAPI & Uvicorn</li>
            <li>SQLAlchemy & Pydantic</li>
            <li>LangChain, LangChain-OpenAI</li>
            <li>pymilvus</li>
            <li>OpenAI SDK</li>
            <li>Streamlit</li>
            <li>tiktoken</li>
        </ul>
    </div>

    <div class="section">
        <h2>🤔 Troubleshooting</h2>
        <ul>
            <li><strong>API Errors:</strong> Check your API key and billing info.</li>
            <li><strong>Milvus Errors:</strong> Make sure Docker container is up using <code>docker logs milvus_standalone</code>.</li>
            <li><strong>Module Errors:</strong> Activate your virtual environment and install dependencies.</li>
            <li><strong>Connection Errors:</strong> Ensure the API URL is correct and backend is running.</li>
        </ul>
    </div>

    <div class="section">
        <h2>🏗️ System Architecture</h2>
        <p>Below is a diagram illustrating the architecture of the AI-Powered Smart Parking System:</p>
        <img src="docs/images/architecture_diagram.png" alt="System Architecture Diagram" style="max-width:100%; border:1px solid #ccc; border-radius: 8px;" />
    </div>

    <div class="section">
        <h2>📸 Screenshot</h2>
        <p>Check the <strong>docs</strong> folder for UI screenshots and visual guides.</p>
    </div>

    <div class="section">
        <h2>🤝 Contributing</h2>
        <ol>
            <li>Fork the repository</li>
            <li>Create your branch: <code>git checkout -b feature/YourAmazingFeature</code></li>
            <li>Commit your changes: <code>git commit -m 'Add YourAmazingFeature'</code></li>
            <li>Push your branch: <code>git push origin feature/YourAmazingFeature</code></li>
            <li>Open a Pull Request</li>
        </ol>
    </div>

    <div class="section">
        <h2>📜 License</h2>
        <p>This project is licensed under the <strong>MIT License</strong>. See the <code>LICENSE</code> file for more information.</p>
    </div>

</body>
</html>








