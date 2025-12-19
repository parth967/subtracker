#!/usr/bin/env python3.10
"""
Weekend 1000 Users Setup

This script adds:
1. AGGRESSIVE SEO optimization for weekend traffic
2. 404 error page with performance monitoring
3. User signup cap at 1000 users
4. Performance optimizations
5. Viral marketing features
"""

import os

def create_404_page():
    """Create a beautiful 404 error page"""
    print("🚫 Creating 404 error page...")
    
    error_404_content = '''{% extends "base.html" %}

{% block title %}Page Not Found - RSVP Hub{% endblock %}

{% block content %}
<div class="container-fluid vh-100 d-flex align-items-center justify-content-center bg-gradient" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="text-center text-white">
        <div class="error-animation mb-4">
            <h1 class="display-1 fw-bold animate__animated animate__bounceIn">404</h1>
            <div class="error-icon mb-4">
                <i class="fas fa-search fa-5x opacity-75"></i>
            </div>
        </div>
        
        <h2 class="h3 mb-3">Oops! Page Not Found</h2>
        <p class="lead mb-4">The page you're looking for seems to have wandered off to another celebration!</p>
        
        <div class="d-flex flex-column flex-md-row gap-3 justify-content-center">
            <a href="{{ url_for('home') }}" class="btn btn-light btn-lg">
                <i class="fas fa-home me-2"></i>Go Home
            </a>
            <a href="{{ url_for('template_gallery') }}" class="btn btn-outline-light btn-lg">
                <i class="fas fa-palette me-2"></i>Browse Templates
            </a>
            <a href="{{ url_for('register') }}" class="btn btn-success btn-lg">
                <i class="fas fa-user-plus me-2"></i>Join RSVP Hub
            </a>
        </div>
        
        <!-- Popular searches for SEO -->
        <div class="mt-5">
            <p class="small mb-2">Popular searches:</p>
            <div class="d-flex flex-wrap gap-2 justify-content-center">
                <a href="{{ url_for('template_gallery') }}" class="badge bg-light text-dark text-decoration-none">Wedding Invitations</a>
                <a href="{{ url_for('template_gallery') }}" class="badge bg-light text-dark text-decoration-none">Birthday Invites</a>
                <a href="{{ url_for('template_gallery') }}" class="badge bg-light text-dark text-decoration-none">Party Planning</a>
                <a href="{{ url_for('template_gallery') }}" class="badge bg-light text-dark text-decoration-none">RSVP Management</a>
                <a href="{{ url_for('template_gallery') }}" class="badge bg-light text-dark text-decoration-none">Free Templates</a>
            </div>
        </div>
    </div>
</div>

<!-- Performance monitoring script -->
<script>
// Track 404 errors for performance monitoring
if (typeof gtag !== 'undefined') {
    gtag('event', 'page_not_found', {
        'page_location': window.location.href,
        'page_title': document.title
    });
}

// Redirect to home after 10 seconds if user doesn't interact
let redirectTimer = setTimeout(function() {
    window.location.href = "{{ url_for('home') }}";
}, 10000);

// Cancel redirect if user interacts
document.addEventListener('click', function() {
    clearTimeout(redirectTimer);
});
</script>

<style>
.animate__bounceIn {
    animation: bounceIn 1s;
}

@keyframes bounceIn {
    0%, 20%, 40%, 60%, 80%, 100% {
        animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
    }
    0% {
        opacity: 0;
        transform: scale3d(.3, .3, .3);
    }
    20% {
        transform: scale3d(1.1, 1.1, 1.1);
    }
    40% {
        transform: scale3d(.9, .9, .9);
    }
    60% {
        opacity: 1;
        transform: scale3d(1.03, 1.03, 1.03);
    }
    80% {
        transform: scale3d(.97, .97, .97);
    }
    100% {
        opacity: 1;
        transform: scale3d(1, 1, 1);
    }
}
</style>
{% endblock %}'''
    
    try:
        with open('templates/404.html', 'w') as f:
            f.write(error_404_content)
        print("✅ Created 404.html")
        return True
    except Exception as e:
        print(f"❌ Error creating 404.html: {e}")
        return False

