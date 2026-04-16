# 🚀 HOW TO RUN SANKALP - CSS & STYLING EXPLAINED

## ⚠️ IMPORTANT: DO NOT OPEN HTML FILES DIRECTLY!

### ❌ WRONG
```
Open File Manager
Right-click index.html
Choose "Open with Browser"
Result: Plain HTML, no CSS, no styling
```

### ✅ CORRECT
```
Use Django Development Server
Access through: http://127.0.0.1:8000/
Result: Full styling, CSS, Bootstrap, everything works!
```

---

## 🎨 WHERE IS THE CSS?

The CSS is in THREE places:

### 1️⃣ **Bootstrap 5** (From CDN - Online)
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```
- Professional UI framework
- Responsive design
- Buttons, cards, forms, etc.

### 2️⃣ **Font Awesome Icons** (From CDN - Online)
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```
- Beautiful icons
- Leaf icon, user icons, etc.

### 3️⃣ **Custom CSS** (In Your Project)
```
Location: sankalp/core/static/css/style.css
File Type: Local (650+ lines of custom styling)
```

---

## 🏃 QUICKEST WAY TO RUN

### **Option 1: Use Startup Script (EASIEST)**
Double-click this file:
```
startup.bat
```
Then select option `1` to run server.

### **Option 2: Manual Commands**

**STEP 1**: Open PowerShell  
Press: `Windows Key + R` → Type `powershell` → Enter

**STEP 2**: Navigate to project
```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\Sankalp Campus management system"
```

**STEP 3**: Activate virtual environment
```powershell
venv\Scripts\activate
```
(You'll see `(venv)` appear on the left)

**STEP 4**: Go to Django folder
```powershell
cd sankalp
```

**STEP 5**: Run the server
```powershell
python manage.py runserver
```

**STEP 6**: Wait for this message:
```
Starting development server at http://0.0.0.0:8000/
```

**STEP 7**: Open browser and go to:
```
http://127.0.0.1:8000/
```

---

## 📍 WHAT YOU'LL SEE

### At http://127.0.0.1:8000/ (HOME PAGE)
✅ Beautiful green navigation bar  
✅ SANKALP logo with leaf icon  
✅ Hero section with information  
✅ Statistics cards  
✅ Professional colors and fonts  
✅ Responsive buttons  
✅ Proper spacing and layout  

### At http://127.0.0.1:8000/login
✅ Styled login form  
✅ Role selector (Student/Teacher/Admin)  
✅ Password toggle button  
✅ Beautiful card design  
✅ Error messages with colors  

### At http://127.0.0.1:8000/dashboard
✅ Statistics cards with icons  
✅ Table with complaints  
✅ Status badges with colors  
✅ Responsive design  

---

## 📂 FILE STRUCTURE

```
Sankalp Project/
│
├── startup.bat                          ← USE THIS!
├── startup.sh
│
├── sankalp/
│   ├── manage.py                        ← RUN: python manage.py runserver
│   ├── db.sqlite3
│   │
│   ├── sankalp/
│   │   └── settings.py                  ← Configuration
│   │
│   └── core/
│       ├── static/                      ← Static files folder
│       │   ├── css/
│       │   │   └── style.css            ← CUSTOM CSS (650+ lines) ✅
│       │   │
│       │   └── js/
│       │       └── script.js            ← JavaScript (400+ lines) ✅
│       │
│       └── templates/                   ← HTML Templates folder
│           ├── base.html                ← Master template (has CSS links)
│           ├── index.html               ← Home page
│           ├── login.html               ← Login page
│           ├── dashboard.html           ← Student dashboard
│           └── ... more templates
```

---

## 🎨 CSS IS INCLUDED - Proof

Open: `sankalp/core/templates/base.html`

You'll see at the top:
```html
<!-- Bootstrap CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Font Awesome Icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- Custom CSS -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

All CSS is there! You just need to run Django server to see it.

---

## ⚡ QUICK COMMANDS REFERENCE

```powershell
# Navigate to project
cd "c:\Users\LENOVO\OneDrive\Desktop\Sankalp Campus management system"

# Activate environment
venv\Scripts\activate

# Enter Django folder
cd sankalp

# Run server (THIS IS THE KEY COMMAND!)
python manage.py runserver

# Then open browser
http://127.0.0.1:8000/

# To STOP server
Ctrl + C (in PowerShell)
```

---

## 🪟 WINDOWS-SPECIFIC STEPS

### Method 1: Use Startup Script (BEST)
1. Navigate to project folder
2. Double-click `startup.bat`
3. Select option `1`
4. Open browser to `http://127.0.0.1:8000/`

### Method 2: PowerShell (STEP-BY-STEP)
1. Right-click on empty space in project folder
2. Click "Open PowerShell window here"
3. Type: `venv\Scripts\activate`
4. Type: `cd sankalp`
5. Type: `python manage.py runserver`
6. Open browser to `http://127.0.0.1:8000/`

### Method 3: Command Prompt
1. Press `Windows + R`
2. Type `cmd`
3. Type: `cd "c:\Users\LENOVO\OneDrive\Desktop\Sankalp Campus management system"`
4. Type: `venv\Scripts\activate`
5. Type: `cd sankalp`
6. Type: `python manage.py runserver`

---

## ✅ HOW TO KNOW IT'S WORKING

When you run the server, you'll see:
```
Performing system checks...
System check identified no issues (0 silenced).
April 11, 2026 - XX:XX:XX
Django version 6.0.3, using settings 'sankalp.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
```

Then open http://127.0.0.1:8000/ in browser and you'll see:
- ✅ Beautiful styled homepage
- ✅ Green navigation bar with logo
- ✅ Icons and proper fonts
- ✅ Responsive design
- ✅ All CSS working perfectly

---

## 🔐 LOGIN CREDENTIALS

After server is running, go to http://127.0.0.1:8000/login

```
Username: student1
Password: password123
Role: Student
```

Or try with admin account:
```
Username: admin
Password: admin123
Role: Admin
```

---

## ❌ COMMON MISTAKES TO AVOID

### ❌ Mistake 1: Opening HTML file directly
```
DON'T: Double-click index.html
```

### ❌ Mistake 2: Not activating virtual environment
```
DON'T: Run python without (venv) showing
```

### ❌ Mistake 3: Running from wrong folder
```
DON'T: Run from Desktop/Sankalp folder
DO: Navigate to Desktop/Sankalp/sankalp folder
```

### ❌ Mistake 4: Ignoring error messages
```
DO: Read error messages in PowerShell
DO: Check TROUBLESHOOTING.md if error occurs
```

---

## ✅ CORRECT PROCESS

```
1. Open PowerShell
2. Navigate to project folder
3. Activate virtual environment (venv\Scripts\activate)
4. Go to sankalp folder (cd sankalp)
5. Run server (python manage.py runserver)
6. Open browser to http://127.0.0.1:8000/
7. See beautiful styled website with CSS
8. Login with student1 / password123
9. Explore the complete application!
```

---

## 🎯 SUMMARY

| What | How |
|------|-----|
| CSS Included? | ✅ YES (Bootstrap + Custom 650+ lines) |
| How to View? | Run Django server, open http://127.0.0.1:8000/ |
| Which File to Run? | `startup.bat` (Windows) or `python manage.py runserver` |
| Why No CSS When Opening HTML? | Django templates need server, CSS links need server |
| Is Project Broken? | ❌ NO - Just need to run with Django server |

---

**Key Takeaway**: This is a DJANGO PROJECT, not plain HTML files. Always run through Django server to see all styling, CSS, and features working perfectly!

**Last Updated**: April 11, 2026
