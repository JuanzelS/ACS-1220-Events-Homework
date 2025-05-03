"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest
# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)

##########################################
# Routes
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""
    # Get all events and send to the template
    events = Event.query.all()
    return render_template('index.html', events=events)


@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')
        
        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            return render_template('create.html',
                error='Incorrect datetime format! Please try again.')
        
        # Create a new event with the given title, description, & datetime
        new_event = Event(
            title=new_event_title,
            description=new_event_description,
            date_and_time=date_and_time
        )
        
        # Add and commit to the database
        db.session.add(new_event)
        db.session.commit()
        
        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')


@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""
    # Get the event with the given id and send to the template
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)


@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    # Get the event with the given id from the database
    event = Event.query.get_or_404(event_id)
    
    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')
    
    if is_returning_guest:
        # Look up the guest by name
        guest = Guest.query.filter_by(name=guest_name).first()
        
        # If the guest doesn't exist, render template with error
        if not guest:
            return render_template(
                'event_detail.html',
                event=event,
                error='No guest with that name was found. Please try again or register as a new guest.'
            )
        
        # If the guest does exist, add the event to their events_attending
        if event not in guest.events_attending:
            guest.events_attending.append(event)
            db.session.commit()
    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')
        
        # Create a new guest and add the event to their events_attending
        new_guest = Guest(
            name=guest_name,
            email=guest_email,
            phone=guest_phone
        )
        
        # Associate the guest with the event
        new_guest.events_attending.append(event)
        
        # Add and commit to the database
        db.session.add(new_guest)
        db.session.commit()
        
    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id))


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    """Show a single guest and their events."""
    # Get the guest with the given id and send to the template
    guest = Guest.query.get_or_404(guest_id)
    return render_template('guest_detail.html', guest=guest)