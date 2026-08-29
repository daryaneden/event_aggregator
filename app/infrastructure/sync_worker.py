import asyncio
import logging

from app.application.use_cases.sync_events import SyncEventsUseCase

logger = logging.getLogger(__name__)


async def sync_worker(use_case: SyncEventsUseCase) -> None:
    while True:
        try:
            logger.info("Starting scheduled events synchronization")

            await use_case.execute()

            logger.info("Scheduled events synchronization completed")

        except Exception:
            logger.exception("Scheduled events synchronization failed")

        # await asyncio.sleep(24 * 60 * 60)
        await asyncio.sleep(10)