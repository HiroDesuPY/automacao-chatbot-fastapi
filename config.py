from dotenv import load_dotenv
import os


load_dotenv()

PINECONEAPI = os.getenv("PINECONEAPI")
TELEGRAMBOT_API = os.getenv("TELEGRAMBOT_API")

print(f"PINECONEAPI: {PINECONEAPI}")
print(f"TELEGRAMBOT_API: {TELEGRAMBOT_API}")