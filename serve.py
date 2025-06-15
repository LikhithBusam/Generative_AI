# from fastapi import FastAPI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_groq import ChatGroq
# import os
# from langserve import add_routes
# from dotenv import load_dotenv
# load_dotenv()

# groq_api_key=os.getenv("GROQ_API_KEY")
# model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

# # 1. Create prompt template
# system_template = "Translate the following into {language}:"
# prompt_template = ChatPromptTemplate.from_messages([
#     ('system', system_template),
#     ('user', '{text}')
# ])

# parser=StrOutputParser()

# ##create chain
# chain=prompt_template|model|parser



# ## App definition
# app=FastAPI(title="Langchain Server",
#             version="1.0",
#             description="A simple API server using Langchain runnable interfaces")

# ## Adding chain routes
# add_routes(
#     app,
#     chain,
#     path="/chain"
# )

# if __name__=="__main__":
#     import uvicorn
#     uvicorn.run(app,host="127.0.0.1",port=8001)


from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# LangChain components
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Load LLM
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate the following into {language}:"),
    ("user", "{text}")
])

# Output parser
parser = StrOutputParser()

# Chain: Prompt → LLM → Parser
chain = prompt | model | parser

# FastAPI app setup
app = FastAPI(
    title="LangChain Translator API",
    version="1.0",
    description="A simple translation API using LangChain + Groq"
)

# Request body model
class TranslationRequest(BaseModel):
    language: str
    text: str

# Translation endpoint
@app.post("/translate")
def translate(request: TranslationRequest):
    try:
        result = chain.invoke({
            "language": request.language,
            "text": request.text
        })
        return {"translated_text": result}
    except Exception as e:
        return {"error": str(e)}
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8001)
