from dotenv import load_dotenv

load_dotenv()

from fhir_server.mcp_server import mcp  # noqa: E402


if __name__ == "__main__":
    mcp.run()
