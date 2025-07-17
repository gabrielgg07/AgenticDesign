from fastmcp import FastMCP
from langChain_server import lang_mcp
from news_server import news_mcp

main_mcp = FastMCP(
    name="Main MCP Server",
    instructions="This is helpful in importing all the mcp server listed"
)

main_mcp.mount("lang_mcp", lang_mcp)
main_mcp.mount("news_mcp", news_mcp)


if __name__ == "__main__":
    main_mcp.run(transport="sse", host="127.0.0.1", port=8001)
