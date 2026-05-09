"""MCP server entry point."""

import os

from fastmcp import FastMCP
from starlette.responses import JSONResponse

from ai_contained.core.mcp import load_providers

mcp = FastMCP("ai-contained")
load_providers(mcp)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):  # type: ignore[no-untyped-def]
    """Return server health status."""
    return JSONResponse({"status": "healthy"})


def main() -> None:
    """Start the MCP HTTP server."""
    mcp.run(
        transport="http",
        host=os.getenv("ADDRESS", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        show_banner=False,
    )


if __name__ == "__main__":
    main()
