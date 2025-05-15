
## 🚀 Getting Started

### Prerequisites

-   Python 3.9 or higher
-   Git
-   An OpenAI API Key
-   (For macOS users needing `watchdog` for Streamlit hot-reloading):
    ```bash
    xcode-select --install
    ```

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd parking_agent_system
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On macOS/Linux
    source venv/bin/activate
    # On Windows
    # venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root of the project (`parking_agent_system/.env`).

    > **⚠️ Important:** The `.env` file is ignored by Git (as it should be) and contains sensitive information like your API key. **Never commit it to your repository.**

    Add your configurations to it. Here's an example structure:
    ```env
    # OpenAI Configuration
    OPENAI_API_KEY="sk-YourOpenAIapiKeyHere"

    # Milvus Configuration
    # For Milvus Lite, these might not be strictly necessary if defaults are used,
    # but good to have for explicitness or if using a standalone Milvus server.
    MILVUS_HOST="localhost"
    MILVUS_PORT="19530"
    # Path for Milvus Lite data storage. Ensure this directory exists or can be created.
    MILVUS_DATA_PATH="./data/milvus_data"

    # Optional: If using a separate FastAPI backend
    # API_BASE_URL="http://localhost:8000"
    ```

5.  **Milvus Setup:**
    -   By default, the system is configured to use Milvus Lite.
    -   The Milvus Lite data will be stored in the path specified by `MILVUS_DATA_PATH` in your `.env` file (defaulting to `./data/milvus_data/` if not set and the code defaults to it). Ensure this directory is writable by the application.
    -   No separate Milvus server installation is needed for Milvus Lite.
    -   If you intend to use a standalone Milvus server, update `MILVUS_HOST` and `MILVUS_PORT` accordingly in your `.env` file.

## ⚙️ Running the Application

There are two main ways to run this project, depending on whether you intend to use the FastAPI backend separately.

### Scenario 1: Running Streamlit UI Standalone (Agent logic within Streamlit app)

This is the most common scenario if your Streamlit application directly initializes and uses the `ParkingAgent` from the `agent/` directory.

1.  Ensure your virtual environment is activated:
    ```bash
    source venv/bin/activate # Or your venv activation command
    ```
2.  Navigate to the UI directory and run the Streamlit app:
    ```bash
    cd ui
    streamlit run app.py
    ```
3.  Open your web browser and go to the local URL provided by Streamlit (usually `http://localhost:8501`).

### Scenario 2: Running with a Separate FastAPI Backend

Use this scenario if your `app/main.py` is designed as a separate API backend that the Streamlit UI (or other services) will consume.

1.  Ensure your virtual environment is activated.
2.  **Start the FastAPI Backend:**
    -   Open a new terminal window or tab.
    -   Navigate to the `app/` directory:
        ```bash
        cd app
        ```
    -   Run the FastAPI application using Uvicorn:
        ```bash
        uvicorn main:app --reload --port 8000
        ```
        *(The `--reload` flag is for development. The `--port` can be changed if needed.)*
    -   The FastAPI backend should now be running (typically at `http://localhost:8000`). Check its API documentation (if enabled, usually at `http://localhost:8000/docs`).

3.  **Start the Streamlit UI:**
    -   Open another new terminal window or tab.
    -   Ensure your virtual environment is activated.
    -   Navigate to the `ui/` directory:
        ```bash
        cd ui
        ```
    -   Run the Streamlit app:
        ```bash
        streamlit run app.py
        ```
    -   The Streamlit UI will open in your browser (usually `http://localhost:8501`).
    > **Note:** If your Streamlit UI is designed to communicate with this FastAPI backend, ensure it's configured to point to the correct API base URL (e.g., `http://localhost:8000`). This might be set via an environment variable (e.g., `API_BASE_URL` in the `.env` file).

## 🔑 Environment Variables

The application relies on environment variables for configuration, especially API keys and service connection details. These should be defined in a `.env` file in the project root.

-   `OPENAI_API_KEY`: **(Required)** Your API key for accessing OpenAI models.
-   `MILVUS_HOST`: Hostname for the Milvus server (e.g., `"localhost"`).
-   `MILVUS_PORT`: Port for the Milvus server (e.g., `"19530"`).
-   `MILVUS_DATA_PATH`: Filesystem path where Milvus Lite should store its data (e.g., `"./data/milvus_data"`). Ensure this directory is writable.
-   `API_BASE_URL`: (Optional) If using a separate FastAPI backend (Scenario 2), this is the base URL of that backend (e.g., `"http://localhost:8000"`) used by the Streamlit UI.

<!-- List other environment variables if you have them -->

## 🤔 Troubleshooting

-   **`auth_subrequest_error` from OpenAI:**
    -   Ensure the `OPENAI_API_KEY` in your `.env` file is correct.
    -   Check your OpenAI account for billing issues or insufficient credits.
    -   Verify the `.env` file is in the project root and is being loaded.
-   **Milvus Connection/Initialization Issues:**
    -   Ensure the `MILVUS_DATA_PATH` is writable.
    -   If using a standalone Milvus server, verify it's running and accessible.
    -   Check application logs for Milvus client errors.
-   **Streamlit `watchdog` module warning (macOS):**
    Run: `pip install watchdog`. You might also need: `xcode-select --install`.
-   **`markdown2` library not found:**
    Run: `pip install markdown2` for richer Markdown rendering.
-   **FastAPI backend not reachable from Streamlit (Scenario 2):**
    Ensure the FastAPI server is running. Check `API_BASE_URL` and firewall settings.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📜 License

Distributed under the MIT License. See `LICENSE` file for more information (if you add one).

<!-- If you don't have a LICENSE file, you can state: -->
<!-- This project is currently unlicensed. Feel free to use it as you see fit, or consider adding a license. -->