from typing import Any,Dict
from graph.state import GraphState
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document

web_search_tool=TavilySearchResults(k=3)

def web_search(state: GraphState) -> Dict[str, Any]:
    print("----web search----")

    question = state['question']
    documents = state['documents']

    docs= web_search_tool.invoke({"query":question}) #kullanıcının sorusunu aratıyoruz
    web_results="\n".join([d["conent"] for d in docs])  # Arama sonuçlarının içeriklerini tek bir metinde birleştiriyoruz

    web_results=Document(page_content=web_results)  # Web arama sonuçlarını LangChain Document nesnesine dönüştürüyoruz

    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents":documents,"question":question}

