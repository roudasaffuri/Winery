from datetime import datetime
from flask import session

def inject_current_year():
    """Inject the current year, username and user-email into templates."""
    return {
        'current_year': datetime.now().year,
        'username': session.get('username', None), # Get username from session
        'useremail': session.get('useremail',  None)  # Get username from session
    }