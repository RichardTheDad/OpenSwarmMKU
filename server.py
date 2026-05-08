# FastAPI entry point — run with: python server.py

import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

from swarm import create_agency
from agency_swarm.integrations.fastapi import run_fastapi


if __name__ == "__main__":
    run_fastapi(
        agencies={
            "open-swarm": create_agency,
        },
        host="127.0.0.1",   # localhost only — not exposed to LAN/network
        port=8080,
        enable_logging=True,
        cors_origins=[
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            "http://localhost:3000",   # Agency Swarm UI dev server if used
        ],
        allowed_local_file_dirs=[
            "./uploads",
        ],
    )
