// Trendy Features for RSVP Hub
// Viral sharing, social proof, and modern UI enhancements

// Live User Counter (Animated)
function updateLiveUserCounter() {
    const counter = document.getElementById('live-user-counter');
    if (counter) {
        let currentCount = parseInt(counter.textContent) || 1000;
        // Simulate live updates (in production, fetch from API)
        setInterval(() => {
            currentCount += Math.floor(Math.random() * 3);
            counter.textContent = currentCount.toLocaleString() + '+';
        }, 30000); // Update every 30 seconds
    }
}

// Viral Social Sharing with Animations
function initViralSharing() {
    // Add trendy share buttons
    const shareButtons = document.querySelectorAll('.viral-share-btn');
    shareButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const platform = this.dataset.platform;
            const url = this.dataset.url || window.location.href;
            const title = this.dataset.title || document.title;
            
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            
            shareToPlatform(platform, url, title);
        });
    });
}

function shareToPlatform(platform, url, title) {
    const encodedUrl = encodeURIComponent(url);
    const encodedTitle = encodeURIComponent(title);
    
    const shareUrls = {
        'facebook': `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedTitle}`,
        'twitter': `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}&hashtags=RSVPHub,FreeInvitations,EventPlanning`,
        'whatsapp': `https://wa.me/?text=${encodedTitle}%20${encodedUrl}`,
        'pinterest': `https://pinterest.com/pin/create/button/?url=${encodedUrl}&description=${encodedTitle}`,
        'instagram': `https://www.instagram.com/`, // Instagram doesn't support direct sharing
        'linkedin': `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`,
        'email': `mailto:?subject=${encodedTitle}&body=Check%20this%20out:%20${encodedUrl}`
    };
    
    if (shareUrls[platform]) {
        window.open(shareUrls[platform], '_blank', 'width=600,height=400');
        trackShare(platform);
    }
}

// Track viral shares
function trackShare(platform) {
    // Send analytics event
    if (typeof clarity !== 'undefined') {
        clarity('event', 'viral_share', { platform: platform });
    }
    console.log(`Shared to ${platform}`);
}

// Copy Link with Trendy Animation
function copyInviteLink(url, buttonElement) {
    navigator.clipboard.writeText(url).then(() => {
        const originalText = buttonElement.innerHTML;
        buttonElement.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
        buttonElement.classList.add('btn-success');
        buttonElement.classList.remove('btn-outline-primary');
        
        setTimeout(() => {
            buttonElement.innerHTML = originalText;
            buttonElement.classList.remove('btn-success');
            buttonElement.classList.add('btn-outline-primary');
        }, 2000);
        
        // Show trendy toast notification
        showTrendyToast('Link copied to clipboard! 🎉');
    });
}

// Trendy Toast Notifications
function showTrendyToast(message) {
    const toast = document.createElement('div');
    toast.className = 'trendy-toast';
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-check-circle me-2"></i>
            ${message}
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Floating Action Button (FAB) for Quick Share
function createFloatingShareButton() {
    const fab = document.createElement('div');
    fab.className = 'floating-share-fab';
    fab.innerHTML = `
        <button class="fab-button" id="fab-main">
            <i class="fas fa-share-alt"></i>
        </button>
        <div class="fab-menu" id="fab-menu">
            <a href="#" class="fab-item" data-platform="facebook" title="Share on Facebook">
                <i class="fab fa-facebook"></i>
            </a>
            <a href="#" class="fab-item" data-platform="twitter" title="Share on Twitter">
                <i class="fab fa-twitter"></i>
            </a>
            <a href="#" class="fab-item" data-platform="whatsapp" title="Share on WhatsApp">
                <i class="fab fa-whatsapp"></i>
            </a>
            <a href="#" class="fab-item" data-platform="pinterest" title="Share on Pinterest">
                <i class="fab fa-pinterest"></i>
            </a>
            <a href="#" class="fab-item" data-platform="email" title="Share via Email">
                <i class="fas fa-envelope"></i>
            </a>
        </div>
    `;
    document.body.appendChild(fab);
    
    const fabMain = document.getElementById('fab-main');
    const fabMenu = document.getElementById('fab-menu');
    
    fabMain.addEventListener('click', () => {
        fabMenu.classList.toggle('active');
        fabMain.classList.toggle('active');
    });
    
    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!fab.contains(e.target)) {
            fabMenu.classList.remove('active');
            fabMain.classList.remove('active');
        }
    });
    
    // Handle share clicks
    fabMenu.querySelectorAll('.fab-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const platform = item.dataset.platform;
            shareToPlatform(platform, window.location.href, document.title);
            fabMenu.classList.remove('active');
            fabMain.classList.remove('active');
        });
    });
}

