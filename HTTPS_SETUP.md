# HTTPS Setup Guide for Local Development

This guide explains how to set up HTTPS (SSL/TLS) for your Django application during local development.

## Why HTTPS in Development?

- Test features that require HTTPS (e.g., geolocation, camera access, secure cookies)
- Replicate production environment more accurately
- Test SSL-specific configurations
- Required by some modern browser features

---

## Option 1: Using Django Extensions (Recommended for Development)

### Step 1: Install Required Packages

```bash
pip install django-extensions Werkzeug pyOpenSSL
```

### Step 2: Update settings.py

Add `'django_extensions'` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django_extensions',
]
```

### Step 3: Run Server with SSL

```bash
python manage.py runserver_plus --cert-file cert.crt
```

This will automatically generate a self-signed certificate and run your server over HTTPS.

### Step 4: Access Your Application

Open your browser to: https://localhost:8000

**Note:** You'll see a security warning because it's a self-signed certificate. Click "Advanced" and "Proceed anyway" to continue.

---

## Option 2: Manual Certificate Generation (Windows)

### Step 1: Install OpenSSL

Download and install OpenSSL for Windows:
- Download from: https://slproweb.com/products/Win32OpenSSL.html
- Install the Win64 OpenSSL version
- Add OpenSSL to your system PATH

### Step 2: Generate Private Key

Open Command Prompt in your project directory:

```bash
openssl genrsa -out localhost.key 2048
```

### Step 3: Generate Certificate Signing Request (CSR)

```bash
openssl req -new -key localhost.key -out localhost.csr
```

When prompted, fill in the information:
- Country Name: US
- State: Your State
- Locality: Your City
- Organization: Your School Name
- Common Name: localhost (IMPORTANT)
- Email: your-email@example.com

### Step 4: Generate Self-Signed Certificate

```bash
openssl x509 -req -days 365 -in localhost.csr -signkey localhost.key -out localhost.crt
```

### Step 5: Run Django with SSL

```bash
python manage.py runserver --cert localhost.crt --key localhost.key
```

**Note:** Standard Django runserver doesn't support SSL natively. You'll need to use django-extensions or another WSGI server.

---

## Option 3: Using mkcert (Easiest - Trusted Certificate)

mkcert creates locally-trusted development certificates without browser warnings.

### Step 1: Install mkcert

**Windows:**
```bash
# Using Chocolatey
choco install mkcert

# Or download from: https://github.com/FiloSottile/mkcert/releases
```

**Mac:**
```bash
brew install mkcert
```

**Linux:**
```bash
sudo apt install mkcert
```

### Step 2: Install Local Certificate Authority

```bash
mkcert -install
```

This creates a local certificate authority and installs it in your system trust store.

### Step 3: Generate Certificate for localhost

In your project directory:

```bash
mkcert localhost 127.0.0.1 ::1
```

This creates two files:
- `localhost+2.pem` (certificate)
- `localhost+2-key.pem` (private key)

### Step 4: Install django-extensions

```bash
pip install django-extensions Werkzeug pyOpenSSL
```

Add to `INSTALLED_APPS` in settings.py:

```python
INSTALLED_APPS = [
    ...
    'django_extensions',
]
```

### Step 5: Run Server with SSL

```bash
python manage.py runserver_plus --cert-file localhost+2.pem --key-file localhost+2-key.pem
```

### Step 6: Access Your Application

Open your browser to: https://localhost:8000

**No security warnings!** The certificate is trusted by your browser.

---

## Running on Network with HTTPS

To access HTTPS from other devices on your network:

### Step 1: Find Your IP Address

```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

Look for your IPv4 address (e.g., 192.168.1.100)

### Step 2: Generate Certificate with IP Address

Using mkcert:
```bash
mkcert localhost 127.0.0.1 ::1 192.168.1.100
```

### Step 3: Run Server on All Interfaces

```bash
python manage.py runserver_plus 0.0.0.0:8000 --cert-file localhost+3.pem --key-file localhost+3-key.pem
```

### Step 4: Access from Other Devices

- From the server: https://localhost:8000
- From other devices: https://192.168.1.100:8000

**Note:** Other devices will show security warnings unless you install the mkcert CA certificate on them.

---

## Alternative: Using Gunicorn with SSL (Production-like)

### Step 1: Install Gunicorn

```bash
pip install gunicorn
```

### Step 2: Generate Certificates (using any method above)

### Step 3: Run with Gunicorn

```bash
gunicorn lostandfound.wsgi:application --bind 0.0.0.0:8000 --certfile=localhost.crt --keyfile=localhost.key
```

---

## Troubleshooting

### Browser Shows Security Warning

**For self-signed certificates:** This is normal. Click "Advanced" → "Proceed to localhost"

**For mkcert:** Make sure you ran `mkcert -install` first

### Certificate Not Trusted on Mobile

1. Export the mkcert CA certificate:
```bash
mkcert -CAROOT
```

2. Copy the `rootCA.pem` file to your mobile device
3. Install it as a trusted certificate authority

### "Module not found" Errors

Make sure all packages are installed:
```bash
pip install django-extensions Werkzeug pyOpenSSL
```

### Port Already in Use

Change the port:
```bash
python manage.py runserver_plus 0.0.0.0:8443 --cert-file cert.pem --key-file key.pem
```

---

## Security Notes

⚠️ **Important Reminders:**

1. **Development Only:** Self-signed certificates are for development only
2. **Never Commit Certificates:** Add `*.pem`, `*.crt`, `*.key` to `.gitignore`
3. **Production:** Use Let's Encrypt or a commercial CA for production
4. **Keep Keys Private:** Never share or commit private keys
5. **Firewall:** Ensure your firewall allows HTTPS (port 443 or custom port)

---

## Production Deployment

For production, use proper SSL certificates:

1. **Let's Encrypt (Free):** https://letsencrypt.org/
2. **Commercial CAs:** DigiCert, Sectigo, etc.
3. **Use Nginx/Apache:** As a reverse proxy with SSL termination
4. **Update ALLOWED_HOSTS:** Set to your actual domain in settings.py

Example production settings:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## Quick Reference

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| django-extensions | Quick setup | Browser warnings | Quick testing |
| Manual OpenSSL | Full control | Complex, warnings | Learning SSL |
| mkcert | No warnings, trusted | Extra install | Regular development |
| Gunicorn | Production-like | More setup | Staging environment |

---

## Recommended Approach

For most developers, we recommend **Option 3 (mkcert)** because:
- ✅ No browser security warnings
- ✅ Trusted by your system
- ✅ Easy to set up
- ✅ Works across all localhost apps
- ✅ Can be used on mobile devices

---

## Need Help?

- Django Extensions Docs: https://django-extensions.readthedocs.io/
- mkcert GitHub: https://github.com/FiloSottile/mkcert
- OpenSSL Docs: https://www.openssl.org/docs/
- Django SSL Guide: https://docs.djangoproject.com/en/stable/topics/security/

---

## Update requirements.txt

After installing packages for HTTPS, update your requirements:

```bash
pip freeze > requirements.txt
```

Your requirements.txt should now include:
```
django-extensions>=3.2.0
Werkzeug>=2.3.0
pyOpenSSL>=23.0.0
```
