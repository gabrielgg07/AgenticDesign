# agentEx/agent.py or llm_agent/__init__.py
from google.adk.agents import  LlmAgent
from . import prompt
from llm_agent.adk_client import OpenAIClient
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

root_agent = LlmAgent(
    name="financial_advisor_agent",
    description="A financial advisor with numerous amounts of financial tools, documents, and knowledge",
    model=OpenAIClient(),
    instruction=prompt.example_prompt,
    sub_agents=[],
    tools=[
        #MCPToolset(connection_params=SseConnectionParams(url="http://localhost:8931/sse")),
        MCPToolset(connection_params=SseConnectionParams(url="http://localhost:8001/sse"))
    ]
)