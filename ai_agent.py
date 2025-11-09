from pydantic import BaseModel, Field
from uagents import Agent, Context, Protocol, Model
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

CHAT_MODEL = "gpt-4o-mini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

agent = Agent(name="open_ai_agent",
              seed="open_ai_agent_seed_phrase_12345",  # Add your unique seed
              port=8000,
              endpoint=["http://127.0.0.1:8000/submit"]
              )

class AIRequest(BaseModel):
    question: str = Field(
        description="The question that the user wants to have an answer for."
    )

class AIResponse(BaseModel):
    answer: str = Field(
        description="The answer from AI agent to the user agent"
    )

PROMPT_TEMPLATE = """
Answer the following question:
{question}
"""

@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)

def query_openai_chat(prompt: str):
    client = OpenAI(
        api_key=OPENAI_API_KEY,  
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",  # Changed from "system" to "user" for questions
                "content": prompt,
            }
        ],
        model=CHAT_MODEL,  # Use the constant instead of hardcoded value
    )
    return chat_completion.choices[0].message.content

@agent.on_message(model=AIRequest, replies=AIResponse)
async def answer_question(ctx: Context, sender: str, msg: AIRequest):
    ctx.logger.info(f"Received question from {sender}: {msg.question}")
    prompt = PROMPT_TEMPLATE.format(question=msg.question)
    response = query_openai_chat(prompt)
    ctx.logger.info(f"Response: {response}")
    await ctx.send(
        sender, AIResponse(answer=response)
    )

if __name__ == "__main__":
    agent.run()