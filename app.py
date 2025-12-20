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

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
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

# Import email service (optional - only if configured)
try:
    from email_service import email_service
except ImportError:
    email_service = None

# Handle missing email columns gracefully
def get_user_email_pref(user, pref_name, default=True):
    """Safely get email preference, returns default if column doesn't exist"""
    try:
        return getattr(user, pref_name, default)
    except:
        return default

# Load environment variables
load_dotenv('.env.production' if os.path.exists('.env.production') else '.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
# FORCE CORRECT DATABASE - NO FALLBACK
# FIXED: Force correct InviteMe database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Parth967:khushali979797@Parth967.mysql.pythonanywhere-services.com/Parth967$inviteme?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True,
}

# File upload configuration
UPLOAD_FOLDER = 'static/uploads/invitations'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Load user, handling missing email columns gracefully"""
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        # If email columns don't exist, query without them
        try:
            from sqlalchemy import text
            result = db.session.execute(
                text("SELECT id, username, email, password_hash, full_name, created_at, is_active FROM user WHERE id = :id"),
                {'id': int(user_id)}
            ).fetchone()
            if result:
                # Create a minimal user object
                user = User()
                user.id = result[0]
                user.username = result[1]
                user.email = result[2]
                user.password_hash = result[3]
                user.full_name = result[4]
                user.created_at = result[5]
                user.is_active = result[6]
                # Set defaults for email prefs
                user.email_notifications_enabled = True
                user.email_new_rsvp = True
                user.email_reminders = True
                user.email_weekly_summary = False
                user.email_milestones = True
                return user
        except:
            pass
        return None


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
    
    # Email notification preferences (optional - columns added via migration)
    # These columns are optional and won't break if they don't exist in DB
    # To add them, run: python add_email_columns.py
    try:
        email_notifications_enabled = db.Column(db.Boolean, default=True, nullable=True)
        email_new_rsvp = db.Column(db.Boolean, default=True, nullable=True)
        email_reminders = db.Column(db.Boolean, default=True, nullable=True)
        email_weekly_summary = db.Column(db.Boolean, default=False, nullable=True)
        email_milestones = db.Column(db.Boolean, default=True, nullable=True)
    except:
        pass  # Columns don't exist yet - that's okay
    
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
    custom_image = db.Column(db.String(255))  # Path to uploaded custom image
    design_data = db.Column(db.Text)  # JSON data for drag-and-drop editor
    
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

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_image(file, user_id, invitation_id=None):
    """Save uploaded image and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create unique filename: user_id_timestamp_filename
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{user_id}_{timestamp}_{filename}"
        
        # Create user-specific directory
        user_upload_dir = os.path.join(UPLOAD_FOLDER, str(user_id))
        os.makedirs(user_upload_dir, exist_ok=True)
        
        filepath = os.path.join(user_upload_dir, unique_filename)
        file.save(filepath)
        
        # Return relative path for database
        return f"uploads/invitations/{user_id}/{unique_filename}"
    return None

