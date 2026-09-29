from app.application.interfaces.notification_client import NotificationClient
from app.application.interfaces.uow_factory import UnitOfWorkFactory


class ProcessOutboxUseCase:

    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        notification_client: NotificationClient,
    ):
        self.uow_factory = uow_factory
        self.notification_client = notification_client

    async def execute(self) -> None:

        async with self.uow_factory() as uow:
            messages = await uow.outbox_repository.get_pending()

        print("PENDING MESSAGES:", len(messages))
        
        for message in messages:

            if message.event_type != "ticket_registered":
                continue

            payload = message.payload

            print("PROCESSING OUTBOX:", message.id)

            await self.notification_client.send_notification(
                message=(
                    "Вы успешно зарегистрированы "
                    "на мероприятие"
                ),
                reference_id=payload["ticket_id"],
                idempotency_key=str(message.id),
            )

            print("NOTIFICATION SENT:", message.id)

            async with self.uow_factory() as uow:

                print("MARKING AS SENT:", message.id)

                await uow.outbox_repository.mark_as_sent(
                    message.id,
                )

            print("OUTBOX MARKED AS SENT:", message.id)