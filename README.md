# 🎉 InviteMe - Beautiful Invitation & RSVP Platform

Create stunning invitations and manage RSVPs with ease. A modern, free, and user-friendly platform for all your celebration needs.

![InviteMe Banner](https://via.placeholder.com/800x200/667eea/ffffff?text=InviteMe+-+Beautiful+Invitations)

## ✨ Features

### 🎨 **Beautiful Templates**
- **6 Professional Templates**: Classic, Modern, Floral, Vintage, Festive, and Corporate
- **Fully Customizable**: Change colors, fonts, and layouts
- **Mobile Responsive**: Perfect on any device
- **Event-Specific Icons**: Automatic icons based on event type

### 📱 **Easy Sharing**
- **Unique Links**: Each invitation gets a unique, shareable URL
- **QR Code Generation**: Instant QR codes for easy sharing
- **Social Media Integration**: Share on WhatsApp, Facebook, Twitter, Email
- **No Registration Required**: Guests can RSVP without creating accounts

### 📊 **RSVP Management**
- **Real-time Tracking**: See responses as they come in
- **Detailed Analytics**: Beautiful charts and statistics
- **Guest Information**: Collect names, emails, dietary requirements
- **Status Options**: Attending, Not Attending, Maybe
- **Guest Count Tracking**: Handle plus-ones and families

### 🎯 **Event Types**
- **Weddings**: Elegant designs for your special day
- **Birthday Parties**: Fun and colorful celebrations
- **Corporate Events**: Professional business invitations
- **Baby Showers**: Sweet and gentle designs
- **Graduations**: Achievement celebration templates
- **Holiday Parties**: Festive seasonal designs
- **Custom Events**: Flexible for any occasion

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
git clone <repository-url>
cd inviteme

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python migrate_db.py init
```

### 2. Run the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
python app.py
```

### 3. Open in Browser

Visit `http://localhost:5000` and start creating beautiful invitations!

## 📖 How to Use

### Creating an Invitation

1. **Visit the Homepage**: Go to `http://localhost:5000`
2. **Click "Create Invitation"**: Start the creation process
3. **Fill Event Details**:
   - Event title and description
   - Date, time, and venue information
   - Host contact details
4. **Choose Design**:
   - Select from 6 beautiful templates
   - Pick your favorite color scheme
   - Add a personal message
5. **Set Preferences**:
   - Maximum guest limit (optional)
   - RSVP requirements
6. **Create & Share**: Get your unique invitation link instantly!

### Managing RSVPs

1. **Access Management Dashboard**: Use the link provided after creation
2. **View Real-time Stats**: See who's attending, maybe, or can't make it
3. **Share Your Invitation**:
   - Copy the unique link
   - Share via social media
   - Use the QR code for easy scanning
4. **Track Responses**: Monitor guest details, dietary requirements, and messages

### Guest Experience

1. **Receive Invitation**: Guests get a beautiful, mobile-friendly invitation
2. **Easy RSVP**: Simple form with attendance status selection
3. **Provide Details**: Name, contact info, guest count, dietary needs
4. **Leave Messages**: Personal messages for the host
5. **Instant Confirmation**: Immediate feedback after submitting

## 🎨 Template Gallery

### Classic Elegance
- **Perfect for**: Weddings, formal events
- **Style**: Timeless, sophisticated
- **Colors**: Royal blues and purples

### Modern Minimalist
- **Perfect for**: Corporate events, contemporary celebrations
- **Style**: Clean, professional
- **Colors**: Cool blues and teals

### Floral Garden
- **Perfect for**: Garden parties, spring events
- **Style**: Nature-inspired, romantic
- **Colors**: Warm pinks and yellows

### Vintage Charm
- **Perfect for**: Retro parties, nostalgic events
- **Style**: Classic, warm
- **Colors**: Soft pastels and earth tones

### Festive Celebration
- **Perfect for**: Birthday parties, fun events
- **Style**: Colorful, energetic
- **Colors**: Bright pinks and purples

### Corporate Professional
- **Perfect for**: Business events, conferences
- **Style**: Sophisticated, clean
- **Colors**: Professional grays and blues

## 🛠 Technical Details

### Built With
- **Backend**: Flask (Python web framework)
- **Database**: SQLite (lightweight, no setup required)
- **Frontend**: Bootstrap 5 + Custom CSS
- **Charts**: Chart.js for analytics
- **QR Codes**: Python qrcode library
- **Icons**: Font Awesome

### Database Schema

#### Invitations Table
- Basic event information (title, description, type)
- Date, time, and venue details
- Host contact information
- Design preferences (template, colors)
- Sharing settings and limits

#### RSVPs Table
- Guest information and contact details
- Attendance status and guest count
- Dietary requirements and special requests
- Response timestamp and messages

### File Structure
```
inviteme/
├── app.py                 # Main Flask application
├── migrate_db.py          # Database management script
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Homepage
│   ├── create_invitation.html
│   ├── view_invitation.html
│   ├── manage_invitation.html
│   └── template_gallery.html
├── static/               # Static assets (CSS, JS, images)
└── inviteme.db          # SQLite database (created automatically)
```

## 🔧 Database Management

The `migrate_db.py` script provides easy database management:

```bash
# Initialize database (first time setup)
python migrate_db.py init

# Reset database (delete all data)
python migrate_db.py reset

# Create backup
python migrate_db.py backup

# Restore from backup
python migrate_db.py restore

# Check database status
python migrate_db.py status
```

## 🌟 Key Features in Detail

### Real-time Analytics
- **Live Updates**: RSVP counts update automatically
- **Visual Charts**: Beautiful pie charts showing response breakdown
- **Guest Lists**: Detailed view of all responses with timestamps
- **Export Ready**: Easy to copy guest information

### Mobile-First Design
- **Responsive Layout**: Perfect on phones, tablets, and desktops
- **Touch-Friendly**: Easy navigation on mobile devices
- **Fast Loading**: Optimized for all connection speeds
- **Offline Viewing**: Invitations work without internet once loaded

### Security & Privacy
- **No Registration**: Guests don't need to create accounts
- **Unique URLs**: Each invitation has a secure, unique identifier
- **Local Storage**: All data stored locally, no external tracking
- **Optional Information**: Guests choose what information to share

## 🎯 Use Cases

### Personal Events
- **Weddings**: Elegant invitations with RSVP management
- **Birthday Parties**: Fun designs for all ages
- **Anniversary Celebrations**: Romantic templates
- **Holiday Gatherings**: Seasonal designs

### Professional Events
- **Corporate Meetings**: Professional, clean designs
- **Conferences**: Information-rich layouts
- **Team Building**: Casual, friendly styles
- **Product Launches**: Modern, exciting templates

### Family Events
- **Baby Showers**: Sweet, gentle designs
- **Graduations**: Achievement-focused templates
- **Reunions**: Nostalgic, warm styles
- **Milestone Birthdays**: Special celebration designs

## 🚀 Deployment Options

### Local Development
- Perfect for personal use
- No external dependencies
- Run on your computer

### Cloud Deployment
- Deploy to Heroku, PythonAnywhere, or similar
- Add custom domain
- Scale for larger events

### Self-Hosted
- Run on your own server
- Full control over data
- Customize as needed

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Found an issue? Let us know!
2. **Suggest Features**: Have ideas for improvements?
3. **Submit Code**: Fork, improve, and submit pull requests
4. **Improve Documentation**: Help make the docs better
5. **Share Templates**: Create new invitation designs

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Why Choose InviteMe?

### ✅ **Completely Free**
- No subscription fees
- No hidden costs
- No feature limitations

### ✅ **No Registration Required**
- Start creating immediately
- Guests RSVP without accounts
- Privacy-focused approach

### ✅ **Beautiful & Professional**
- Designer-quality templates
- Mobile-responsive design
- Professional appearance

### ✅ **Easy to Use**
- Intuitive interface
- Quick setup process
- Instant sharing

### ✅ **Powerful Features**
- Real-time analytics
- QR code generation
- Social media integration
- Detailed guest management

---

**Made with ❤️ for celebrations everywhere**

*InviteMe - Where every invitation is perfect*