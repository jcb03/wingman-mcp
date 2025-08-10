import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Test if loading worked
api_key = os.getenv("OPENAI_API_KEY")
print(f"✅ API Key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"✅ API Key starts with: {api_key[:10]}...")

import uvicorn
from mcp_server import mcp
from fastapi.responses import HTMLResponse

# Get the FastMCP app using the CORRECT method
app = mcp.http_app()  # ← METHOD with parentheses, not attribute

# Add health check endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>Dating Wingman MCP Server</title></head>
        <body>
            <h1>🎯 Dating Wingman MCP Server</h1>
            <p>✅ Server is running successfully!</p>
            <p>🚀 Ready for Puch AI integration!</p>
            <p>📱 Connect via: <code>/mcp connect [URL]/mcp puch2024</code></p>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "tools": 8, 
        "api_key_loaded": bool(os.getenv("OPENAI_API_KEY")),
        "app_name": os.getenv("APP_NAME", "Dating Wingman")
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        access_log=True
    )
