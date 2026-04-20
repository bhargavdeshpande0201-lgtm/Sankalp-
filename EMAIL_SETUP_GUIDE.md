# Email Configuration Guide for Password Reset

## Overview
The password reset feature uses Django's email system to send password reset links to users. This guide explains how the system works and how to configure it for different email services.

---

## How Password Reset Works

### 1. User Initiates Password Reset
- User clicks "Forgot Password?" link on login page
- Enters their email address
- System validates that the email exists in the database

### 2. Secure Token Generation
- A random, secure token is generated: `secrets.token_urlsafe(32)`
- Token is stored in the user's session
- Token expires after **1 hour** for security
- User receives an email with a reset link containing their User ID and token

### 3. User Clicks Reset Link
- User clicks the unique reset link from the email
- Link format: `http://yourdomain.com/reset-password/[user_id]/[token]`
- System verifies the token matches the stored session token
- If valid, user can enter a new password

### 4. Password Update
- User enters new password twice
- Password is validated:
  - Minimum 8 characters
  - Must contain at least 1 number
  - Both entries must match
- Password is updated in the database using `set_password()` (securely hashed)
- Session token is cleared

---

## Current Configuration

### Development Mode (Default)
**Current Setting:** `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

**Purpose:** For testing and development
- Emails are printed to the Django console/terminal
- No actual email is sent
- Perfect for testing the flow without email credentials
- Useful for debugging

**How to Test:**
1. Run the development server
2. Click "Forgot Password?" and enter an email
3. Check the terminal/console for the email content and reset link
4. Copy the reset link URL and test it in your browser

---

## Production Email Configuration

Choose one of the following options based on your hosting and requirements:

### Option 1: Gmail SMTP (easiest for small deployments)

**Setup Steps:**

1. **Enable 2-Factor Authentication in Google Account:**
   - Go to https://myaccount.google.com/
   - Click "Security" in the left menu
   - Enable "2-Step Verification"

2. **Create App-Specific Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your machine)
   - Google will generate a 16-character password

3. **Update settings.py:**

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # 16-character app password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

**Security Note:** Store credentials in environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
```

Create `.env` file:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

---

### Option 2: SendGrid (recommended for production)

**Setup Steps:**

1. **Create SendGrid Account:**
   - Go to https://sendgrid.com/
   - Sign up for a free account

2. **Get API Key:**
   - Go to Settings → API Keys
   - Create a new API key (Full Access)

3. **Install Package:**
```bash
pip install sendgrid
pip install django-sendgrid-v5
```

4. **Update settings.py:**

```python
# Email Configuration
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

5. **Create .env file:**
```
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxx
```

---

### Option 3: AWS SES (for AWS users)

**Setup Steps:**

1. **Create AWS Account and verify email:**
   - Go to AWS Console → SES Service
   - Verify your sending email address

2. **Get AWS Credentials:**
   - Create IAM user with SES permissions
   - Get Access Key ID and Secret Access Key

3. **Install Package:**
```bash
pip install django-ses
pip install boto3
```

4. **Update settings.py:**

```python
# Email Configuration
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

---

## Testing Email Configuration

### Test Script
Create `test_email.py` in your project root:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sankalp.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

# Test email
subject = 'Test Email - SANKALP Password Reset'
message = 'This is a test email from SANKALP Campus Management System.'
from_email = settings.DEFAULT_FROM_EMAIL
recipient_list = ['test@example.com']  # Change to your test email

try:
    result = send_mail(subject, message, from_email, recipient_list)
    if result:
        print("✓ Email sent successfully!")
    else:
        print("✗ Email failed to send (check console backend output)")
except Exception as e:
    print(f"✗ Error: {str(e)}")
