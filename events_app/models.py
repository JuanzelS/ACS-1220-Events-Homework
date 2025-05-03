"""Create database models to represent tables."""
from events_app import db
from sqlalchemy.orm import backref
import enum

# Define EventType enum for the stretch challenge
class EventType(enum.Enum):
    PARTY = 'Party'
    STUDY = 'Study'
    NETWORKING = 'Networking'
    OTHER = 'Other'

# Create association table for many-to-many relationship
guest_event_table = db.Table('guest_event',
    db.Column('guest_id', db.Integer, db.ForeignKey('guest.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class Guest(db.Model):
    """Guest model representing event attendees."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    events_attending = db.relationship(
        'Event', 
        secondary=guest_event_table,
        back_populates='guests'
    )
    
    def __repr__(self):
        return f'<Guest: {self.name}>'

class Event(db.Model):
    """Event model representing scheduled events."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    date_and_time = db.Column(db.DateTime, nullable=False)
    # STRETCH CHALLENGE: event_type as Enum column
    event_type = db.Column(db.Enum(EventType), default=EventType.OTHER)
    guests = db.relationship(
        'Guest', 
        secondary=guest_event_table,
        back_populates='events_attending'
    )
    
    def __repr__(self):
        return f'<Event: {self.title}>'