from flask import render_template, request, redirect, url_for, flash, session, send_file
from app import app, db
from models import *
from forms import *
from utils import *
from datetime import datetime, date, timedelta
from sqlalchemy import or_, and_
from collections import OrderedDict

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter(
            or_(User.username == form.username.data, User.email == form.email.data)
        ).first()
        if existing_user:
            flash('Username or email already exists.', 'error')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please complete your profile.', 'success')
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        
        # Redirect to appropriate profile setup
        if user.role == 'donor':
            return redirect(url_for('donor_profile'))
        elif user.role == 'hospital':
            return redirect(url_for('hospital_profile'))
        elif user.role == 'organization':
            return redirect(url_for('organization_profile'))
        
    return render_template('auth/register.html', form=form)

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Role-based dashboard"""
    user = get_current_user()
    profile = get_user_profile(user)
    five_days_ago = datetime.utcnow() - timedelta(days=5)
    if user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif user.role == 'donor':
        return redirect(url_for('donor_dashboard'))
    elif user.role == 'hospital':
        return redirect(url_for('hospital_dashboard'))
    elif user.role == 'organization':
        return redirect(url_for('organization_dashboard'))
    
    return render_template(five_days_ago = datetime.utcnow() - timedelta(days=5))

# Donor routes
@app.route('/donor/dashboard')
@role_required(['donor'])
def donor_dashboard():
    """Donor dashboard"""
    user = get_current_user()
    profile = get_user_profile(user)
    
    # Get recent donations
    recent_donations = []
    if profile:
        recent_donations = Donation.query.filter_by(donor_id=profile.id).order_by(Donation.donation_date.desc()).limit(5).all()
    
    # Get blood requests for compatible blood types
    blood_requests = []
    if profile:
        compatible_types = get_compatible_blood_types(profile.blood_type)
        blood_requests = BloodRequest.query.filter(
            BloodRequest.blood_type.in_(compatible_types),
            BloodRequest.status == 'active'
        ).order_by(BloodRequest.requested_at.desc()).limit(5).all()
    
    # Get upcoming events
    upcoming_events = DonationEvent.query.filter(
        DonationEvent.event_date >= date.today(),
        DonationEvent.status == 'upcoming'
    ).order_by(DonationEvent.event_date.asc()).limit(5).all()
    
    return render_template('donor/dashboard.html', 
                         profile=profile, 
                         recent_donations=recent_donations,
                         blood_requests=blood_requests,
                         upcoming_events=upcoming_events)

@app.route('/donor/profile', methods=['GET', 'POST'])
@role_required(['donor'])
def donor_profile():
    """Donor profile management"""
    user = get_current_user()
    profile = get_user_profile(user)
    form = DonorProfileForm()
    
    if form.validate_on_submit():
        if profile:
            # Update existing profile
            profile.full_name = form.full_name.data
            profile.blood_type = form.blood_type.data
            profile.phone = form.phone.data
            profile.address = form.address.data
            profile.city = form.city.data
            profile.state = form.state.data
            profile.zip_code = form.zip_code.data
            profile.date_of_birth = form.date_of_birth.data
            profile.medical_conditions = form.medical_conditions.data
        else:
            # Create new profile
            profile = DonorProfile(
                user_id=user.id,
                full_name=form.full_name.data,
                blood_type=form.blood_type.data,
                phone=form.phone.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                zip_code=form.zip_code.data,
                date_of_birth=form.date_of_birth.data,
                medical_conditions=form.medical_conditions.data
            )
            db.session.add(profile)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('donor_dashboard'))
    
    # Populate form with existing data
    if profile:
        form.full_name.data = profile.full_name
        form.blood_type.data = profile.blood_type
        form.phone.data = profile.phone
        form.address.data = profile.address
        form.city.data = profile.city
        form.state.data = profile.state
        form.zip_code.data = profile.zip_code
        form.date_of_birth.data = profile.date_of_birth
        form.medical_conditions.data = profile.medical_conditions
    
    return render_template('donor/profile.html', form=form, profile=profile)

# Hospital routes
@app.route('/hospital/dashboard')
@role_required(['hospital'])
def hospital_dashboard():
    """Hospital dashboard"""
    user = get_current_user()
    profile = get_user_profile(user)
    
    # Get hospital's blood requests
    blood_requests = []
    if profile:
        blood_requests = BloodRequest.query.filter_by(hospital_id=profile.id).order_by(BloodRequest.requested_at.desc()).limit(10).all()
    
    return render_template('hospital/dashboard.html', profile=profile, blood_requests=blood_requests)

@app.route('/hospital/profile', methods=['GET', 'POST'])
@role_required(['hospital'])
def hospital_profile():
    """Hospital profile management"""
    user = get_current_user()
    profile = get_user_profile(user)
    form = HospitalProfileForm()
    
    if form.validate_on_submit():
        if profile:
            # Update existing profile
            profile.hospital_name = form.hospital_name.data
            profile.license_number = form.license_number.data
            profile.contact_person = form.contact_person.data
            profile.phone = form.phone.data
            profile.address = form.address.data
            profile.city = form.city.data
            profile.state = form.state.data
            profile.zip_code = form.zip_code.data
        else:
            # Create new profile
            profile = HospitalProfile(
                user_id=user.id,
                hospital_name=form.hospital_name.data,
                license_number=form.license_number.data,
                contact_person=form.contact_person.data,
                phone=form.phone.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                zip_code=form.zip_code.data
            )
            db.session.add(profile)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('hospital_dashboard'))
    
    # Populate form with existing data
    if profile:
        form.hospital_name.data = profile.hospital_name
        form.license_number.data = profile.license_number
        form.contact_person.data = profile.contact_person
        form.phone.data = profile.phone
        form.address.data = profile.address
        form.city.data = profile.city
        form.state.data = profile.state
        form.zip_code.data = profile.zip_code
    
    return render_template('hospital/request_blood.html', form=form, profile=profile, is_profile=True)

@app.route('/hospital/request-blood', methods=['GET', 'POST'])
@role_required(['hospital'])
def request_blood():
    """Create blood request"""
    user = get_current_user()
    profile = get_user_profile(user)
    
    if not profile:
        flash('Please complete your hospital profile first.', 'warning')
        return redirect(url_for('hospital_profile'))
    
    form = BloodRequestForm()
    if form.validate_on_submit():
        blood_request = BloodRequest(
            hospital_id=profile.id,
            blood_type=form.blood_type.data,
            units_needed=form.units_needed.data,
            urgency_level=form.urgency_level.data,
            description=form.description.data,
            needed_by=datetime.combine(form.needed_by.data, datetime.min.time())
        )
        db.session.add(blood_request)
        db.session.commit()
        
        # Notify compatible donors
        compatible_types = [form.blood_type.data]
        if form.blood_type.data != 'O-':
            compatible_types.extend(get_compatible_blood_types(form.blood_type.data))
        
        donors = DonorProfile.query.filter(
            DonorProfile.blood_type.in_(compatible_types),
            DonorProfile.is_available == True
        ).all()
        
        for donor in donors:
            create_notification(
                donor.user_id,
                f'Blood Request - {form.blood_type.data}',
                f'{profile.hospital_name} needs {form.units_needed.data} units of {form.blood_type.data} blood. Urgency: {form.urgency_level.data.title()}',
                'blood_request'
            )
        
        flash('Blood request created successfully!', 'success')
        return redirect(url_for('hospital_dashboard'))
    
    return render_template('hospital/request_blood.html', form=form, profile=profile)

# Organization routes
@app.route('/organization/dashboard')
@role_required(['organization'])
def organization_dashboard():
    """Organization dashboard"""
    user = get_current_user()
    profile = get_user_profile(user)
    
    # Get organization's events
    events = []
    if profile:
        events = DonationEvent.query.filter_by(organization_id=profile.id).order_by(DonationEvent.event_date.desc()).limit(10).all()
    
    return render_template('organization/dashboard.html', profile=profile, events=events)

@app.route('/organization/profile', methods=['GET', 'POST'])
@role_required(['organization'])
def organization_profile():
    """Organization profile management"""
    user = get_current_user()
    profile = get_user_profile(user)
    form = OrganizationProfileForm()
    
    if form.validate_on_submit():
        if profile:
            # Update existing profile
            profile.organization_name = form.organization_name.data
            profile.registration_number = form.registration_number.data
            profile.contact_person = form.contact_person.data
            profile.phone = form.phone.data
            profile.address = form.address.data
            profile.city = form.city.data
            profile.state = form.state.data
            profile.zip_code = form.zip_code.data
        else:
            # Create new profile
            profile = OrganizationProfile(
                user_id=user.id,
                organization_name=form.organization_name.data,
                registration_number=form.registration_number.data,
                contact_person=form.contact_person.data,
                phone=form.phone.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                zip_code=form.zip_code.data
            )
            db.session.add(profile)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('organization_dashboard'))
    
    # Populate form with existing data
    if profile:
        form.organization_name.data = profile.organization_name
        form.registration_number.data = profile.registration_number
        form.contact_person.data = profile.contact_person
        form.phone.data = profile.phone
        form.address.data = profile.address
        form.city.data = profile.city
        form.state.data = profile.state
        form.zip_code.data = profile.zip_code
    
    return render_template('organization/manage_donors.html', form=form, profile=profile, is_profile=True)

@app.route('/organization/manage-donors')
@role_required(['organization'])
def manage_donors():
    """Manage donors"""
    # Get all donors for display
    donors = DonorProfile.query.join(User).filter(User.is_active == True).all()
    return render_template('organization/manage_donors.html', donors=donors)

# Admin routes
@app.route('/admin/dashboard')
@role_required(['admin'])
def admin_dashboard():
    """Admin dashboard"""
    # Get system statistics
    total_users = User.query.count()
    total_donors = User.query.filter_by(role='donor').count()
    total_hospitals = User.query.filter_by(role='hospital').count()
    total_organizations = User.query.filter_by(role='organization').count()
    active_requests = BloodRequest.query.filter_by(status='active').count()
    five_days_ago = datetime.utcnow() - timedelta(days=5)
    stats = {
        'total_users': total_users,
        'total_donors': total_donors,
        'total_hospitals': total_hospitals,
        'total_organizations': total_organizations,
        'active_requests': active_requests
    }
    return render_template('admin/dashboard.html', stats=stats, five_days_ago=five_days_ago)

@app.route('/admin/manage-users')
@role_required(['admin'])
def manage_users():
    """Manage all users"""
    from datetime import datetime, timedelta
    users = User.query.order_by(User.created_at.desc()).all()
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    now = datetime.utcnow()
    return render_template('admin/manage_users.html', users=users, seven_days_ago=seven_days_ago, now=now)

@app.route('/admin/toggle-user/<int:user_id>')
@role_required(['admin'])
def toggle_user_status(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}.', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/analytics')
@role_required(['admin'])
def admin_analytics():
    from datetime import datetime, timedelta
    from collections import OrderedDict
    # Get user registrations for the last 7 days
    today = datetime.utcnow().date()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    days_str = [d.strftime('%Y-%m-%d') for d in days]
    counts = OrderedDict((d, 0) for d in days_str)
    donor_counts = OrderedDict((d, 0) for d in days_str)
    hospital_counts = OrderedDict((d, 0) for d in days_str)
    org_counts = OrderedDict((d, 0) for d in days_str)
    users = User.query.filter(User.created_at >= days[0]).all()
    for user in users:
        day = user.created_at.strftime('%Y-%m-%d')
        if day in counts:
            counts[day] += 1
            if user.role == 'donor':
                donor_counts[day] += 1
            elif user.role == 'hospital':
                hospital_counts[day] += 1
            elif user.role == 'organization':
                org_counts[day] += 1
    return render_template('admin/analytics.html', days=list(counts.keys()), counts=list(counts.values()), donor_counts=list(donor_counts.values()), hospital_counts=list(hospital_counts.values()), org_counts=list(org_counts.values()))

@app.route('/admin/blood-type-distribution')
@role_required(['admin'])
def blood_type_distribution():
    from collections import OrderedDict
    blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    counts = OrderedDict((bt, 0) for bt in blood_types)
    from models import DonorProfile
    donors = DonorProfile.query.all()
    for donor in donors:
        if donor.blood_type in counts:
            counts[donor.blood_type] += 1
    return render_template('admin/blood_type_distribution.html', blood_types=list(counts.keys()), counts=list(counts.values()))

# Search routes
@app.route('/search/donors', methods=['GET', 'POST'])
@login_required
def search_donors():
    """Search for donors"""
    form = SearchForm()
    donors = []
    
    if form.validate_on_submit():
        query = DonorProfile.query.join(User).filter(User.is_active == True)
        
        if form.blood_type.data:
            query = query.filter(DonorProfile.blood_type == form.blood_type.data)
        
        if form.city.data:
            query = query.filter(DonorProfile.city.ilike(f'%{form.city.data}%'))
        
        if form.state.data:
            query = query.filter(DonorProfile.state.ilike(f'%{form.state.data}%'))
        
        donors = query.all()
    
    return render_template('search/donors.html', form=form, donors=donors)

# Blood request response route
@app.route('/respond-to-request/<int:request_id>/<action>')
@role_required(['donor'])
def respond_to_request(request_id, action):
    """Respond to blood request"""
    user = get_current_user()
    profile = get_user_profile(user)
    
    if not profile:
        flash('Please complete your profile first.', 'warning')
        return redirect(url_for('donor_profile'))
    
    blood_request = BloodRequest.query.get_or_404(request_id)
    
    # Check if already responded
    existing_response = BloodRequestResponse.query.filter_by(
        request_id=request_id,
        donor_id=profile.id
    ).first()
    
    if existing_response:
        flash('You have already responded to this request.', 'warning')
        return redirect(url_for('donor_dashboard'))
    
    if action in ['accept', 'decline']:
        response = BloodRequestResponse(
            request_id=request_id,
            donor_id=profile.id,
            status='accepted' if action == 'accept' else 'declined'
        )
        db.session.add(response)
        db.session.commit()
        
        message = 'accepted' if action == 'accept' else 'declined'
        flash(f'You have {message} the blood request.', 'success')
    
    return redirect(url_for('donor_dashboard'))

@app.route('/download-source')
def download_source():
    """Download the complete source code"""
    return send_file('download.html')

@app.route('/blood_donation_platform_source.zip')
def download_zip():
    """Serve the ZIP file for download"""
    try:
        return send_file('blood_donation_platform_source.zip', as_attachment=True, download_name='blood_donation_platform_source.zip')
    except FileNotFoundError:
        flash('Download file not found', 'error')
        return redirect(url_for('index'))

# Create admin user route (for initial setup)
@app.route('/create-admin')
def create_admin():
    """Create initial admin user - should be removed in production"""
    existing_admin = User.query.filter_by(role='admin').first()
    if existing_admin:
        flash('Admin user already exists.', 'warning')
        return redirect(url_for('index'))
    
    admin = User(
        username='admin',
        email='admin@bloodbank.com',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    
    flash('Admin user created successfully! Username: admin, Password: admin123', 'success')
    return redirect(url_for('login'))

@app.route('/admin/donors')
@role_required(['admin'])
def admin_list_donors():
    donors = User.query.filter_by(role='donor').order_by(User.created_at.desc()).all()
    return render_template('admin/list_donors.html', donors=donors)

@app.route('/admin/hospitals')
@role_required(['admin'])
def admin_list_hospitals():
    hospitals = User.query.filter_by(role='hospital').order_by(User.created_at.desc()).all()
    return render_template('admin/list_hospitals.html', hospitals=hospitals)

@app.route('/admin/organizations')
@role_required(['admin'])
def admin_list_organizations():
    organizations = User.query.filter_by(role='organization').order_by(User.created_at.desc()).all()
    return render_template('admin/list_organizations.html', organizations=organizations)