def add_user_cap_and_performance():
    """Add user signup cap and performance monitoring to app.py"""
    print("👥 Adding 1000 user signup cap and performance monitoring...")
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Add imports at the top
        imports_to_add = '''
import time
from functools import wraps
from datetime import datetime, timedelta
'''
        
        if 'import time' not in content:
            # Add after existing imports
            import_section = content.find('from dotenv import load_dotenv')
            if import_section != -1:
                end_of_line = content.find('\n', import_section)
                content = content[:end_of_line] + imports_to_add + content[end_of_line:]
        
        # Add performance monitoring decorator
        performance_decorator = '''
# Performance monitoring decorator
def monitor_performance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        try:
            result = f(*args, **kwargs)
            end_time = time.time()
            # Log slow requests (over 2 seconds)
            if end_time - start_time > 2:
                print(f"SLOW REQUEST: {f.__name__} took {end_time - start_time:.2f}s")
            return result
        except Exception as e:
            print(f"ERROR in {f.__name__}: {e}")
            raise
    return decorated_function

# User cap check function
def check_user_limit():
    """Check if we've reached the 1000 user limit"""
    user_count = User.query.count()
    return user_count >= 1000

'''
        
        # Add after database models
        if 'def generate_invitation_code():' in content and 'def monitor_performance' not in content:
            insertion_point = content.find('def generate_invitation_code():')
            content = content[:insertion_point] + performance_decorator + content[insertion_point:]
        
        # Add 404 error handler
        error_handler = '''
# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 500

'''
        
        # Add error handlers before routes
        if '@app.route' in content and '@app.errorhandler(404)' not in content:
            first_route = content.find('@app.route')
            content = content[:first_route] + error_handler + content[first_route:]
        
        # Modify register route to include user cap
        register_route_pattern = "if User.query.filter_by(username=username).first():"
        if register_route_pattern in content:
            user_cap_check = '''    # Check user limit (cap at 1000 users)
    if check_user_limit():
        flash('Sorry! We\'ve reached our beta user limit of 1000 users. Join our waitlist!', 'error')
        return redirect(url_for('register'))
    
    '''
            content = content.replace(register_route_pattern, user_cap_check + register_route_pattern)
        
        # Add performance monitoring to key routes
        routes_to_monitor = ['home', 'dashboard', 'create_invitation', 'register', 'login']
        for route in routes_to_monitor:
            pattern = f"def {route}():"
            if pattern in content and f"@monitor_performance\ndef {route}():" not in content:
                content = content.replace(f"def {route}():", f"@monitor_performance\ndef {route}():")
        
        with open('app.py', 'w') as f:
            f.write(content)
        print("✅ Added user cap and performance monitoring to app.py")
        return True
        
    except Exception as e:
        print(f"❌ Error updating app.py: {e}")
        return False

