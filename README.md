<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parking AI Assistant</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            line-height: 1.6;
            color: #24292e;
            margin: 0;
            padding: 0;
            background-color: #f6f8fa;
        }
        .container {
            max-width: 900px;
            margin: 40px auto;
            padding: 30px;
            background-color: #fff;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
        }
        h1, h2, h3 {
            color: #0366d6;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; }
        h3 { font-size: 1.25em; }
        p { margin-bottom: 1em; }
        ul { padding-left: 20px; }
        li { margin-bottom: 0.5em; }
        code {
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            background-color: rgba(27,31,35,0.05);
            border-radius: 3px;
        }
        pre {
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            background-color: #f6f8fa;
            border-radius: 3px;
            border: 1px solid #e1e4e8;
        }
        pre code {
            display: inline;
            padding: 0;
            margin: 0;
            overflow: visible;
            line-height: inherit;
            word-wrap: normal;
            background-color: transparent;
            border: 0;
        }
        .header-icon {
            font-size: 1.5em;
            margin-right: 10px;
        }
        .section {
            margin-bottom: 30px;
        }
        .note {
            background-color: #fffbdd;
            border-left: 4px solid #ffeb3b;
            padding: 10px 15px;
            margin-bottom: 15px;
            border-radius: 3px;
        }
        .warning {
            background-color: #ffebe9;
            border-left: 4px solid #d73a49;
            padding: 10px 15px;
            margin-bottom: 15px;
            border-radius: 3px;
        }
        .env-example {
            background-color: #f0f0f0;
            border: 1px dashed #ccc;
            padding: 10px;
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            white-space: pre;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><span class="header-icon">🚗</span> Parking AI Assistant</h1>

        <div class="section">
            <p>
                Welcome to the Parking AI Assistant project! This system provides an intelligent assistant to help users find and book parking spots.
                It leverages a conversational AI agent, a vector database for storing conversation history and relevant parking information,
                and a user-friendly web interface.
            </p>
            <!-- Add a screenshot or GIF of the UI here if you have one -->
            <!-- <img src="path/to/your/screenshot.png" alt="Parking AI Assistant UI" style="max-width:100%; border-radius: 6px; margin-bottom: 20px;"> -->
        </div>

        <div class="section">
            <h2>✨ Features</h2>
            <ul>
                <li>Conversational interface for parking queries powered by a LangChain agent.</li>
                <li>Ability to find parking spots based on location, time, and other criteria.</li>
                <li>Potential to book parking spots (if backend integration and agent tools support it).</li>
                <li>Milvus Lite for efficient similarity search and storing embeddings (e.g., for conversation history or RAG).</li>
                <li>Streamlit-based user interface for easy interaction.</li>
                <li>Optional FastAPI backend (<code>app/</code> directory) for serving API endpoints, potentially for more complex operations or decoupling logic from the UI.</li>
            </ul>
        </div>

        <div class="section">
            <h2>🛠️ Tech Stack</h2>
            <ul>
                <li><strong>Python 3.9+</strong></li>
                <li><strong>AI Agent Framework:</strong> LangChain</li>
                <li><strong>LLM:</strong> OpenAI (e.g., GPT-3.5-turbo, GPT-4)</li>
                <li><strong>UI Framework:</strong> Streamlit</li>
                <li><strong>Backend API (Optional):</strong> FastAPI (if <code>app/main.py</code> is used as a backend)</li>
                <li><strong>Vector Database:</strong> Milvus Lite (configurable for standalone Milvus)</li>
                <li><strong>Environment Management:</strong> <code>.env</code> files for secrets and configuration</li>
            </ul>
        </div>

        <div class="section">
            <h2>📂 Project Structure</h2>
            <pre><code>parking_agent_system/
├── 📦 app/                     # Optional FastAPI backend
│   ├── 📄 __init__.py
│   ├── 🚀 main.py             # FastAPI application
│   ├── 🧠 models.py           # Database models (e.g., SQLAlchemy)
│   ├── 📐 schemas.py          # Pydantic schemas for API
│   ├── 🗃️ database.py        # Database connection setup
│   ├── 🛠️ crud.py              # CRUD operations for the database
│   └── 🌱 initial_data.py    # Script for initial data seeding
├── 🤖 agent/                    # Core LangChain agent logic
│   ├── 📄 __init__.py
│   ├── 🅿️ parking_agent.py     # Main agent definition
│   ├── 🧰 tools.py               # Custom tools for the agent
│   └── 📝 prompts.py            # Prompts for the agent
├── 📊 milvus_utils/             # Utilities for Milvus connection
│   ├── 📄 __init__.py
│   └── 🔌 milvus_connector.py
├── 🖥️ ui/                        # Streamlit user interface
│   ├── 📄 __init__.py
│   └── 🌐 app.py                # Main Streamlit application
├── 📂 data/                      # Data storage (e.g., Milvus data)
│   └── milvus_data/           # Default Milvus Lite data path (ignored by .gitignore)
├── 🧪 .env                       # Environment variables (GITIGNORED!)
├── 📜 requirements.txt          # Python dependencies
└── 📘 README.md                  # This file
</code></pre>
        </div>

        <div class="section">
            <h2>🚀 Getting Started</h2>

            <h3>Prerequisites</h3>
            <ul>
                <li>Python 3.9 or higher</li>
                <li>Git</li>
                <li>An OpenAI API Key</li>
                <li>(For macOS users needing <code>watchdog</code> for Streamlit hot-reloading):
                    <pre><code>xcode-select --install</code></pre>
                </li>
            </ul>

            <h3>Installation & Setup</h3>
            <ol>
                <li><strong>Clone the repository:</strong>
                    <pre><code>git clone <your-repository-url>
cd parking_agent_system</code></pre>
                </li>
                <li><strong>Create and activate a virtual environment (recommended):</strong>
                    <pre><code>python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate</code></pre>
                </li>
                <li><strong>Install dependencies:</strong>
                    <pre><code>pip install -r requirements.txt</code></pre>
                </li>
                <li>
                    <strong>Set up Environment Variables:</strong><br>
                    Create a <code>.env</code> file in the root of the project (<code>parking_agent_system/.env</code>).
                    <div class="warning">
                        <strong>Important:</strong> The <code>.env</code> file is ignored by Git (as it should be) and contains sensitive information like your API key. <strong>Never commit it to your repository.</strong>
                    </div>
                    Add your configurations to it. Here's an example:
                    <div class="env-example">
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
                    </div>
                </li>
                <li>
                    <strong>Milvus Setup:</strong><br>
                    By default, the system is configured to use Milvus Lite.
                    <ul>
                        <li>The Milvus Lite data will be stored in the path specified by <code>MILVUS_DATA_PATH</code> in your <code>.env</code> file (defaulting to <code>./data/milvus_data/</code> if not set and the code defaults to it). Ensure this directory is writable by the application.</li>
                        <li>No separate Milvus server installation is needed for Milvus Lite.</li>
                        <li>If you intend to use a standalone Milvus server, update <code>MILVUS_HOST</code> and <code>MILVUS_PORT</code> accordingly in your <code>.env</code> file.</li>
                    </ul>
                </li>
            </ol>
        </div>

        <div class="section">
            <h2>⚙️ Running the Application</h2>
            <p>There are two main ways to run this project, depending on whether you intend to use the FastAPI backend separately.</p>

            <h3>Scenario 1: Running Streamlit UI Standalone (Agent logic within Streamlit app)</h3>
            <p>This is the most common scenario if your Streamlit application directly initializes and uses the <code>ParkingAgent</code> from the <code>agent/</code> directory.</p>
            <ol>
                <li>
                    <strong>Ensure your virtual environment is activated:</strong>
                    <pre><code>source venv/bin/activate  # Or your venv activation command</code></pre>
                </li>
                <li>
                    <strong>Navigate to the UI directory and run the Streamlit app:</strong>
                    <pre><code>cd ui
streamlit run app.py</code></pre>
                </li>
                <li>Open your web browser and go to the local URL provided by Streamlit (usually <code>http://localhost:8501</code>).</li>
            </ol>

            <h3>Scenario 2: Running with a Separate FastAPI Backend</h3>
            <p>
                Use this scenario if your <code>app/main.py</code> is designed as a separate API backend that the Streamlit UI (or other services) will consume.
                This might be for more complex operations, data management, or if you want to expose agent functionalities via API endpoints.
            </p>
            <ol>
                <li>
                    <strong>Ensure your virtual environment is activated.</strong>
                </li>
                <li>
                    <strong>Start the FastAPI Backend:</strong>
                    <ul>
                        <li>Open a new terminal window or tab.</li>
                        <li>Navigate to the <code>app/</code> directory:
                            <pre><code>cd app</code></pre>
                        </li>
                        <li>Run the FastAPI application using Uvicorn (a common ASGI server):
                            <pre><code>uvicorn main:app --reload --port 8000</code></pre>
                            (The <code>--reload</code> flag is useful for development as it restarts the server on code changes. You can change the <code>--port</code> if needed.)
                        </li>
                        <li>The FastAPI backend should now be running (typically at <code>http://localhost:8000</code>). You can check its API documentation (if enabled, usually at <code>http://localhost:8000/docs</code>).</li>
                    </ul>
                </li>
                <li>
                    <strong>Start the Streamlit UI:</strong>
                    <ul>
                        <li>Open another new terminal window or tab (or use the previous one if you backgrounded the FastAPI server).</li>
                        <li>Ensure your virtual environment is activated.</li>
                        <li>Navigate to the <code>ui/</code> directory:
                            <pre><code>cd ui</code></pre>
                        </li>
                        <li>Run the Streamlit app:
                            <pre><code>streamlit run app.py</code></pre>
                        </li>
                        <li>The Streamlit UI will open in your browser (usually <code>http://localhost:8501</code>).</li>
                        <li>
                            <div class="note">
                                <strong>Important:</strong> If your Streamlit UI is designed to communicate with this FastAPI backend, ensure it's configured to point to the correct API base URL (e.g., <code>http://localhost:8000</code>). This might be set via an environment variable (e.g., <code>API_BASE_URL</code> in the <code>.env</code> file) or hardcoded (less ideal).
                            </div>
                        </li>
                    </ul>
                </li>
            </ol>
        </div>


        <div class="section">
            <h2>🔑 Environment Variables</h2>
            <p>The application relies on environment variables for configuration, especially API keys and service connection details. These should be defined in a <code>.env</code> file in the project root.</p>
            <ul>
                <li><code>OPENAI_API_KEY</code>: <strong>(Required)</strong> Your API key for accessing OpenAI models.</li>
                <li><code>MILVUS_HOST</code>: Hostname for the Milvus server (e.g., <code>"localhost"</code> for local Milvus Lite or a standalone server).</li>
                <li><code>MILVUS_PORT</code>: Port for the Milvus server (e.g., <code>"19530"</code>).</li>
                <li><code>MILVUS_DATA_PATH</code>: Filesystem path where Milvus Lite should store its data (e.g., <code>"./data/milvus_data"</code>). Ensure this directory is writable.</li>
                <li><code>API_BASE_URL</code>: (Optional) If using a separate FastAPI backend (Scenario 2), this is the base URL of that backend (e.g., <code>"http://localhost:8000"</code>) used by the Streamlit UI.</li>
                <!-- List other environment variables if you have them -->
            </ul>
        </div>

        <div class="section">
            <h2>🤔 Troubleshooting</h2>
            <ul>
                <li>
                    <strong><code>auth_subrequest_error</code> from OpenAI:</strong> This usually indicates an issue with your <code>OPENAI_API_KEY</code>.
                    <ul>
                        <li>Ensure the key in your <code>.env</code> file is correct and has no typos.</li>
                        <li>Check your OpenAI account for billing issues, insufficient credits, or if the key has been revoked.</li>
                        <li>Verify the <code>.env</code> file is in the project root (<code>parking_agent_system/.env</code>) and is being loaded correctly.</li>
                    </ul>
                </li>
                <li>
                    <strong>Milvus Connection/Initialization Issues:</strong>
                    <ul>
                        <li>Ensure the <code>MILVUS_DATA_PATH</code> specified in your <code>.env</code> file is writable by the application.</li>
                        <li>If using a standalone Milvus server, verify it's running and accessible at the specified <code>MILVUS_HOST</code> and <code>MILVUS_PORT</code>.</li>
                        <li>Check for any error messages from the <code>milvus_connector.py</code> or related Milvus client libraries in your application logs.</li>
                    </ul>
                </li>
                <li>
                    <strong>Streamlit <code>watchdog</code> module warning (macOS):</strong> If you see a warning about installing `watchdog` for better performance, run:
                    <pre><code>pip install watchdog</code></pre>
                    You might also need to install Xcode command-line tools if prompted: <code>xcode-select --install</code>.
                </li>
                 <li>
                    <strong><code>markdown2</code> library not found:</strong> If you see warnings about `markdown2` not being found, install it for richer Markdown rendering in the assistant's responses:
                    <pre><code>pip install markdown2</code></pre>
                </li>
                <li>
                    <strong>FastAPI backend not reachable from Streamlit:</strong> If using Scenario 2, ensure the FastAPI server is running and accessible. Check for typos in the <code>API_BASE_URL</code> if used. Firewall settings could also be an issue in some environments.
                </li>
            </ul>
        </div>

        <div class="section">
            <h2>🤝 Contributing</h2>
            <p>Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.</p>
            <ol>
                <li>Fork the Project.</li>
                <li>Create your Feature Branch (<code>git checkout -b feature/AmazingFeature</code>).</li>
                <li>Commit your Changes (<code>git commit -m 'Add some AmazingFeature'</code>).</li>
                <li>Push to the Branch (<code>git push origin feature/AmazingFeature</code>).</li>
                <li>Open a Pull Request.</li>
            </ol>
        </div>

        <div class="section">
            <h2>📜 License</h2>
            <p>Distributed under the MIT License. See <code>LICENSE</code> file for more information (if you add one).</p>
            <!-- If you don't have a LICENSE file, you can state:
            <p>This project is currently unlicensed. Feel free to use it as you see fit, or consider adding a license.</p>
            -->
        </div>

    </div>
</body>
</html>