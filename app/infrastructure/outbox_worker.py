import asyncio
import logging

from app.application.use_cases.proccess_outbox_use_case import ProcessOutboxUseCase

logger = logging.getLogger(__name__)

async def outbox_worker(use_case: ProcessOutboxUseCase) -> None:
    while True:
        try:
            logger.info("Starting outbox processing")

            await use_case.execute()

            logger.info("Outbox processing completed")

        except Exception:
            logger.exception("Outbox processing failed")

        await asyncio.sleep(5)