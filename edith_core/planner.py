# planner.py

import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.2,
    openai_api_key=OPENAI_API_KEY
)

def plan_task(user_goal: str):
    prompt = f"""
You are an intelligent task planner for Android UI automation testing.
Given a high-level goal, break it down into step-by-step UI actions.

Format your answer as a numbered list of short steps.

Goal: {user_goal}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.splitlines()
