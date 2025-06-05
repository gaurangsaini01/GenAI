from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()
query = input("🙋🏻‍♂️ : ")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
)
#connection with DB or instance leliya db ka
vector_db = QdrantVectorStore.from_existing_collection(url="http://localhost:6333",
                                                       collection_name="my_documents",embedding=embeddings)
#search in DB now using similarity search in Qdrant db
results = vector_db.similarity_search(query=query)

#Ab llm ko dena h context

context = []
for result in results:
    page = {"page_content":result.page_content,"page_number":result.metadata['page_label']}
    context.append(page)

stringified_context = json.dumps(context)

SYSTEM_PROMPT = f"""
You are an AI agent who answers users query based on the available context along with page content and page number .
You need to find the answer to user query from the context not from your intelligence and give it to user . Tell the page number to the user also .

Don't say "Based on the Context" like sentences , simply provide answer and say "\n for more reference visit page number" .

Context :
 {stringified_context}
"""

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":query}]
)
print("🤖: ",response.choices[0].message.content)


