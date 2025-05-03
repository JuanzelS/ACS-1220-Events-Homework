"""Script to initialize the database."""
from events_app import app, db
from events_app.models import Guest, Event
import os
from datetime import datetime

with app.app_context():
    # Print the database location
    print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Delete the existing database file if it exists
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database at {db_path}")
    
    print("Creating all tables...")
    db.create_all()
    
    # Verify tables were created
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables created: {tables}")
    
    # Create sample data
    sample_event = Event(
        title="Welcome Party",
        description="Join us for a welcome celebration!",
        date_and_time=datetime.now()
    )
    
    sample_guest = Guest(
        name="John Doe",
        email="john@example.com",
        phone="555-123-4567"
    )
    
    db.session.add(sample_event)
    db.session.add(sample_guest)
    db.session.commit()
    
    # Associate the guest with the event
    sample_guest.events_attending.append(sample_event)
    db.session.commit()
    
    print("Database initialized successfully with sample data!")
    print(f"Event count: {Event.query.count()}")
    print(f"Guest count: {Guest.query.count()}")