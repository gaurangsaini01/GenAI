from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

res = client.embeddings.create(
    input="Hi Turn me into vector embedding please",
    model="text-embedding-3-small"
)
print(res)