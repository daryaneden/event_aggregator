from collections.abc import AsyncIterator
from datetime import datetime

from app.application.interfaces.event_provider import EventsProvider
from app.domain.entities.event import Event


class EventsPaginator:

    def __init__(self, provider: EventsProvider, changed_at: datetime):
        self.provider = provider
        self.changed_at = changed_at

    async def __aiter__(self) -> AsyncIterator[Event]:
        url = None

        while True:

            page = await self.provider.get_events_page(changed_at=self.changed_at, url=url)

            for event in page.events:
                yield event

            if page.next_url is None:
                break

            url = page.next_url
