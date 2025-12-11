"""
SubTracker Pro - Professional Subscription Management Dashboard

A Flask-based web application for tracking and managing all your subscriptions.
Features include:
- Multi-user subscription tracking
- Cost analytics and insights
- Subscription categorization
- Payment tracking and reminders
- Future spending projections
- Real-time cost analysis

Author: SubTracker Pro Team
License: MIT
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, TextAreaField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from decimal import Decimal
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///subscription_manager.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access SubTracker Pro.'
login_manager.login_message_category = 'info'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return AuthUser.query.get(int(user_id))

# Authentication Forms
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignupForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])

class SubscriptionForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    cost = DecimalField('Cost', validators=[DataRequired()])
    billing_cycle = SelectField('Billing Cycle', 
                               choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')],
                               validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description')
    website_url = StringField('Website URL')
    notes = TextAreaField('Notes')

# Database Models
class AuthUser(UserMixin, db.Model):
    """Authentication user model for login system"""
    __tablename__ = 'auth_users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to subscription users
    subscription_users = db.relationship('User', backref='auth_user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<AuthUser {self.email}>'

class User(db.Model):
    """Subscription user model (for tracking who uses which subscriptions)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    user_type = db.Column(db.String(50), default='personal')  # personal, business, family
    auth_user_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(50), default='fas fa-star')
    color = db.Column(db.String(20), default='primary')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    subscriptions = db.relationship('Subscription', backref='category', lazy=True)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    billing_cycle = db.Column(db.String(20), nullable=False)  # monthly, yearly, weekly
    start_date = db.Column(db.Date, nullable=False)
    next_billing = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, paused, cancelled
    website_url = db.Column(db.String(200))
    notes = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(50))  # credit_card, debit_card, paypal, etc.
    status = db.Column(db.String(20), default='completed')  # completed, pending, failed
    notes = db.Column(db.Text)
    
    subscription = db.relationship('Subscription', backref='payments')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper Functions
def calculate_next_billing(start_date, billing_cycle):
    """Calculate next billing date based on cycle"""
    if billing_cycle == 'monthly':
        if start_date.month == 12:
            return start_date.replace(year=start_date.year + 1, month=1)
        else:
            return start_date.replace(month=start_date.month + 1)
    elif billing_cycle == 'yearly':
        return start_date.replace(year=start_date.year + 1)
    elif billing_cycle == 'weekly':
        return start_date + timedelta(weeks=1)
    return start_date

