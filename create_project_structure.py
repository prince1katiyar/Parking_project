import os

structure = {
    "parking_agent_system": {
        "app": ["__init__.py", "main.py", "models.py", "schemas.py", "database.py", "crud.py", "initial_data.py"],
        "agent": ["__init__.py", "parking_agent.py", "tools.py", "prompts.py"],
        "milvus_utils": ["__init__.py", "milvus_connector.py"],
        "ui": ["__init__.py", "app.py"],
        "data": ["parking.db"], 
        "": [".env", "requirements.txt", "README.md"]
    }
}

def create_structure(base_path, structure):
    for root, files in structure.items():
        folder_path = os.path.join(base_path, root)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'w') as f:
                if file.endswith(".py"):
                    f.write(f"# {file}\n")
                elif file == "README.md":
                    f.write("# Parking Agent System\n\nProject documentation goes here.")
                elif file == ".env":
                    f.write("OPENAI_API_KEY=\nMILVUS_URI=\n")
                elif file == "requirements.txt":
                    f.write("fastapi\nuvicorn\nsqlalchemy\npydantic\nlangchain\nopenai\nstreamlit\npymilvus\n")
                else:
                    pass 
if __name__ == "__main__":
    create_structure(".", structure["parking_agent_system"])
    print("✅ Project structure created successfully.")
