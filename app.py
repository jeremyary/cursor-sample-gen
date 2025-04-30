from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastmcp import FastMCP
from typing import Dict, Any
import uvicorn
import markdown2
import os
import re
from pathlib import Path

app = FastAPI(title="MCP Service")
mcp = FastMCP()

# Setup templates
templates = Jinja2Templates(directory="templates")

# Mount static files
static_path = Path("static")
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

def process_mermaid_blocks(content: str) -> str:
    """Process markdown content to properly handle Mermaid diagrams."""
    # Find all mermaid code blocks
    pattern = r"```mermaid\n(.*?)\n```"
    
    def replace_mermaid(match):
        diagram_code = match.group(1)
        # Escape any HTML special characters in the diagram code
        diagram_code = diagram_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<div class="mermaid">\n{diagram_code}\n</div>'
    
    # Replace mermaid code blocks with div elements
    content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)
    return content

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        # Read README content
        with open("README.md", "r") as f:
            readme_content = f.read()
        
        # Process mermaid diagrams first
        readme_content = process_mermaid_blocks(readme_content)
        
        # Convert markdown to HTML with extras
        html_content = markdown2.markdown(
            readme_content,
            extras=[
                "fenced-code-blocks",
                "tables",
                "header-ids",
                "task-lists",
                "code-friendly"
            ]
        )
        
        # Get the title from the first line of the README
        title = readme_content.split("\n")[0].strip("# ")
        
        # Return the formatted HTML page
        return templates.TemplateResponse(
            "docs.html",
            {
                "request": {},  # FastAPI requires this
                "title": title,
                "content": html_content
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/send")
async def send_message(message: Dict[str, Any]):
    try:
        response = await mcp.send_message(message)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/mcp/status")
async def get_status():
    return {"status": "active", "connections": mcp.get_connection_count()}

@app.post("/mcp/connect")
async def connect_to_mcp(connection_params: Dict[str, Any]):
    try:
        await mcp.connect(**connection_params)
        return {"status": "connected"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/mcp/disconnect")
async def disconnect_from_mcp():
    try:
        await mcp.disconnect()
        return {"status": "disconnected"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/LICENSE", response_class=PlainTextResponse)
async def read_license():
    try:
        with open("LICENSE", "r") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=404, detail="License file not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000) 