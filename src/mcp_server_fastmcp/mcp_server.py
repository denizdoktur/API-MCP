from mcp.server import FastMCP
from tools.code_analysis_tool import CodeAnalysisTool

code_analysis_tool = CodeAnalysisTool()

# MCP Server Imp. with FASTMCP

mcp = mcp_configured = FastMCP(
    name="ConfiguredServer",
    port=8080,  # Sets the default SSE port
    host="127.0.0.1", # Sets the default SSE host
    log_level="DEBUG", # Sets the logging level
    on_duplicate_tools="warn" , # Warn if tools with the same name are registered (options: 'error', 'warn', 'ignore')
    tools=[code_analysis_tool],
    path="/mcp"
)

# Entry point to run the server
if __name__ == "__main__":
    mcp.run(transport="sse")
    # mcp.run(transport="streamable-http")