def get_monthly_cost(cost, billing_cycle):
    """Convert any billing cycle to monthly cost for comparison"""
    if billing_cycle == 'monthly':
        return float(cost)
    elif billing_cycle == 'yearly':
        return float(cost) / 12
    elif billing_cycle == 'weekly':
        return float(cost) * 4.33  # Average weeks per month
    return float(cost)

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthUser.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = SignupForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = AuthUser.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in instead.', 'error')
            return redirect(url_for('login'))
        
        # Create new user
        user = AuthUser(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # Create default personal user for subscriptions
        personal_user = User(
            name=form.name.data,
            email=form.email.data,
            user_type='personal',
            auth_user_id=user.id
        )
        db.session.add(personal_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Main Routes
@app.route('/')
@login_required
def dashboard():
    """Main dashboard with analytics"""
    # Get data for current user only
    users = User.query.filter_by(auth_user_id=current_user.id).all()
    categories = Category.query.all()
    subscriptions = Subscription.query.join(User).filter(
        User.auth_user_id == current_user.id,
        Subscription.status == 'active'
    ).all()
    
    # Calculate analytics
    total_subscriptions = len(subscriptions)
    total_monthly_cost = sum(get_monthly_cost(sub.cost, sub.billing_cycle) for sub in subscriptions)
    total_yearly_cost = total_monthly_cost * 12
    
    # Upcoming renewals (next 30 days)
    upcoming_renewals = Subscription.query.filter(
        Subscription.next_billing <= datetime.now().date() + timedelta(days=30),
        Subscription.status == 'active'
    ).order_by(Subscription.next_billing).all()
    
    # Category breakdown
    category_stats = {}
    for category in categories:
        cat_subs = [s for s in subscriptions if s.category_id == category.id]
        if cat_subs:
            category_stats[category.name] = {
                'count': len(cat_subs),
                'monthly_cost': sum(get_monthly_cost(s.cost, s.billing_cycle) for s in cat_subs),
                'color': category.color,
                'icon': category.icon
            }
    
    # User breakdown
    user_stats = {}
    for user in users:
        user_subs = [s for s in subscriptions if s.user_id == user.id]
        if user_subs:
            user_stats[user.name] = {
                'count': len(user_subs),
                'monthly_cost': sum(get_monthly_cost(s.cost, s.billing_cycle) for s in user_subs),
                'type': user.user_type
            }
    
    # Recent subscriptions
    recent_subscriptions = Subscription.query.order_by(Subscription.created_at.desc()).limit(5).all()
    
    stats = {
        'total_subscriptions': total_subscriptions,
        'total_monthly_cost': round(total_monthly_cost, 2),
        'total_yearly_cost': round(total_yearly_cost, 2),
        'avg_cost_per_subscription': round(total_monthly_cost / total_subscriptions if total_subscriptions > 0 else 0, 2),
        'category_stats': category_stats,
        'user_stats': user_stats
    }
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         upcoming_renewals=upcoming_renewals,
                         recent_subscriptions=recent_subscriptions,
                         users=users,
                         categories=categories)

@app.route('/subscriptions')
@login_required
def subscriptions():
    """View all subscriptions"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    category_id = request.args.get('category', 'all')
    user_id = request.args.get('user', 'all')
    
    query = Subscription.query.join(User).filter(User.auth_user_id == current_user.id)
    
    if status != 'all':
        query = query.filter(Subscription.status == status)
    if category_id != 'all':
        query = query.filter(Subscription.category_id == category_id)
    if user_id != 'all':
        query = query.filter(Subscription.user_id == user_id)
    
    subscriptions = query.order_by(Subscription.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    users = User.query.filter_by(auth_user_id=current_user.id).all()
    categories = Category.query.all()
    
    return render_template('subscriptions.html', 
                         subscriptions=subscriptions,
                         users=users,
                         categories=categories,
                         current_status=status,
                         current_category=category_id,
                         current_user=user_id,
                         today=datetime.now().date())

@app.route('/add_subscription', methods=['GET', 'POST'])
@login_required
def add_subscription():
    """Add new subscription"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            cost = Decimal(request.form['cost'])
            billing_cycle = request.form['billing_cycle']
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            user_id = request.form['user_id']
            category_id = request.form['category_id']
            
            # Calculate next billing date
            next_billing = calculate_next_billing(start_date, billing_cycle)
            
            subscription = Subscription(
                name=name,
                description=request.form.get('description', ''),
                cost=cost,
                billing_cycle=billing_cycle,
                start_date=start_date,
                next_billing=next_billing,
                website_url=request.form.get('website_url', ''),
                notes=request.form.get('notes', ''),
                user_id=user_id,
                category_id=category_id
            )
            
            db.session.add(subscription)
            db.session.commit()
            
            flash('Subscription added successfully!', 'success')
            return redirect(url_for('subscriptions'))
            
        except Exception as e:
            flash(f'Error adding subscription: {str(e)}', 'error')
    
    users = User.query.filter_by(auth_user_id=current_user.id).all()
    categories = Category.query.all()
    
    return render_template('add_subscription.html', users=users, categories=categories)

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    """Add new user"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form.get('email', '')
            user_type = request.form['user_type']
            
            user = User(
                name=name,
                email=email if email else None,
                user_type=user_type,
                auth_user_id=current_user.id
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('User added successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error adding user: {str(e)}', 'error')
    
    return render_template('add_user.html')

@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    """Add new category"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            icon = request.form['icon']
            color = request.form['color']
            
            category = Category(
                name=name,
                icon=icon,
                color=color
            )
            
            db.session.add(category)
            db.session.commit()
            
            flash('Category added successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error adding category: {str(e)}', 'error')
    
    return render_template('add_category.html')

@app.route('/analytics')
@login_required
def analytics():
    """Detailed analytics page"""
    subscriptions = Subscription.query.join(User).filter(
        User.auth_user_id == current_user.id,
        Subscription.status == 'active'
    ).all()
    
    # Monthly spending trend (last 12 months)
    monthly_data = {}
    for i in range(12):
        month_date = datetime.now().replace(day=1) - timedelta(days=30*i)
        month_key = month_date.strftime('%Y-%m')
        monthly_data[month_key] = 0
    
    # Calculate spending by month
    for sub in subscriptions:
        monthly_cost = get_monthly_cost(sub.cost, sub.billing_cycle)
        for month in monthly_data.keys():
            if sub.start_date <= datetime.strptime(month + '-01', '%Y-%m-%d').date():
                monthly_data[month] += monthly_cost
    
    # Sort by date
    sorted_months = sorted(monthly_data.items())
    
    return render_template('analytics.html', 
                         subscriptions=subscriptions,
                         monthly_data=sorted_months)

@app.route('/api/subscription_data')
@login_required
def api_subscription_data():
    """API endpoint for chart data"""
    subscriptions = Subscription.query.join(User).filter(
        User.auth_user_id == current_user.id,
        Subscription.status == 'active'
    ).all()
    categories = Category.query.all()
    
    # Category data for pie chart
    category_data = {}
    for category in categories:
        cat_subs = [s for s in subscriptions if s.category_id == category.id]
        if cat_subs:
            category_data[category.name] = sum(get_monthly_cost(s.cost, s.billing_cycle) for s in cat_subs)
    
    return jsonify({
        'categories': list(category_data.keys()),
        'category_costs': list(category_data.values())
    })

def init_default_data():
    """Initialize default categories and sample data"""
    if Category.query.count() == 0:
        default_categories = [
            {'name': 'Streaming', 'icon': 'fas fa-play', 'color': 'danger'},
            {'name': 'Software', 'icon': 'fas fa-laptop-code', 'color': 'primary'},
            {'name': 'Cloud Storage', 'icon': 'fas fa-cloud', 'color': 'info'},
            {'name': 'Music', 'icon': 'fas fa-music', 'color': 'success'},
            {'name': 'News & Media', 'icon': 'fas fa-newspaper', 'color': 'warning'},
            {'name': 'Fitness', 'icon': 'fas fa-dumbbell', 'color': 'secondary'},
            {'name': 'Gaming', 'icon': 'fas fa-gamepad', 'color': 'dark'},
            {'name': 'Productivity', 'icon': 'fas fa-tasks', 'color': 'info'},
        ]
        
        for cat_data in default_categories:
            category = Category(**cat_data)
            db.session.add(category)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_default_data()
    app.run(debug=True, host='127.0.0.1', port=5001)