// Social Proof: Show Recent Activity
function showSocialProof() {
    const activities = [
        { name: 'Sarah M.', action: 'created a wedding invitation', time: '2 minutes ago' },
        { name: 'John D.', action: 'shared a birthday party invite', time: '5 minutes ago' },
        { name: 'Emma L.', action: 'created a corporate event', time: '8 minutes ago' },
        { name: 'Mike T.', action: 'shared a wedding RSVP', time: '12 minutes ago' }
    ];
    
    const proofContainer = document.getElementById('social-proof');
    if (proofContainer) {
        let index = 0;
        setInterval(() => {
            const activity = activities[index % activities.length];
            proofContainer.innerHTML = `
                <div class="social-proof-item">
                    <i class="fas fa-user-circle me-2"></i>
                    <strong>${activity.name}</strong> ${activity.action}
                    <span class="text-muted ms-2">${activity.time}</span>
                </div>
            `;
            index++;
        }, 5000);
    }
}

// Referral Program UI
function initReferralProgram() {
    const referralBtn = document.getElementById('referral-btn');
    if (referralBtn) {
        referralBtn.addEventListener('click', () => {
            const referralCode = referralBtn.dataset.code || 'RSVPHUB2024';
            const referralUrl = `${window.location.origin}/register?ref=${referralCode}`;
            copyInviteLink(referralUrl, referralBtn);
        });
    }
}

// Trendy Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Initialize all trendy features
document.addEventListener('DOMContentLoaded', () => {
    updateLiveUserCounter();
    initViralSharing();
    showSocialProof();
    initReferralProgram();
    initScrollAnimations();
    
    // Add floating share button on invitation pages
    if (window.location.pathname.includes('/invitation/')) {
        createFloatingShareButton();
    }
});

// Add trendy CSS dynamically
const trendyStyles = `
<style>
/* Trendy Toast */
.trendy-toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    z-index: 9999;
    transform: translateY(100px);
    opacity: 0;
    transition: all 0.3s ease;
}

.trendy-toast.show {
    transform: translateY(0);
    opacity: 1;
}

/* Floating Action Button */
.floating-share-fab {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 1000;
}

.fab-button {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
}

.fab-button:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.fab-button.active {
    transform: rotate(45deg);
}

.fab-menu {
    position: absolute;
    bottom: 80px;
    right: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
    opacity: 0;
    visibility: hidden;
    transform: translateY(20px);
    transition: all 0.3s ease;
}

.fab-menu.active {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.fab-item {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #667eea;
    text-decoration: none;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.fab-item:hover {
    transform: scale(1.1);
    color: #764ba2;
}

.fab-item i {
    font-size: 1.2rem;
}

/* Social Proof */
.social-proof-item {
    padding: 0.75rem;
    background: rgba(102, 126, 234, 0.1);
    border-radius: 8px;
    margin-bottom: 0.5rem;
    animation: slideIn 0.5s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Scroll Animations */
.animate-on-scroll {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.6s ease;
}

.animate-on-scroll.animate-in {
    opacity: 1;
    transform: translateY(0);
}

/* Viral Share Buttons */
.viral-share-btn {
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.viral-share-btn::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255,255,255,0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.viral-share-btn:active::before {
    width: 300px;
    height: 300px;
}

/* Live Counter Animation */
#live-user-counter {
    display: inline-block;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

@media (max-width: 768px) {
    .floating-share-fab {
        bottom: 20px;
        right: 20px;
    }
    
    .fab-button {
        width: 50px;
        height: 50px;
        font-size: 1.2rem;
    }
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', trendyStyles);

