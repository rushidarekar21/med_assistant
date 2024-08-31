api_key = "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"
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from langchain_groq import ChatGroq
import uvicorn
from fastapi import FastAPI



llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=1,
    groq_api_key = api_key
)

app = FastAPI(
    title = "Simple Server",
    version = '1.0',
    description = "My first api server"
)

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

add_routes(
    app,
    prompt | llm,
    path = "/prompt"
)

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)