from uagents import Agent, Context, Field, Model, Protocol
from pydantic import BaseModel, Field
import asyncio

# Replace this with YOUR AI agent's address from the logs
AI_AGENT_ADDRESS = "agent1qdpzrc02a8lnlzaahtdyy3wnaux64pqa22vykp59tx67jx2mmy3dzf249jk"

agent = Agent(name="simple test agent",
              seed="simple_test_agent_seed_12345",  # Changed seed
              port=9000,
              endpoint=["http://127.0.0.1:9000/submit"]
              )

QUESTION = "Write the Javascript code to give me the sum from 1 to 10"


class AIRequest(BaseModel):
    question: str = Field(
        description="The question that the user wants to have an answer for."
    )


class AIResponse(BaseModel):
    answer: str = Field(
        description="The answer from AI agent to the user agent"
    )


@agent.on_event("startup")
async def ask_question(ctx: Context):
    ctx.logger.info(
        f"Asking AI agent to answer {QUESTION}"
    )
    # Add a delay to ensure AI agent is registered
    await asyncio.sleep(5)
    
    await ctx.send(
        AI_AGENT_ADDRESS,  # Changed from 'THE OTHER AGENTS ADDR'
        AIRequest(question=QUESTION)
    )


@agent.on_message(model=AIResponse)
async def handle_data(ctx: Context, sender: str, data: AIResponse):
    ctx.logger.info(f"Got response from AI agent: {data.answer}")

if __name__ == "__main__":
    agent.run()