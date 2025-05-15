*(See the full structure in previous versions if needed; truncated here for brevity in this example)*

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+
-   Git
-   OpenAI API Key

### Installation & Setup

1.  **Clone repository:**
    ```bash
    git clone <your-repository-url>
    cd parking_agent_system
    ```

2.  **Create & activate virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate    # Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create `.env` file in project root (`parking_agent_system/.env`):
    ```env
    # OpenAI
    OPENAI_API_KEY="sk-YourOpenAIapiKeyHere"

    # Milvus
    MILVUS_HOST="localhost"
    MILVUS_PORT="19530"
    MILVUS_DATA_PATH="./data/milvus_data"

    # Optional for FastAPI scenario
    # API_BASE_URL="http://localhost:8000"
    ```
    > **⚠️ Never commit your `.env` file!**

5.  **Milvus Setup:**
    Milvus Lite data is stored at `MILVUS_DATA_PATH`. No separate server needed for Milvus Lite. For standalone Milvus, update `MILVUS_HOST` and `MILVUS_PORT`.

## ⚙️ Running the Application

Follow the steps for the scenario that fits your needs.

### Scenario 1: Run Streamlit UI (Recommended for most users)

This runs the Parking AI Assistant with its user interface.

1.  **Activate virtual environment** (if not already active).
    ```bash
    source venv/bin/activate
    ```
2.  **Navigate to UI directory and run Streamlit:**
    ```bash
    cd ui
    streamlit run app.py
    ```
3.  Open your browser to `http://localhost:8501` (or the URL shown in your terminal).

### Scenario 2: Run FastAPI Backend (For API development or advanced use)

If you need to run the FastAPI backend separately (e.g., the Streamlit UI is configured to call it, or you're developing API endpoints).

1.  **Activate virtual environment.**
2.  **Start FastAPI server:**
    In a **new terminal**, navigate to the `app/` directory and run:
    ```bash
    cd app
    uvicorn main:app --reload --port 8000
    ```
    The API will be available at `http://localhost:8000`.
3.  **Start Streamlit UI (if needed):**
    Follow steps in **Scenario 1** in a separate terminal. Ensure Streamlit is configured to use the FastAPI backend (e.g., via `API_BASE_URL` in `.env`).

## 🔑 Environment Variables

Key variables to set in your `.env` file:

-   `OPENAI_API_KEY`: **Required.**
-   `MILVUS_HOST`: Default `localhost`.
-   `MILVUS_PORT`: Default `19530`.
-   `MILVUS_DATA_PATH`: Default `./data/milvus_data`.
-   `API_BASE_URL`: (Optional) For Scenario 2, e.g., `http://localhost:8000`.

## 🤔 Troubleshooting

-   **OpenAI `auth_subrequest_error`**: Check `OPENAI_API_KEY` and OpenAI account status.
-   **Milvus Issues**: Ensure `MILVUS_DATA_PATH` is writable. For standalone, check server status.
-   **Module Not Found**: Re-run `pip install -r requirements.txt` in activated venv.

## 🤝 Contributing

Pull Requests are welcome. Fork, branch, commit, and open a PR.

## 📜 License

MIT License (Add a `LICENSE` file for details).