# 🚀 Quick Installation Commands for PythonAnywhere

## Step 1: Open Bash Console
Go to PythonAnywhere **Consoles** tab and open a **Bash** console.

## Step 2: Navigate to Project Directory
```bash
cd /home/Parth967/inviteme
```

## Step 3: Install Dependencies (Choose ONE method)

### Method A: Using requirements.txt
```bash
pip3.10 install --user -r requirements.txt
```

### Method B: Install packages individually (if Method A fails)
```bash
pip3.10 install --user Flask==2.2.5
pip3.10 install --user Flask-SQLAlchemy==2.5.1
pip3.10 install --user Flask-Login==0.6.3
pip3.10 install --user "qrcode[pil]==7.4.2"
pip3.10 install --user Pillow==10.0.1
pip3.10 install --user Werkzeug==2.2.3
pip3.10 install --user python-dotenv==1.0.0
pip3.10 install --user PyMySQL==1.1.0
```

### Method C: Use deployment script
```bash
python3.10 deploy_pythonanywhere.py
```

## Step 4: Initialize Database
```bash
python3.10 migrate_db.py init
```

## Step 5: Test Application Import
```bash
python3.10 -c "from app import app; print('✅ App imports successfully!')"
```

## Step 6: Configure Web App
1. Go to **Web** tab in PythonAnywhere
2. Set **Source code**: `/home/Parth967/inviteme`
3. Set **Working directory**: `/home/Parth967/inviteme`
4. Click on **WSGI configuration file** and replace content with `wsgi.py`
5. Click **Reload** button

## Step 7: Test Your Site
Visit: `https://parth967.pythonanywhere.com`

---

## 🔧 Troubleshooting

### If you get "No module named 'qrcode'" error:
```bash
pip3.10 install --user qrcode[pil]==7.4.2
```

### If you get database connection errors:
```bash
python3.10 -c "
import pymysql
try:
    conn = pymysql.connect(
        host='Parth967.mysql.pythonanywhere-services.com',
        user='Parth967', 
        password='khushali979797',
        database='Parth967\$inviteme'
    )
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Database error: {e}')
"
```

### If imports still fail:
```bash
python3.10 -c "
import sys
print('Python path:')
for p in sys.path:
    print(f'  {p}')
"
```

### Check installed packages:
```bash
pip3.10 list --user | grep -E "(Flask|qrcode|Pillow|PyMySQL)"
```

---

## 🎯 Quick Fix Commands

If you're getting the Flask-SQLAlchemy import error right now, run these commands in order:

```bash
cd /home/Parth967/inviteme
pip3.10 install --user Flask==2.2.5
pip3.10 install --user Flask-SQLAlchemy==2.5.1
pip3.10 install --user Flask-Login==0.6.3
pip3.10 install --user qrcode[pil]==7.4.2
pip3.10 install --user Pillow==10.0.1
pip3.10 install --user Werkzeug==2.2.3
pip3.10 install --user python-dotenv==1.0.0
pip3.10 install --user PyMySQL==1.1.0
python3.10 migrate_db.py init
```

Then reload your web app in the **Web** tab.

---

**🎉 Your InviteMe platform will be live at: `https://parth967.pythonanywhere.com`**