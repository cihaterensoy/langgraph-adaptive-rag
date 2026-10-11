#burada vector database'imizi oluşturacağız

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]
docs=[WebBaseLoader(url).load() for url in urls] # webbaseloader ile sayfayı langchainin document nesnesine çevirdik
docs_list = [item for sublist in docs for item in sublist] # 3 ana dökümanı bir subliste ayırıp bu sublisti item'a ayırıyoruz

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250,chunk_overlap=0
)
splits = text_splitter.split_documents(docs_list)#dökümanları daha küçük parçalara ayırıyoruz
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)
vectorstore = Chroma.from_documents(
    documents=splits,
    collection_name="rag-chroma",
    embedding=embeddings,
    persist_directory="./.chroma"#vektör storumuzu chroma adlı klasöre kaydedecek
)
# dökümanları embedding'e çevirip Chroma vector database'e kaydediyoruz
retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=embeddings,
).as_retriever() #Vector database'i soru sorulduğunda ilgili döküman parçalarını getirebilecek bir retriever'a dönüştürüyo
# daha sonra database'den benzer dökümanları bulmak için retriever oluşturuyoruz