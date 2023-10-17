import openai
import dotenv
import os

dotenv.load_dotenv()
key = os.getenv("OPENAI_API_KEY")

def generate_sql_query(messages):
    response = openai.ChatCompletion.create(
      api_key=key,
      model='gpt-4',
      messages = messages,
      max_tokens=1024
    )
    return response