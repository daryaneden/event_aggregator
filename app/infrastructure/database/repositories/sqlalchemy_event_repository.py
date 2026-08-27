from datetime import date, time, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.infrastructure.database.models.event import EventModel
from app.infrastructure.database.models.place import PlaceModel
from app.domain.entities.event import Event
from app.domain.entities.place import Place


class SqlAlchemyEventRepository:

    def __init__(self, session):
        self.session = session

    async def save(self, event: Event) -> None: 
        place = await self.session.get(PlaceModel, event.place.id) 

        if place is None: 
            place = PlaceModel(id=event.place.id, 
                               name=event.place.name, 
                               city=event.place.city, 
                               address=event.place.address, 
                               seats_pattern=event.place.seats_pattern) 

            self.session.add(place)
            await self.session.flush() 

        else: 
            place.name = event.place.name
            place.city = event.place.city 
            place.address = event.place.address 
            place.seats_pattern = event.place.seats_pattern 

        event_model = await self.session.get( EventModel, event.id) 

        if event_model is None: 
            event_model = EventModel(id=event.id, 
                                     name=event.name, 
                                     place_id=event.place.id, 
                                     event_time=event.event_time, 
                                     registration_deadline=event.registration_deadline, 
                                     status=event.status, 
                                     number_of_visitors=event.number_of_visitors, 
                                     changed_at=event.changed_at, 
                                     created_at=event.created_at, 
                                     status_changed_at=event.status_changed_at) 

            self.session.add(event_model) 

        else: 
            event_model.name = event.name 
            event_model.place_id = event.place.id 
            event_model.event_time = event.event_time 
            event_model.registration_deadline = event.registration_deadline 
            event_model.status = event.status 
            event_model.number_of_visitors = event.number_of_visitors 
            event_model.changed_at = event.changed_at 
            event_model.created_at = event.created_at 
            event_model.status_changed_at = event.status_changed_at

    async def get_events(
    self,
    date_from: date | None,
    page: int,
    page_size: int,
) -> tuple[list[Event], int]:

        query = (
            select(EventModel)
            .options(selectinload(EventModel.place))
        )

        if date_from is not None:
            query = query.where(
                EventModel.event_time >= date_from
            )

        count_query = select(
            func.count()
        ).select_from(query.subquery())

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = (
            query
            .order_by(EventModel.event_time)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(query)

        event_models = result.scalars().all()

        events = [
            self._to_domain(event_model)
            for event_model in event_models
        ]

        return events, total

    def _to_domain(self, model: EventModel) -> Event:
        return Event(
            id=model.id,
            name=model.name,
            place=Place(
                id=model.place.id,
                name=model.place.name,
                city=model.place.city,
                address=model.place.address,
                seats_pattern=model.place.seats_pattern,
            ),
            event_time=model.event_time,
            registration_deadline=model.registration_deadline,
            status=model.status,
            number_of_visitors=model.number_of_visitors,
            changed_at=model.changed_at,
            created_at=model.created_at,
            status_changed_at=model.status_changed_at,
        )

    async def get_by_id(self, event_id: UUID) -> Event | None:
        query = (
            select(EventModel)
            .options(selectinload(EventModel.place))
            .where(EventModel.id == event_id)
        )

        result = await self.session.execute(query)

        event_model = result.scalar_one_or_none()

        if event_model is None:
            return None

        return self._to_domain(event_model)