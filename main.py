import os
from app import create_app

app = create_app(os.environ.get("FLASK_ENVIRON") or "development")

if __name__ == "__main__":
    app.run()
