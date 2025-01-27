from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

MODEL_NAMES = [
    "llama3-70b-8192",
    "mixtral-8x7b-32768"
]

tool_tavily = TavilySearchResults(max_results=2)

tools = [tool_tavily]

app = FastAPI(title='LangGraph AI Agent')

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]

@app.post("/chat")
def chat_endpoint(request: RequestState):
    if request.model_name not in MODEL_NAMES:
        return {"error": "Invalid model name. Please select a valid model."}

    llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name=request.model_name)
    agent = create_react_agent(llm, tools=tools, state_modifier=request.system_prompt)

    state = {"messages": request.messages}
    result = agent.invoke(state)

    return result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
