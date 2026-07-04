import asyncio
import sys
from pathlib import Path


from src.infrastructure.database.session import create_tables


async def main()->None:
    try:
        await create_tables()
    except Exception as e:
        sys.exit(1)

if __name__=="__main__":
    asyncio.run(main())