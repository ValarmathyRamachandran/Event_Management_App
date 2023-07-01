# Event Management App

This repository contains the API service for an Event Management app developed using Python Django.

The Event Management app provides functionality for two types of users:

## User Functionalities

Users of the Event Management app can perform the following actions:
- View Events: Users can browse and view all available events.
- Book Ticket: Users can book tickets for events.
- View Ticket: Users can view their booked tickets.
- View Registered Events: Users can see a list of all events they have registered for, sorted chronologically.

## Admin Functionalities

Administrators of the Event Management app have additional capabilities:
- Create Event: Admins can create new events.
- List Events: Admins can view a list of all existing events.
- Update Events: Admins can update the details of existing events.
- View Event Summary: Admins can view a summary of an event, including information such as the number of registered users and available seats.

## Event Capabilities

Events in the Event Management app possess the following features:
- Max Available Seats: Admins can set the maximum number of available seats for an event.
- Booking Open Window: Users can book tickets for events only within a specific time window defined by the admin.


# Event Management app API

Follow these steps to set up and run the Event Management app API:

## Clone the repository:
git clone https://github.com/ValarmathyRamachandran/event_management_app.git


## Install the necessary dependencies:
pip install -r requirements.txt


## Set up the database:
python manage.py migrate


## Start the development server:
python manage.py runserver


The API service should now be up and running at [http://localhost:8000/](http://localhost:8000/)

## API Endpoints

The Event Management app API provides the following endpoints:

Refer swagger urls: [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)

