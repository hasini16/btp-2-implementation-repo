import os

def create_structure():
    # Define the directory and file structure
    structure = {
        "cnc_automation_project": {
            "backend": {
                "api": ["__init__.py", "routes.py"],
                "cad_integration": ["__init__.py", "sw_connection.py", "feature_recognition.py", "gcode_generator.py"],
                "ml_models": ["__init__.py", "cnn_lstm.py", "xai_explainer.py", "saved_models/"],
                "app.py": "",
                "requirements.txt": "flask\nfastapi\npywin32\ntensorflow\nkeras\nlime\npandas\nnumpy"
            },
            "frontend": {
                "public": ["index.html"],
                "src": {
                    "components": [],
                    "services": [],
                    "App.js": ""
                },
                "package.json": ""
            },
            "docs": {
                "outputs": [],
                "architecture.dot": ""
            }
        }
    }

    def build(base_path, layout):
        for name, content in layout.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                build(path, content)
            elif isinstance(content, list):
                os.makedirs(path, exist_ok=True)
                for item in content:
                    if item.endswith('/'):
                        os.makedirs(os.path.join(path, item), exist_ok=True)
                    else:
                        open(os.path.join(path, item), 'a').close()
            else:
                with open(path, 'w') as f:
                    f.write(content)

    print("Building project structure...")
    build(".", structure)
    print("Project scaffolded successfully!")

if __name__ == "__main__":
    create_structure()