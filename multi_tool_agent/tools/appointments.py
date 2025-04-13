import datetime

# Current date for appointments
today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)
next_week = today + datetime.timedelta(days=7)

# Common location data - reused to reduce repetition
locations = {
    'dentist': {
        'address': '123 Main St, Springfield, IL 62701',
        'coordinates': {'lat': 39.781, 'long': -89.650}
    },
    'vision': {
        'address': '456 Oak Ave, Springfield, IL 62702',
        'coordinates': {'lat': 39.776, 'long': -89.645}
    },
    'hair': {
        'address': '789 Elm Blvd, Springfield, IL 62704',
        'coordinates': {'lat': 39.792, 'long': -89.655}
    }
}

# Appointment data with clearer structure
appointments_data = [
    # Dentist appointments
    {
        'id': '1', 
        'date': today.strftime('%Y-%m-%d'), 
        'time': '10:00 AM', 
        'specialty': 'dentist', 
        'open': True,
        'address': locations['dentist']['address'],
        'coordinates': locations['dentist']['coordinates']
    },
    {
        'id': '2', 
        'date': today.strftime('%Y-%m-%d'), 
        'time': '11:00 AM', 
        'specialty': 'dentist', 
        'open': True,
        'address': locations['dentist']['address'],
        'coordinates': locations['dentist']['coordinates']
    },
    {
        'id': '3', 
        'date': tomorrow.strftime('%Y-%m-%d'), 
        'time': '11:00 AM', 
        'specialty': 'dentist', 
        'open': True,
        'address': locations['dentist']['address'],
        'coordinates': locations['dentist']['coordinates']
    },
    {
        'id': '4', 
        'date': tomorrow.strftime('%Y-%m-%d'), 
        'time': '3:00 PM', 
        'specialty': 'dentist', 
        'open': True,
        'address': locations['dentist']['address'],
        'coordinates': locations['dentist']['coordinates']
    },
    {
        'id': '5', 
        'date': next_week.strftime('%Y-%m-%d'), 
        'time': '1:00 PM', 
        'specialty': 'dentist', 
        'open': True,
        'address': locations['dentist']['address'],
        'coordinates': locations['dentist']['coordinates']
    },
    {
        'id': '6', 
        'date': next_week.strftime('%Y-%m-%d'), 
        'time': '2:00 PM', 
        'specialty': 'dentist', 
        'open': True,
        'address': locations['dentist']['address'],
        'coordinates': locations['dentist']['coordinates']
    },
    
    # Vision appointments
    {
        'id': '7', 
        'date': tomorrow.strftime('%Y-%m-%d'), 
        'time': '2:00 PM', 
        'specialty': 'vision', 
        'open': True,
        'address': locations['vision']['address'],
        'coordinates': locations['vision']['coordinates']
    },
    {
        'id': '8', 
        'date': next_week.strftime('%Y-%m-%d'), 
        'time': '2:00 PM', 
        'specialty': 'vision', 
        'open': True,
        'address': locations['vision']['address'],
        'coordinates': locations['vision']['coordinates']
    },
    {
        'id': '9', 
        'date': next_week.strftime('%Y-%m-%d'), 
        'time': '4:00 PM', 
        'specialty': 'vision', 
        'open': True,
        'address': locations['vision']['address'],
        'coordinates': locations['vision']['coordinates']
    },
    
    # Hair appointments
    {
        'id': '10', 
        'date': today.strftime('%Y-%m-%d'), 
        'time': '10:30 AM', 
        'specialty': 'hair', 
        'open': True,
        'address': locations['hair']['address'],
        'coordinates': locations['hair']['coordinates']
    },
    {
        'id': '11', 
        'date': tomorrow.strftime('%Y-%m-%d'), 
        'time': '11:00 AM', 
        'specialty': 'hair', 
        'open': True,
        'address': locations['hair']['address'],
        'coordinates': locations['hair']['coordinates']
    },
    {
        'id': '12', 
        'date': tomorrow.strftime('%Y-%m-%d'), 
        'time': '2:00 PM', 
        'specialty': 'hair', 
        'open': True,
        'address': locations['hair']['address'],
        'coordinates': locations['hair']['coordinates']
    },
    {
        'id': '13', 
        'date': next_week.strftime('%Y-%m-%d'), 
        'time': '11:00 AM', 
        'specialty': 'hair', 
        'open': True,
        'address': locations['hair']['address'],
        'coordinates': locations['hair']['coordinates']
    },
    {
        'id': '14', 
        'date': next_week.strftime('%Y-%m-%d'), 
        'time': '3:00 PM', 
        'specialty': 'hair', 
        'open': True,
        'address': locations['hair']['address'],
        'coordinates': locations['hair']['coordinates']
    }
]

