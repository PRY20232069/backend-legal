from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
import os

load_dotenv()

NUMBER_OF_TERMS_PROCESSED_IN_PARALLEL=int(os.getenv("NUMBER_OF_TERMS_PROCESSED_IN_PARALLEL"))

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

OPENAI_MODEL_ID_1X1=os.getenv("OPENAI_MODEL_ID_1X1")
OPENAI_SYSTEM_CONTENT_1X1=os.getenv("OPENAI_SYSTEM_CONTENT_1X1")

OPENAI_MODEL_ID_3X3=os.getenv("OPENAI_MODEL_ID_3X3")
OPENAI_SYSTEM_CONTENT_3X3=os.getenv("OPENAI_SYSTEM_CONTENT_3X3")

DB_HOST=os.getenv("DB_HOST")
DB_NAME=os.getenv("DB_NAME")
DB_USERNAME=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")

DB_CONNECTION_URI=os.getenv("DB_CONNECTION_URI")

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

ORIGIN_ALLOWED_1=os.getenv("ORIGIN_ALLOWED_1")
ORIGIN_ALLOWED_2=os.getenv("ORIGIN_ALLOWED_2")
ORIGIN_ALLOWED_3=os.getenv("ORIGIN_ALLOWED_3")
ORIGIN_ALLOWED_4=os.getenv("ORIGIN_ALLOWED_4")
ORIGIN_ALLOWED_5=os.getenv("ORIGIN_ALLOWED_5")
ORIGIN_ALLOWED_6=os.getenv("ORIGIN_ALLOWED_6")

FIREBASE_CERTIFICATE_FILE=os.getenv("FIREBASE_CERTIFICATE_FILE")
FIREBASE_STORAGE_ACCESS_URL=os.getenv("FIREBASE_STORAGE_ACCESS_URL")

EMAIL_ADDRESS=os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD=os.getenv('EMAIL_PASSWORD')
EMAIL_FROM=os.getenv('EMAIL_FROM')

RECOVERY_EMAIL_SUBJECT=os.getenv('RECOVERY_EMAIL_SUBJECT')
RECOVERY_EMAIL_CONTENT=os.getenv('RECOVERY_EMAIL_CONTENT')

DEFAULT_USER_PASSWORD=os.getenv('DEFAULT_USER_PASSWORD')


cred = credentials.Certificate(FIREBASE_CERTIFICATE_FILE)
initialize_app(cred, {'storageBucket': FIREBASE_STORAGE_ACCESS_URL})




# TODO: PARA TP2 AGREGAR TESTING