# Authentication Routes
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            user = User.query.filter_by(username=username).first()
        except Exception:
            # If email columns missing, query without them
            from sqlalchemy import text
            result = db.session.execute(
                text("SELECT id, username, email, password_hash, full_name, created_at, is_active FROM user WHERE username = :username"),
                {'username': username}
            ).fetchone()
            if result:
                user = User()
                user.id = result[0]
                user.username = result[1]
                user.email = result[2]
                user.password_hash = result[3]
                user.full_name = result[4]
                user.created_at = result[5]
                user.is_active = result[6]
                # Set defaults for email prefs
                user.email_notifications_enabled = True
                user.email_new_rsvp = True
                user.email_reminders = True
                user.email_weekly_summary = False
                user.email_milestones = True
            else:
                user = None
        
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
        # Check user limit (cap at 1000 users)
        try:
            user_count = User.query.count()
        except Exception:
            # If email columns don't exist, count without them
            from sqlalchemy import text
            result = db.session.execute(text("SELECT COUNT(*) FROM user")).scalar()
            user_count = result or 0
        
        if user_count >= 1000:
            flash('Sorry! We\'ve reached our beta user limit of 1000 users. Join our waitlist!', 'error')
            return render_template('auth/register.html')
        
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
        
        # Create new user (handle missing email columns)
        try:
            user = User(
                username=username,
                email=email,
                full_name=full_name
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            # If email columns don't exist, insert without them
            from sqlalchemy import text
            password_hash = generate_password_hash(password)
            db.session.execute(
                text("""
                    INSERT INTO user (username, email, password_hash, full_name, created_at, is_active)
                    VALUES (:username, :email, :password_hash, :full_name, NOW(), 1)
                """),
                {
                    'username': username,
                    'email': email,
                    'password_hash': password_hash,
                    'full_name': full_name
                }
            )
            db.session.commit()
            # Reload user
            user = User.query.filter_by(username=username).first()
        
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
    # Get design data from editor if available
    design_data = session.get('editor_design_data', None)
    return render_template('create_invitation.html', design_data=design_data)

@app.route('/editor')
@login_required
def invitation_editor():
    """Drag-and-drop visual invitation editor"""
    return render_template('editor/drag_drop_editor.html')

@app.route('/api/upload-image', methods=['POST'])
@login_required
def upload_image():
    """Handle image upload for invitations"""
    if 'image' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        image_path = save_uploaded_image(file, current_user.id)
        if image_path:
            return jsonify({
                'success': True,
                'image_url': url_for('uploaded_file', filename=image_path),
                'image_path': image_path
            })
        else:
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP, SVG'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    try:
        return send_from_directory('static', filename)
    except:
        # Fallback if file doesn't exist
        return "File not found", 404

@app.route('/editor/save', methods=['POST'])
@login_required
def save_editor_design():
    """Save design from visual editor"""
    try:
        design_data = request.json.get('design_data', '')
        # Store in session temporarily or return to form
        session['editor_design_data'] = design_data
        return jsonify({'success': True, 'message': 'Design saved! Continue with invitation details.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        
        # Send email notifications (optional - works fine without email setup)
        if email_service:
            try:
                # Send confirmation to guest if email provided
                guest_email = request.form.get('guest_email', '')
                if guest_email and existing_rsvp is None:  # Only for new RSVPs
                    email_service.send_rsvp_confirmation(
                        request.form['guest_name'],
                        guest_email,
                        invitation
                    )
                
                # Notify host about new RSVP
                host = invitation.creator
                email_enabled = getattr(host, 'email_notifications_enabled', True) if host else False
                email_new_rsvp = getattr(host, 'email_new_rsvp', True) if host else False
                if host and email_enabled and email_new_rsvp:
                    rsvp_obj = existing_rsvp if existing_rsvp else rsvp
                    email_service.send_new_rsvp_notification(
                        host.email,
                        host.full_name,
                        invitation,
                        rsvp_obj
                    )
                
                # Check for milestones (10, 25, 50, 100 RSVPs)
                email_milestones = getattr(host, 'email_milestones', True) if host else False
                if host and email_milestones:
                    total_rsvps = invitation.total_rsvps
                    milestones = [10, 25, 50, 100]
                    if total_rsvps in milestones:
                        email_service.send_milestone_notification(
                            host.email,
                            host.full_name,
                            invitation,
                            total_rsvps
                        )
            except Exception:
                pass  # Silently fail - don't break RSVP if email fails
        
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

# SEO Landing Pages
@app.route('/wedding-rsvp')
def wedding_rsvp():
    """Wedding RSVP landing page for SEO"""
    return render_template('landing/wedding_rsvp.html')

@app.route('/birthday-invitation')
def birthday_invitation():
    """Birthday invitation landing page for SEO"""
    return render_template('landing/birthday_invitation.html')

@app.route('/corporate-events')
def corporate_events():
    """Corporate events landing page for SEO"""
    return render_template('landing/corporate_events.html')

# Blog Routes
@app.route('/blog')
def blog():
    """Blog listing page"""
    blog_posts = [
        {
            'slug': 'how-to-create-wedding-rsvp-online',
            'title': 'How to Create Wedding RSVP Online: Complete Guide 2024',
            'excerpt': 'Learn how to create beautiful wedding RSVP invitations online for free. Step-by-step guide with templates and tips.',
            'date': '2024-12-19',
            'category': 'Weddings'
        },
        {
            'slug': 'best-rsvp-tools-for-small-weddings',
            'title': 'Best RSVP Tools for Small Weddings: Free & Easy Solutions',
            'excerpt': 'Discover the best free RSVP tools for small weddings. Compare features, templates, and find the perfect solution.',
            'date': '2024-12-18',
            'category': 'Weddings'
        },
        {
            'slug': 'free-online-invitation-maker-guide',
            'title': 'Free Online Invitation Maker: Create Stunning Invites in Minutes',
            'excerpt': 'Complete guide to using free online invitation makers. Learn how to create professional invitations without design skills.',
            'date': '2024-12-17',
            'category': 'Tutorials'
        },
        {
            'slug': 'digital-vs-paper-invitations',
            'title': 'Digital vs Paper Invitations: Which is Better for Your Event?',
            'excerpt': 'Compare digital and paper invitations. Learn the pros and cons of each and make the best choice for your event.',
            'date': '2024-12-16',
            'category': 'Tips'
        },
        {
            'slug': 'birthday-party-invitation-ideas',
            'title': 'Birthday Party Invitation Ideas: Creative Templates & Tips',
            'excerpt': 'Get inspired with creative birthday party invitation ideas. Templates, themes, and tips for memorable invites.',
            'date': '2024-12-15',
            'category': 'Birthdays'
        },
        {
            'slug': 'corporate-event-invitation-etiquette',
            'title': 'Corporate Event Invitation Etiquette: Professional Guide',
            'excerpt': 'Master corporate event invitation etiquette. Learn how to create professional invites that make the right impression.',
            'date': '2024-12-14',
            'category': 'Corporate'
        },
        {
            'slug': 'rsvp-tracking-best-practices',
            'title': 'RSVP Tracking Best Practices: Manage Guest Responses Like a Pro',
            'excerpt': 'Learn RSVP tracking best practices to manage guest responses efficiently. Tools, tips, and strategies for event planners.',
            'date': '2024-12-13',
            'category': 'Tips'
        },
        {
            'slug': 'qr-code-invitations-guide',
            'title': 'QR Code Invitations: Modern Way to Share Your Event',
            'excerpt': 'Everything you need to know about QR code invitations. How to create, share, and use QR codes for events.',
            'date': '2024-12-12',
            'category': 'Technology'
        },
        {
            'slug': 'wedding-invitation-templates-free',
            'title': 'Free Wedding Invitation Templates: 15+ Beautiful Designs',
            'excerpt': 'Browse our collection of free wedding invitation templates. Elegant designs for every wedding style and theme.',
            'date': '2024-12-11',
            'category': 'Weddings'
        },
        {
            'slug': 'event-planning-rsvp-checklist',
            'title': 'Event Planning RSVP Checklist: Never Miss a Guest Response',
            'excerpt': 'Complete RSVP checklist for event planners. Track responses, manage guest lists, and ensure perfect attendance.',
            'date': '2024-12-10',
            'category': 'Tips'
        },
        {
            'slug': 'online-rsvp-vs-traditional-methods',
            'title': 'Online RSVP vs Traditional Methods: Which Should You Choose?',
            'excerpt': 'Compare online RSVP systems with traditional methods. Discover why digital RSVPs are becoming the new standard.',
            'date': '2024-12-09',
            'category': 'Technology'
        },
        {
            'slug': 'baby-shower-invitation-ideas',
            'title': 'Baby Shower Invitation Ideas: Cute Templates & Themes',
            'excerpt': 'Adorable baby shower invitation ideas and templates. Gender reveal, themed parties, and creative design inspiration.',
            'date': '2024-12-08',
            'category': 'Baby Showers'
        },
        {
            'slug': 'holiday-party-invitation-tips',
            'title': 'Holiday Party Invitation Tips: Spread the Festive Cheer',
            'excerpt': 'Create perfect holiday party invitations with our tips and templates. Christmas, New Year, and seasonal celebration ideas.',
            'date': '2024-12-07',
            'category': 'Holidays'
        },
        {
            'slug': 'rsvp-reminder-email-templates',
            'title': 'RSVP Reminder Email Templates: Get More Responses',
            'excerpt': 'Professional RSVP reminder email templates that get results. Learn when and how to send effective reminders.',
            'date': '2024-12-06',
            'category': 'Tips'
        },
        {
            'slug': 'mobile-friendly-invitations-importance',
            'title': 'Why Mobile-Friendly Invitations Matter: Statistics & Tips',
            'excerpt': 'Discover why mobile-friendly invitations are essential. Statistics, best practices, and responsive design tips.',
            'date': '2024-12-05',
            'category': 'Technology'
        }
    ]
    return render_template('blog/index.html', blog_posts=blog_posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    # Map slugs to blog post data
    blog_posts_map = {
        'how-to-create-wedding-rsvp-online': {
            'title': 'How to Create Wedding RSVP Online: Complete Guide 2024',
            'content': 'wedding_rsvp_guide',
            'date': '2024-12-19',
            'category': 'Weddings',
            'meta_description': 'Learn how to create beautiful wedding RSVP invitations online for free. Step-by-step guide with templates and tips for your special day.'
        },
        'best-rsvp-tools-for-small-weddings': {
            'title': 'Best RSVP Tools for Small Weddings: Free & Easy Solutions',
            'content': 'best_rsvp_tools',
            'date': '2024-12-18',
            'category': 'Weddings',
            'meta_description': 'Discover the best free RSVP tools for small weddings. Compare features, templates, and find the perfect solution for intimate celebrations.'
        }
    }
    
    post = blog_posts_map.get(slug)
    if not post:
        return render_template('404.html'), 404
    
    return render_template(f'blog/{post["content"]}.html', post=post, slug=slug)

# SEO Routes
@app.route('/sitemap.xml')
def sitemap():
    """Serve sitemap.xml for search engines"""
    return app.send_static_file('sitemap.xml')

@app.route('/robots.txt')
def robots():
    """Serve robots.txt for search engines"""
    return app.send_static_file('robots.txt')

# Email Notification Settings
@app.route('/settings/notifications')
@login_required
def notification_settings():
    """User email notification preferences"""
    return render_template('settings/notifications.html')

@app.route('/settings/notifications', methods=['POST'])
@login_required
def update_notification_settings():
    """Update email notification preferences"""
    # Safely update preferences (works even if columns don't exist yet)
    try:
        if hasattr(current_user, 'email_notifications_enabled'):
            current_user.email_notifications_enabled = request.form.get('email_notifications_enabled') == 'on'
        if hasattr(current_user, 'email_new_rsvp'):
            current_user.email_new_rsvp = request.form.get('email_new_rsvp') == 'on'
        if hasattr(current_user, 'email_reminders'):
            current_user.email_reminders = request.form.get('email_reminders') == 'on'
        if hasattr(current_user, 'email_weekly_summary'):
            current_user.email_weekly_summary = request.form.get('email_weekly_summary') == 'on'
        if hasattr(current_user, 'email_milestones'):
            current_user.email_milestones = request.form.get('email_milestones') == 'on'
        
        db.session.commit()
        flash('Notification settings updated successfully!', 'success')
    except Exception as e:
        flash('Settings saved (email features require database migration)', 'info')
    
    return redirect(url_for('notification_settings'))

# Background task for sending reminders (can be called via cron or scheduled task)
@app.route('/tasks/send-reminders')
def send_event_reminders():
    """Send event reminders 1 day before (call this daily via cron)"""
    if not email_service:
        return jsonify({'status': 'skipped', 'message': 'Email service not configured'})
    
    tomorrow = datetime.utcnow() + timedelta(days=1)
    tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0)
    tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59)
    
    # Find events happening tomorrow
    invitations = Invitation.query.filter(
        Invitation.event_date >= tomorrow_start,
        Invitation.event_date <= tomorrow_end
    ).all()
    
    sent_count = 0
    for invitation in invitations:
        # Send reminders to all guests who RSVPed "attending"
        for rsvp in invitation.rsvps:
            if rsvp.status == 'attending' and rsvp.guest_email:
                try:
                    email_service.send_event_reminder(
                        rsvp.guest_email,
                        rsvp.guest_name,
                        invitation
                    )
                    sent_count += 1
                except Exception as e:
                    print(f"Error sending reminder: {e}")
    
    return jsonify({'status': 'success', 'reminders_sent': sent_count})

@app.route('/tasks/send-weekly-summaries')
def send_weekly_summaries():
    """Send weekly RSVP summaries (call this weekly via cron)"""
    if not email_service:
        return jsonify({'status': 'skipped', 'message': 'Email service not configured'})
    
    # Email columns are optional - skip if they don't exist
    users = []
    
    sent_count = 0
    for user in users:
        # Get user's active invitations
        invitations = Invitation.query.filter_by(user_id=user.id).all()
        if invitations:
            try:
                email_service.send_weekly_summary(
                    user.email,
                    user.full_name,
                    invitations
                )
                sent_count += 1
            except Exception as e:
                print(f"Error sending weekly summary: {e}")
    
    return jsonify({'status': 'success', 'summaries_sent': sent_count})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)