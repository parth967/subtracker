"""
InviteMe - Beautiful Invitation & RSVP Platform

A modern Flask web application for creating stunning invitations
and managing RSVPs with beautiful designs and seamless user experience.

Features:
- Create beautiful invitations with multiple templates
- Share invitations via link or QR code
- Manage RSVPs with guest details
- Real-time RSVP tracking
- Mobile-responsive design
- Free to use platform

Author: InviteMe Team
License: MIT
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets
import string
from urllib.parse import quote
import qrcode
import io
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.production' if os.path.exists('.env.production') else '.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///inviteme.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True,
}

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Extended Template Gallery with 15+ Beautiful Templates
INVITATION_TEMPLATES = {
    'classic': {
        'name': 'Classic Elegance',
        'description': 'Timeless and sophisticated design perfect for formal events',
        'category': 'formal',
        'colors': ['#2c3e50', '#ecf0f1', '#3498db'],
        'preview': 'classic-preview.jpg'
    },
    'modern': {
        'name': 'Modern Minimalist',
        'description': 'Clean, contemporary design with bold typography',
        'category': 'modern',
        'colors': ['#34495e', '#ffffff', '#e74c3c'],
        'preview': 'modern-preview.jpg'
    },
    'floral': {
        'name': 'Floral Garden',
        'description': 'Beautiful botanical elements perfect for spring events',
        'category': 'nature',
        'colors': ['#27ae60', '#f8c471', '#e8f5e8'],
        'preview': 'floral-preview.jpg'
    },
    'vintage': {
        'name': 'Vintage Charm',
        'description': 'Nostalgic design with classic typography and ornaments',
        'category': 'vintage',
        'colors': ['#8b4513', '#f4e4bc', '#d2691e'],
        'preview': 'vintage-preview.jpg'
    },
    'festive': {
        'name': 'Festive Celebration',
        'description': 'Vibrant and joyful design for parties and celebrations',
        'category': 'party',
        'colors': ['#ff6b6b', '#4ecdc4', '#45b7d1'],
        'preview': 'festive-preview.jpg'
    },
    'corporate': {
        'name': 'Corporate Professional',
        'description': 'Professional design perfect for business events',
        'category': 'business',
        'colors': ['#2c3e50', '#3498db', '#ecf0f1'],
        'preview': 'corporate-preview.jpg'
    },
    'luxury': {
        'name': 'Luxury Gold',
        'description': 'Elegant gold accents for premium events',
        'category': 'luxury',
        'colors': ['#000000', '#ffd700', '#ffffff'],
        'preview': 'luxury-preview.jpg'
    },
    'ocean': {
        'name': 'Ocean Breeze',
        'description': 'Refreshing blue tones inspired by the sea',
        'category': 'nature',
        'colors': ['#0077be', '#87ceeb', '#f0f8ff'],
        'preview': 'ocean-preview.jpg'
    },
    'sunset': {
        'name': 'Sunset Romance',
        'description': 'Warm sunset colors perfect for romantic events',
        'category': 'romantic',
        'colors': ['#ff6b35', '#f7931e', '#ffb347'],
        'preview': 'sunset-preview.jpg'
    },
    'neon': {
        'name': 'Neon Party',
        'description': 'Electric neon colors for energetic celebrations',
        'category': 'party',
        'colors': ['#ff0080', '#00ff80', '#8000ff'],
        'preview': 'neon-preview.jpg'
    },
    'forest': {
        'name': 'Forest Green',
        'description': 'Natural green tones for outdoor events',
        'category': 'nature',
        'colors': ['#228b22', '#90ee90', '#f0fff0'],
        'preview': 'forest-preview.jpg'
    },
    'royal': {
        'name': 'Royal Purple',
        'description': 'Majestic purple design for elegant occasions',
        'category': 'luxury',
        'colors': ['#663399', '#dda0dd', '#f8f0ff'],
        'preview': 'royal-preview.jpg'
    },
    'cherry': {
        'name': 'Cherry Blossom',
        'description': 'Delicate pink cherry blossom theme',
        'category': 'nature',
        'colors': ['#ffb7c5', '#ffc0cb', '#fff0f5'],
        'preview': 'cherry-preview.jpg'
    },
    'midnight': {
        'name': 'Midnight Glamour',
        'description': 'Sophisticated dark theme with silver accents',
        'category': 'luxury',
        'colors': ['#191970', '#c0c0c0', '#f5f5f5'],
        'preview': 'midnight-preview.jpg'
    },
    'tropical': {
        'name': 'Tropical Paradise',
        'description': 'Vibrant tropical colors for summer events',
        'category': 'nature',
        'colors': ['#ff7f50', '#32cd32', '#ffd700'],
        'preview': 'tropical-preview.jpg'
    },
    'rustic': {
        'name': 'Rustic Barn',
        'description': 'Warm rustic design perfect for country weddings',
        'category': 'rustic',
        'colors': ['#8b4513', '#daa520', '#f5deb3'],
        'preview': 'rustic-preview.jpg'
    },
    'galaxy': {
        'name': 'Galaxy Dreams',
        'description': 'Cosmic theme with stars and nebula colors',
        'category': 'modern',
        'colors': ['#191970', '#9370db', '#4169e1'],
        'preview': 'galaxy-preview.jpg'
    },
    'autumn': {
        'name': 'Autumn Leaves',
        'description': 'Warm autumn colors perfect for fall events',
        'category': 'nature',
        'colors': ['#ff8c00', '#dc143c', '#ffd700'],
        'preview': 'autumn-preview.jpg'
    }
}

# Database Models
class User(UserMixin, db.Model):
    """User authentication model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    invitations = db.relationship('Invitation', backref='creator', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Invitation(db.Model):
    """Main invitation model"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Info
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)  # wedding, birthday, party, etc.
    
    # Event Details
    event_date = db.Column(db.DateTime, nullable=False)
    event_time = db.Column(db.String(20))
    venue_name = db.Column(db.String(200))
    venue_address = db.Column(db.Text)
    
    # Host Information
    host_name = db.Column(db.String(100), nullable=False)
    host_email = db.Column(db.String(120))
    host_phone = db.Column(db.String(20))
    
    # Invitation Settings
    template_id = db.Column(db.String(50), default='classic')
    color_scheme = db.Column(db.String(20), default='blue')
    custom_message = db.Column(db.Text)
    
    # Sharing & Privacy
    invitation_code = db.Column(db.String(20), unique=True, nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    requires_approval = db.Column(db.Boolean, default=False)
    max_guests = db.Column(db.Integer)
    
    # User Association
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rsvps = db.relationship('RSVP', backref='invitation', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Invitation {self.title}>'
    
    @property
    def total_rsvps(self):
        return len(self.rsvps)
    
    @property
    def attending_count(self):
        return len([rsvp for rsvp in self.rsvps if rsvp.status == 'attending'])
    
    @property
    def not_attending_count(self):
        return len([rsvp for rsvp in self.rsvps if rsvp.status == 'not_attending'])
    
    @property
    def maybe_count(self):
        return len([rsvp for rsvp in self.rsvps if rsvp.status == 'maybe'])
    
    @property
    def share_url(self):
        return url_for('view_invitation', code=self.invitation_code, _external=True)

class RSVP(db.Model):
    """RSVP responses model"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Guest Information
    guest_name = db.Column(db.String(100), nullable=False)
    guest_email = db.Column(db.String(120))
    guest_phone = db.Column(db.String(20))
    
    # RSVP Details
    status = db.Column(db.String(20), nullable=False)  # attending, not_attending, maybe
    guest_count = db.Column(db.Integer, default=1)
    dietary_requirements = db.Column(db.Text)
    special_requests = db.Column(db.Text)
    message = db.Column(db.Text)
    
    # Metadata
    invitation_id = db.Column(db.Integer, db.ForeignKey('invitation.id'), nullable=False)
    responded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RSVP {self.guest_name} - {self.status}>'

# Helper Functions
def generate_invitation_code():
    """Generate a unique invitation code"""
    while True:
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        if not Invitation.query.filter_by(invitation_code=code).first():
            return code

def generate_qr_code(url):
    """Generate QR code for invitation URL"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 string
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Main Routes
@app.route('/')
def home():
    """Homepage with invitation templates"""
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with their invitations"""
    invitations = Invitation.query.filter_by(user_id=current_user.id).order_by(Invitation.created_at.desc()).all()
    
    # Calculate statistics
    total_invitations = len(invitations)
    total_rsvps = sum(len(inv.rsvps) for inv in invitations)
    total_attending = sum(inv.attending_count for inv in invitations)
    
    stats = {
        'total_invitations': total_invitations,
        'total_rsvps': total_rsvps,
        'total_attending': total_attending,
        'recent_invitations': invitations[:5]
    }
    
    return render_template('dashboard.html', invitations=invitations, stats=stats)

@app.route('/create')
@login_required
def create_invitation():
    """Create new invitation form"""
    return render_template('create_invitation.html')

@app.route('/create', methods=['POST'])
@login_required
def create_invitation_post():
    """Handle invitation creation"""
    try:
        # Generate unique invitation code
        invitation_code = generate_invitation_code()
        
        # Parse event date and time
        event_date_str = request.form['event_date']
        event_time_str = request.form.get('event_time', '')
        
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d')
        if event_time_str:
            time_parts = event_time_str.split(':')
            event_date = event_date.replace(hour=int(time_parts[0]), minute=int(time_parts[1]))
        
        # Create invitation
        invitation = Invitation(
            title=request.form['title'],
            description=request.form.get('description', ''),
            event_type=request.form['event_type'],
            event_date=event_date,
            event_time=event_time_str,
            venue_name=request.form.get('venue_name', ''),
            venue_address=request.form.get('venue_address', ''),
            host_name=request.form['host_name'],
            host_email=request.form.get('host_email', ''),
            host_phone=request.form.get('host_phone', ''),
            template_id=request.form.get('template_id', 'classic'),
            color_scheme=request.form.get('color_scheme', 'blue'),
            custom_message=request.form.get('custom_message', ''),
            max_guests=int(request.form['max_guests']) if request.form.get('max_guests') else None,
            invitation_code=invitation_code,
            user_id=current_user.id  # Associate with current user
        )
        
        db.session.add(invitation)
        db.session.commit()
        
        flash('Invitation created successfully!', 'success')
        return redirect(url_for('manage_invitation', code=invitation_code))
        
    except Exception as e:
        flash(f'Error creating invitation: {str(e)}', 'error')
        return redirect(url_for('create_invitation'))

@app.route('/invitation/<code>')
def view_invitation(code):
    """View invitation page for guests"""
    invitation = Invitation.query.filter_by(invitation_code=code).first_or_404()
    return render_template('view_invitation.html', invitation=invitation)

@app.route('/invitation/<code>/rsvp', methods=['POST'])
def submit_rsvp(code):
    """Handle RSVP submission"""
    invitation = Invitation.query.filter_by(invitation_code=code).first_or_404()
    
    try:
        # Check if guest already RSVPed
        existing_rsvp = RSVP.query.filter_by(
            invitation_id=invitation.id,
            guest_email=request.form.get('guest_email')
        ).first()
        
        if existing_rsvp:
            # Update existing RSVP
            existing_rsvp.guest_name = request.form['guest_name']
            existing_rsvp.guest_phone = request.form.get('guest_phone', '')
            existing_rsvp.status = request.form['status']
            existing_rsvp.guest_count = int(request.form.get('guest_count', 1))
            existing_rsvp.dietary_requirements = request.form.get('dietary_requirements', '')
            existing_rsvp.special_requests = request.form.get('special_requests', '')
            existing_rsvp.message = request.form.get('message', '')
            existing_rsvp.responded_at = datetime.utcnow()
        else:
            # Create new RSVP
            rsvp = RSVP(
                guest_name=request.form['guest_name'],
                guest_email=request.form.get('guest_email', ''),
                guest_phone=request.form.get('guest_phone', ''),
                status=request.form['status'],
                guest_count=int(request.form.get('guest_count', 1)),
                dietary_requirements=request.form.get('dietary_requirements', ''),
                special_requests=request.form.get('special_requests', ''),
                message=request.form.get('message', ''),
                invitation_id=invitation.id
            )
            db.session.add(rsvp)
        
        db.session.commit()
        
        status_messages = {
            'attending': 'Great! We\'re excited to see you at the event!',
            'not_attending': 'Thanks for letting us know. You\'ll be missed!',
            'maybe': 'Thanks for your response. Hope you can make it!'
        }
        
        flash(status_messages.get(request.form['status'], 'Thank you for your response!'), 'success')
        return redirect(url_for('view_invitation', code=code))
        
    except Exception as e:
        flash(f'Error submitting RSVP: {str(e)}', 'error')
        return redirect(url_for('view_invitation', code=code))

@app.route('/manage/<code>')
@login_required
def manage_invitation(code):
    """Manage invitation dashboard"""
    invitation = Invitation.query.filter_by(
        invitation_code=code, 
        user_id=current_user.id  # Ensure user can only manage their own invitations
    ).first_or_404()
    
    # Generate QR code
    qr_code = generate_qr_code(invitation.share_url)
    
    return render_template('manage_invitation.html', invitation=invitation, qr_code=qr_code)

@app.route('/api/invitation/<code>/stats')
@login_required
def invitation_stats(code):
    """API endpoint for invitation statistics"""
    invitation = Invitation.query.filter_by(
        invitation_code=code,
        user_id=current_user.id  # Ensure user can only access their own stats
    ).first_or_404()
    
    return jsonify({
        'total_rsvps': invitation.total_rsvps,
        'attending': invitation.attending_count,
        'not_attending': invitation.not_attending_count,
        'maybe': invitation.maybe_count,
        'rsvps': [{
            'guest_name': rsvp.guest_name,
            'status': rsvp.status,
            'guest_count': rsvp.guest_count,
            'responded_at': rsvp.responded_at.strftime('%Y-%m-%d %H:%M')
        } for rsvp in invitation.rsvps]
    })

@app.route('/templates')
def template_gallery():
    """Template gallery page"""
    return render_template('template_gallery.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)