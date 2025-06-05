from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
load_dotenv()

file_path =Path(__file__).parent / "nodejs.pdf"

#Loading the file

loader = PyPDFLoader(file_path)
docs = loader.load()
# print(docs[2])

# chunking the file

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=200,
)
split_docs = text_splitter.split_documents(documents=docs)
# print(split_docs[50])

#Vector Embeddings banane hai ab
#model define kera embedding ka
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

#yahan pe model bata diya embedding me jisse wo apne aap embeding bana ke store kerde db me in collection_name
vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="my_documents",
    embedding=embeddings
)
print("INGESTION DONE...")
