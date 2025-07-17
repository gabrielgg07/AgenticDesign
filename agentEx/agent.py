# agentEx/agent.py or llm_agent/__init__.py
from google.adk.agents import  LlmAgent
from . import prompt
from llm_agent.adk_client import OpenAIClient

root_agent = LlmAgent(
    name="example_agent",
    description="Custom OpenAI agent",
    model=OpenAIClient(),
    instruction=prompt.example_prompt,
    sub_agents=[]
)