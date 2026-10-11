from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel,Field
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score:str=Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )

structured_llm_grader=llm.with_structured_output(GradeDocuments)
system = """You are a grader assessing relevance of a retrieved document to a user question.  \n
    If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals.\n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

grade_prompt=ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human","Retrieved document: {document} User question: {question}"),
    ]
)
retrieval_grader=grade_prompt | structured_llm_grader
