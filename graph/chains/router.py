from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel,Field
from typing import Literal #hangi tipte veri beklediğimizi belirleyeceğiz typingle

class RouteQuery(BaseModel):
    """
    Route a user query to the most relevant datasource
    """
    datasource: Literal["vectorstore","websearch"]=Field(
        default=...,
        description="Given a user question choose to route it to web search or a vectorstore"

    )
#default=..., bizim verdiğimiz iki değişkenden birini alacak başka bir cıktı kabul etmeyecek
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
structured_llm_router = llm.with_structured_output(RouteQuery)
# LLM'in çıktısını RouteQuery formatına sokuyoruz, yani LLM kafasına göre cevap vermeyecek datasource alanında "vectorstore" veya "websearch" döndürmesi gerekiyor.

system = """
You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. For all else, use web-search.
"""
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router