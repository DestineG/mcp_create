"""Entry point for running the MCP Scholar server."""

from .server import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
