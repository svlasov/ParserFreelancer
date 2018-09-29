import os

# settings.py
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.environ.get("API_KEY")
USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']


if __name__ == "__main__":
    print(API_KEY)