def get_appointment_specialties() -> list[str]:
    """
    Gets the list of available specialties.

    Returns:
      list: a list of specialties
    Example:
        >>> get_appointment_specialties()
        ['dentist', 'vision', 'hair']
    """
    specialties = list(set([appointment['specialty'] for appointment in appointments_data]))
    return specialties

def get_available_appointments(specialty: str) -> list[dict]:
    """
    Gets the available appointments for the given specialty.
    Args:
      specialty (str): the specialty name
    Returns:
      list: a list of available appointments
    Example:
        >>> get_available_appointments('dentist')
        [{'id': '1', 'date': '2022-01-01', 'time': '10:00 AM'}, {'id': '2', 'date': '2022-01-01', 'time': '11:00 AM'}]
    """
    open_appointments = [
        { 'id': appointment['id'], 'date': appointment['date'], 'time': appointment['time'] }
        for appointment in appointments_data
        if appointment['specialty'] == specialty and appointment['open']
    ]
    return open_appointments

def get_appointment_details(appointment_id: str) -> dict:
    """
    Gets the details of the appointment with the given ID.
    Args:
      appointment_id (str): the appointment ID
    Returns:
      dict: the details of the appointment
    Example:
        >>> get_appointment_details('1')
        {'id': '1', 'date': '2022-01-01', 'time': '10:00 AM', 'specialty': 'dentist', 'open': True, 'address': '123 Main St, Springfield, IL 62701', 'coordinates': {'lat': 39.781, 'long': -89.650}}
    """
    for appointment in appointments_data:
        if appointment['id'] == appointment_id:
            return appointment
    return None

def book_appointment(appointment_id: str) -> dict:
    """
    Books the given appointment.
    Args:
      appointment_id (str): the appointment ID
    Returns:
      dict: the status of the booking
    Example:
        >>> book_appointment('1')
        {'status': 'success', 'message': 'Appointment booked successfully.'}
    """
    for appointment in appointments_data:
        if appointment['open'] and appointment['id'] == appointment_id:
            appointment['open'] = False
            return { 'status': 'success', 'message': 'Appointment booked successfully.' }
    return { 'status': 'fail', 'message': 'Appointment not available.' }

def cancel_appointment(appointment_id: str) -> dict:
    """
    Cancels the appointment with the given ID.
    Args:
      appointment_id (str): the appointment ID
    Returns:
      dict: the status of the cancellation
    Example:
        >>> cancel_appointment('1')
        {'status': 'success', 'message': 'Appointment canceled successfully.'}
    """
    for appointment in appointments_data:
        if not appointment['open'] and appointment['id'] == appointment_id:
            appointment['open'] = True
            return { 'status': 'success', 'message': 'Appointment canceled successfully.' }
    return { 'status': 'fail', 'message': 'Appointment not found.' }

def get_my_appointments() -> list[dict]:
    """
    Gets the appointments booked by the user.
    Returns:
      list: a list of booked appointments
    Example:
        >>> get_my_appointments()
        [{'id': '1', 'date': '2022-01-01', 'time': '10:00 AM', 'specialty': 'dentist'}]
    """
    my_appointments = [
        { 'id': appointment['id'], 'date': appointment['date'], 'time': appointment['time'], 'specialty': appointment['specialty'] }
        for appointment in appointments_data
        if not appointment['open']
    ]
    return my_appointments