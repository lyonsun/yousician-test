import os

from app import create_app

from dotenv import load_dotenv
load_dotenv()

print("test: %s", os.getenv("APP_ENVIRONMENT"))
config_name = os.getenv("APP_ENVIRONMENT")
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