```

**Run the test:**
```bash
python test_email.py
```

### Manual Testing Steps

1. **Start development server:**
```bash
python manage.py runserver
```

2. **Go to login page and click "Forgot Password?"**

3. **Enter an existing user's email** (e.g., student1@example.com)

4. **Check email output:**
   - Console Backend: Check terminal for email content
   - Gmail/SendGrid: Check inbox (may take a few seconds)

5. **Test the reset link:**
   - Copy the reset link from the email
   - Paste it in your browser
   - You should see the password reset form

6. **Complete password reset:**
   - Enter new password (min 8 chars, 1 number)
   - Confirm password
   - Click "Reset Password"
   - You should see success message

---

## Email Requirements

### Form Validation
- Email must exist in the database
- User account must be active

### Password Validation
- Minimum 8 characters
- Must contain at least 1 number (0-9)
- Both password entries must match exactly
- Password is case-sensitive

### Token Security
- Token expires after 1 hour
- Token is cryptographically secure (32 bytes, URL-safe)
- Token is stored in session (not database)
- Token is cleared after successful reset

---

## Troubleshooting

### Emails Not Sending

**Check if email is enabled:**
```python
# In Django shell
python manage.py shell
>>> from django.conf import settings
>>> print(settings.EMAIL_BACKEND)
>>> print(settings.DEFAULT_FROM_EMAIL)
```

**For Gmail:**
- ✓ 2-Factor Authentication must be enabled
- ✓ Use App-specific password (not regular password)
- ✓ Allow "Less secure app access" (if not using app password)
- ✓ Check that app password is correct (no spaces)
- ✓ Verify port is 587 and TLS is enabled

**For SendGrid:**
- ✓ API key must be valid and not expired
- ✓ API key must have email sending permissions
- ✓ Domain must be verified in SendGrid dashboard

**For AWS SES:**
- ✓ Email must be verified in SES console
- ✓ AWS credentials must have SES:SendEmail permission
- ✓ Account must not be in sandbox mode (for production)

### Reset Link Not Working

- ✓ Check if reset link was copied correctly
- ✓ Verify token hasn't expired (1 hour limit)
- ✓ Check that User ID in URL matches a valid user
- ✓ Verify browser can access the reset-password URL

### Token Mismatch Error

- ✓ User may have opened reset link in different browser/device
- ✓ Session may have been cleared (new tab, cleared cookies, etc.)
- ✓ Token may be expired (> 1 hour old)
- Solution: User should request a new reset email

---

## Code Implementation Details

### Key Files Modified

**views.py:**
```python
# Password reset view functions
- forgot_password(request)  # Handles email submission
- reset_password(request, user_id, token)  # Handles password update

# Security features:
- secrets.token_urlsafe(32) - cryptographically secure token
- Session-based token storage - no database changes needed
- Token expiry - 3600 seconds (1 hour)
- set_password() - Django's secure password hashing
```

**forms.py:**
```python
# Form validation
- PasswordResetRequestForm - validates email exists
- PasswordResetForm - validates password strength and confirmation
```

**urls.py:**
```python
# Routes
- path('forgot-password', views.forgot_password, name='forgot_password')
- path('reset-password/<int:user_id>/<str:token>', views.reset_password)
```

**templates:**
- `forgot_password.html` - email submission form
- `reset_password.html` - password reset form
- `login.html` - updated with "Forgot Password?" link

---

## Security Considerations

✓ **Token Security:**
- 32-byte cryptographically secure tokens
- URL-safe encoding
- 1-hour expiration window
- Not stored in database (session only)

✓ **Password Security:**
- Minimum 8 characters required
- Must contain at least 1 number
- Passwords hashed using Django's PBKDF2 algorithm
- User's previous password is not stored in email

✓ **Email Security:**
- Reset link includes specific user ID
- Token is unique per reset request
- Session-based token prevents token reuse
- Email is validated before sending

✓ **Best Practices:**
- Never log passwords in email or console
- Always use TLS for email transmission
- Keep email credentials in environment variables
- Use app-specific passwords for third-party services

---

## Next Steps

1. **Choose your email service** based on your hosting and scale
2. **Configure settings.py** with appropriate credentials
3. **Test the email sending** using the test script
4. **Test the full password reset flow** manually
5. **Monitor email logs** in production

---

## Support

For issues with:
- **Django Email:** https://docs.djangoproject.com/en/stable/topics/email/
- **Gmail:** https://support.google.com/accounts/answer/185833
- **SendGrid:** https://docs.sendgrid.com/
- **AWS SES:** https://docs.aws.amazon.com/ses/