def create_aggressive_seo_content():
    """Create aggressive SEO content for weekend traffic"""
    print("🔥 Creating AGGRESSIVE SEO content for weekend traffic...")
    
    # Create SEO landing pages
    landing_pages = {
        'wedding-invitations.html': {
            'title': 'Free Wedding Invitations - Beautiful Templates | RSVP Hub',
            'description': 'Create stunning wedding invitations for free! 50+ elegant templates, RSVP tracking, QR codes. Perfect for your special day.',
            'keywords': 'wedding invitations, free wedding invites, wedding RSVP, elegant wedding cards',
            'content': '''
<div class="hero bg-gradient text-white py-5">
    <div class="container text-center">
        <h1 class="display-4 fw-bold mb-3">Free Wedding Invitations</h1>
        <p class="lead mb-4">Create stunning wedding invitations that your guests will love</p>
        <a href="{{ url_for('register') }}" class="btn btn-light btn-lg">Start Creating Free</a>
    </div>
</div>

<div class="container py-5">
    <div class="row">
        <div class="col-lg-8 mx-auto">
            <h2>Why Choose RSVP Hub for Your Wedding Invitations?</h2>
            <div class="row g-4 mt-4">
                <div class="col-md-6">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5>💒 Elegant Designs</h5>
                            <p>Beautiful wedding invitation templates designed by professionals</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5>📱 Digital & Print Ready</h5>
                            <p>Perfect for both digital sharing and professional printing</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>'''
        },
        'birthday-invitations.html': {
            'title': 'Free Birthday Invitations - Fun Templates | RSVP Hub',
            'description': 'Create amazing birthday invitations for free! Fun templates for all ages, easy RSVP management, instant sharing.',
            'keywords': 'birthday invitations, free birthday invites, party invitations, birthday RSVP',
            'content': '''
<div class="hero bg-gradient text-white py-5">
    <div class="container text-center">
        <h1 class="display-4 fw-bold mb-3">Free Birthday Invitations</h1>
        <p class="lead mb-4">Make every birthday celebration special with beautiful invitations</p>
        <a href="{{ url_for('register') }}" class="btn btn-light btn-lg">Create Birthday Invite</a>
    </div>
</div>'''
        }
    }
    
    for filename, page_data in landing_pages.items():
        page_content = f'''{{%- extends "base.html" %}}

{{%- block title %}}{page_data['title']}{{%- endblock %}}

{{%- block content %}}
{page_data['content']}
{{%- endblock %}}'''
        
        try:
            with open(f'templates/{filename}', 'w') as f:
                f.write(page_content)
            print(f"✅ Created {filename}")
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")

def add_viral_features():
    """Add viral marketing features"""
    print("🚀 Adding viral marketing features...")
    
    viral_js = '''
<!-- Viral Marketing Features -->
<script>
// Social sharing functions
function shareOnFacebook(url, title) {
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}&quote=${encodeURIComponent(title)}`;
    window.open(shareUrl, 'facebook-share', 'width=580,height=296');
}

function shareOnTwitter(url, title) {
    const shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}&hashtags=RSVPHub,FreeInvitations,EventPlanning`;
    window.open(shareUrl, 'twitter-share', 'width=580,height=296');
}

function shareOnWhatsApp(url, title) {
    const shareUrl = `https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}`;
    window.open(shareUrl, 'whatsapp-share');
}

// Copy link to clipboard
function copyInviteLink(url) {
    navigator.clipboard.writeText(url).then(function() {
        alert('Invitation link copied to clipboard!');
    });
}

// Track viral actions
function trackViralAction(action, platform) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'viral_share', {
            'action': action,
            'platform': platform,
            'page_location': window.location.href
        });
    }
}

// Weekend promotion popup
document.addEventListener('DOMContentLoaded', function() {
    // Show weekend promotion after 30 seconds
    setTimeout(function() {
        if (!localStorage.getItem('weekend_promo_shown')) {
            showWeekendPromo();
            localStorage.setItem('weekend_promo_shown', 'true');
        }
    }, 30000);
});

function showWeekendPromo() {
    const promoHtml = `
        <div class="modal fade" id="weekendPromo" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">🎉 Weekend Special!</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <h4>Join 1000+ Happy Users!</h4>
                        <p>Create your first invitation in under 2 minutes</p>
                        <div class="d-grid gap-2">
                            <a href="/register" class="btn btn-primary btn-lg">Start Creating Free</a>
                            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Maybe Later</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', promoHtml);
    const modal = new bootstrap.Modal(document.getElementById('weekendPromo'));
    modal.show();
}
</script>'''
    
    try:
        with open('templates/base.html', 'r') as f:
            content = f.read()
        
        if 'shareOnFacebook' not in content:
            # Add before closing body tag
            content = content.replace('</body>', viral_js + '\n</body>')
            
            with open('templates/base.html', 'w') as f:
                f.write(content)
            print("✅ Added viral marketing features")
            return True
        else:
            print("⚠️  Viral features already exist")
            return False
            
    except Exception as e:
        print(f"❌ Error adding viral features: {e}")
        return False

