from functools import wraps
from flask import session, redirect, url_for, flash
from models import User, DonorProfile, HospitalProfile, OrganizationProfile, Notification    #modification
from datetime import datetime, timedelta


def login_required(f):
    """Decorator to require login for routes"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def role_required(roles):
    """Decorator to require specific roles for routes"""

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))

            user = User.query.get(session['user_id'])
            if not user or user.role not in roles:
                flash('You do not have permission to access this page.',
                      'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def get_current_user():
    """Get the current logged-in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


def get_user_profile(user):
    """Get the profile for the current user based on their role"""
    if user.role == 'donor':
        return DonorProfile.query.filter_by(user_id=user.id).first()
    elif user.role == 'hospital':
        return HospitalProfile.query.filter_by(user_id=user.id).first()
    elif user.role == 'organization':
        return OrganizationProfile.query.filter_by(user_id=user.id).first()
    return None


def can_donate(donor_profile):
    """Check if a donor is eligible to donate (last donation > 56 days ago)"""
    if not donor_profile.last_donation_date:
        return True

    days_since_last_donation = (datetime.now().date() -
                                donor_profile.last_donation_date).days
    return days_since_last_donation >= 56


def create_notification(user_id, title, message, notification_type='system'):
    """Create a new notification for a user"""
    notification = Notification(user_id=user_id,
                                title=title,
                                message=message,
                                notification_type=notification_type)
    from app import db
    db.session.add(notification)
    db.session.commit()


def get_compatible_blood_types(blood_type):
    """Get compatible blood types for transfusion"""
    compatibility = {
        'A+': ['A+', 'A-', 'O+', 'O-'],
        'A-': ['A-', 'O-'],
        'B+': ['B+', 'B-', 'O+', 'O-'],
        'B-': ['B-', 'O-'],
        'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'AB-': ['A-', 'B-', 'AB-', 'O-'],
        'O+': ['O+', 'O-'],
        'O-': ['O-']
    }
    return compatibility.get(blood_type, [])


def get_blood_type_urgency_score(blood_type):
    """Get urgency score for blood types (rarer types get higher scores)"""
    scores = {
        'AB-': 8,
        'AB+': 7,
        'B-': 6,
        'A-': 5,
        'O-': 4,
        'B+': 3,
        'A+': 2,
        'O+': 1
    }
    return scores.get(blood_type, 1)


def format_urgency_level(urgency):
    """Format urgency level with appropriate styling"""
    colors = {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger',
        'critical': 'dark'
    }
    return colors.get(urgency, 'secondary')


def calculate_age(birth_date):
    """Calculate age from birth date"""
    today = datetime.now().date()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day))
