import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("mcp-time")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_current_time",
            description="Get current time in a specific timezone or UTC",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone name (e.g., 'America/New_York', 'Asia/Shanghai', 'UTC')",
                        "default": "UTC"
                    },
                    "format": {
                        "type": "string",
                        "description": "Time format: 'iso', 'unix', or 'human'",
                        "enum": ["iso", "unix", "human"],
                        "default": "iso"
                    }
                }
            }
        ),
        Tool(
            name="convert_timezone",
            description="Convert time between timezones",
            inputSchema={
                "type": "object",
                "properties": {
                    "time": {
                        "type": "string",
                        "description": "Time in ISO format (e.g., '2024-01-01T12:00:00')"
                    },
                    "from_timezone": {
                        "type": "string",
                        "description": "Source timezone (e.g., 'America/New_York')",
                        "default": "UTC"
                    },
                    "to_timezone": {
                        "type": "string",
                        "description": "Target timezone (e.g., 'Asia/Shanghai')"
                    }
                },
                "required": ["time", "to_timezone"]
            }
        ),
        Tool(
            name="list_timezones",
            description="List all available timezone names",
            inputSchema={
                "type": "object",
                "properties": {
                    "region": {
                        "type": "string",
                        "description": "Filter by region (e.g., 'America', 'Asia', 'Europe')"
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "get_current_time":
            tz_name = arguments.get("timezone", "UTC")
            fmt = arguments.get("format", "iso")

            tz = ZoneInfo(tz_name)
            now = datetime.now(tz)

            if fmt == "unix":
                result = {"timestamp": int(now.timestamp()), "timezone": tz_name}
            elif fmt == "human":
                result = {
                    "time": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
                    "timezone": tz_name
                }
            else:  # iso
                result = {"time": now.isoformat(), "timezone": tz_name}

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "convert_timezone":
            time_str = arguments["time"]
            from_tz_name = arguments.get("from_timezone", "UTC")
            to_tz_name = arguments["to_timezone"]

            # Parse the input time
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))

            # If no timezone info, assume from_timezone
            if dt.tzinfo is None:
                from_tz = ZoneInfo(from_tz_name)
                dt = dt.replace(tzinfo=from_tz)

            # Convert to target timezone
            to_tz = ZoneInfo(to_tz_name)
            converted = dt.astimezone(to_tz)

            result = {
                "original": {
                    "time": dt.isoformat(),
                    "timezone": from_tz_name
                },
                "converted": {
                    "time": converted.isoformat(),
                    "timezone": to_tz_name,
                    "human_readable": converted.strftime("%Y-%m-%d %H:%M:%S %Z")
                }
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "list_timezones":
            from zoneinfo import available_timezones

            region = arguments.get("region")
            all_timezones = sorted(available_timezones())

            if region:
                filtered = [tz for tz in all_timezones if tz.startswith(region)]
            else:
                filtered = all_timezones

            result = {
                "count": len(filtered),
                "timezones": filtered[:100]  # Limit to 100 to avoid huge output
            }

            if len(filtered) > 100:
                result["note"] = f"Showing first 100 of {len(filtered)} timezones. Use 'region' filter to narrow down."

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def run():
    import asyncio
    asyncio.run(main())