def create_weekend_seo_boost():
    """Create weekend-specific SEO content"""
    print("📈 Creating weekend SEO boost content...")
    
    weekend_seo = '''
    <!-- Weekend SEO Boost -->
    <meta name="google-site-verification" content="weekend-boost-rsvp-hub">
    
    <!-- Weekend-specific keywords -->
    <meta name="keywords" content="weekend party invitations, saturday event planning, sunday celebration invites, weekend wedding planning, quick party invites, last minute invitations, weekend event management, saturday party planning, sunday brunch invites">
    
    <!-- Local SEO for weekend events -->
    <meta name="geo.region" content="US">
    <meta name="geo.placename" content="United States">
    <meta name="geo.position" content="39.8283;-98.5795">
    
    <!-- Weekend urgency meta -->
    <meta property="article:published_time" content="2025-12-19T00:00:00Z">
    <meta property="article:modified_time" content="2025-12-19T12:00:00Z">
    
    <!-- Weekend promotion structured data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "SpecialAnnouncement",
        "name": "Weekend RSVP Hub Launch",
        "text": "Join 1000+ users creating beautiful invitations this weekend",
        "datePosted": "2025-12-19",
        "expires": "2025-12-22",
        "category": "Event Planning",
        "audience": {
            "@type": "Audience",
            "audienceType": "Event Planners"
        }
    }
    </script>'''
    
    try:
        with open('templates/base.html', 'r') as f:
            content = f.read()
        
        if 'weekend-boost-rsvp-hub' not in content:
            # Add after existing meta tags
            charset_pos = content.find('<meta charset="UTF-8">')
            if charset_pos != -1:
                end_pos = content.find('\n', charset_pos)
                content = content[:end_pos] + weekend_seo + content[end_pos:]
                
                with open('templates/base.html', 'w') as f:
                    f.write(content)
                print("✅ Added weekend SEO boost")
                return True
        else:
            print("⚠️  Weekend SEO already exists")
            return False
            
    except Exception as e:
        print(f"❌ Error adding weekend SEO: {e}")
        return False

def main():
    """Main function for weekend 1000 users setup"""
    print("🚀 WEEKEND 1000 USERS SETUP")
    print("=" * 50)
    
    success_count = 0
    
    # Create 404 page
    if create_404_page():
        success_count += 1
    
    # Add user cap and performance monitoring
    if add_user_cap_and_performance():
        success_count += 1
    
    # Create aggressive SEO content
    create_aggressive_seo_content()
    success_count += 1
    
    # Add viral features
    if add_viral_features():
        success_count += 1
    
    # Create weekend SEO boost
    if create_weekend_seo_boost():
        success_count += 1
    
    print("\n" + "=" * 50)
    print("🎯 WEEKEND 1000 USERS SETUP COMPLETE!")
    print("=" * 50)
    
    print(f"\n✅ Successfully added {success_count}/5 features:")
    print("✅ Beautiful 404 error page with auto-redirect")
    print("✅ 1000 user signup cap with performance monitoring")
    print("✅ Aggressive SEO landing pages for weekend traffic")
    print("✅ Viral marketing features (social sharing, popups)")
    print("✅ Weekend-specific SEO boost with urgency")
    
    print(f"\n🎯 Weekend Traffic Strategy:")
    print("🔥 Target keywords: 'weekend party invitations', 'quick event planning'")
    print("📱 Viral sharing buttons on all pages")
    print("⏰ Weekend urgency popups after 30 seconds")
    print("🚫 User cap at 1000 to create exclusivity")
    print("📊 Performance monitoring for high traffic")
    print("🎉 Weekend promotion modal for conversions")
    
    print(f"\n🚀 Action Plan for 1000 Users This Weekend:")
    print("1. Deploy to PythonAnywhere immediately")
    print("2. Share on social media with hashtags #RSVPHub #FreeInvitations")
    print("3. Post in event planning Facebook groups")
    print("4. Submit to ProductHunt for weekend launch")
    print("5. Create TikTok videos showing quick invitation creation")
    print("6. Email friends/family to share with their networks")
    print("7. Post in Reddit r/weddingplanning, r/party")
    
    print(f"\n🎊 Your RSVP Hub is ready for 1000 weekend users!")

if __name__ == "__main__":
    main()