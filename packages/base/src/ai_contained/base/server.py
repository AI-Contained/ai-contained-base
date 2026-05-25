"""MCP server entry point."""

import argparse
import os
from collections.abc import AsyncGenerator

from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan
from starlette.requests import Request
from starlette.responses import JSONResponse

from ai_contained.core.mcp import load_providers


@lifespan
async def load_providers_lifespan(server: FastMCP) -> AsyncGenerator[None, None]:
    """Discover and load all installed providers before the server starts accepting requests."""
    await load_providers(server)
    yield


mcp = FastMCP("ai-contained", lifespan=load_providers_lifespan)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Return server health status."""
    return JSONResponse({"status": "healthy"})


def main() -> None:
    """Start the MCP HTTP server."""
    parser = argparse.ArgumentParser(description="AI-Contained MCP server")
    parser.add_argument("--host", default=os.getenv("ADDRESS", "0.0.0.0"), help="Address to bind to")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8080")), help="Port to listen on")
    args = parser.parse_args()

    mcp.run(
        transport="http",
        host=args.host,
        port=args.port,
        show_banner=False,
    )


if __name__ == "__main__":
    main()
