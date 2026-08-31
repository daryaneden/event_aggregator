from uuid import UUID

class EventNotFoundException(Exception):

    def __init__(self, event_id: UUID):
        self.event_id = event_id
        self.detail = f'Event {self.event_id} is not found'

class TicketNotFoundException(Exception):

    def __init__(self, ticket_id: UUID):
        self.detail = f"Ticket {ticket_id} not found"
        self.ticket_id = ticket_id