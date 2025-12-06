# GitHub Setup Guide - Uploading Code Without Images/Database

This guide explains how to upload your Lost and Found Django project to GitHub while **excluding** images and database files.

---

## What Gets Excluded (Already Configured in .gitignore)

✅ **Database Files:**
- `db.sqlite3` - Your SQLite database with all records
- `*.db` - Any other database files

✅ **User Uploaded Images:**
- `media/` folder - All uploaded item photos

✅ **Environment Variables:**
- `.env` - Your secret keys and sensitive settings

✅ **Virtual Environment:**
- `venv/` - Python packages (can be reinstalled from requirements.txt)

✅ **Compiled/Cache Files:**
- `__pycache__/` - Python bytecode
- `*.pyc` - Compiled Python files

✅ **Static Files:**
- `staticfiles/` - Collected static files (can be regenerated)

---

## What WILL Be Uploaded (Your Code)

✅ Python source code (`.py` files)
✅ HTML templates
✅ CSS/JavaScript files in `static/` folder
✅ `requirements.txt` - List of dependencies
✅ `README.md` - Documentation
✅ Django migrations (database schema, not data)
✅ Configuration files

---

## Step-by-Step: Upload to GitHub

### Method 1: Using GitHub Desktop (Easiest)

#### 1. Install GitHub Desktop
Download from: https://desktop.github.com/

#### 2. Create Repository on GitHub.com
1. Go to https://github.com
2. Click the **+** icon → **New repository**
3. Name it: `school-lost-and-found` (or your preferred name)
4. Choose **Private** or **Public**
5. **DO NOT** check "Initialize with README" (you already have one)
6. Click **Create repository**

#### 3. Link Your Local Project
1. Open **GitHub Desktop**
2. Click **File** → **Add Local Repository**
3. Browse to: `C:\Users\harsh\OneDrive\Desktop\fbla\lostandfound`
4. Click **Add Repository**
5. If prompted to create a repository, click **Create**

#### 4. Make Your First Commit
1. You'll see all your files listed (images and database should NOT appear)
2. In the **Summary** field, type: `Initial commit - Lost and Found application`
3. Click **Commit to main**

#### 5. Publish to GitHub
1. Click **Publish repository**
2. Confirm the repository name
3. Choose **Private** or **Public**
4. Uncheck "Keep this code private" if you want it public
5. Click **Publish repository**

✅ **Done!** Your code is now on GitHub without images or database!

---

### Method 2: Using Git Command Line

#### 1. Install Git
Download from: https://git-scm.com/download/win

#### 2. Initialize Git Repository
Open Command Prompt in your project folder:

```bash
cd C:\Users\harsh\OneDrive\Desktop\fbla\lostandfound
git init
```

#### 3. Check What Will Be Uploaded
View files that will be tracked:

```bash
git status
```

**Verify that you DON'T see:**
- `db.sqlite3`
- `media/` folder
- `.env` file
- `venv/` folder

If you see any of these, your .gitignore is not working properly.

#### 4. Add All Code Files
```bash
git add .
```

#### 5. Create Your First Commit
```bash
git commit -m "Initial commit - Lost and Found application"
```

#### 6. Create Repository on GitHub
1. Go to https://github.com
2. Click **+** → **New repository**
3. Name: `school-lost-and-found`
4. Choose Private/Public
5. **DO NOT** initialize with README
6. Click **Create repository**

#### 7. Connect Local to GitHub
Copy the commands shown on GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/school-lost-and-found.git
git branch -M main
git push -u origin main
```

Enter your GitHub username and password (or use Personal Access Token).

✅ **Done!** Your code is uploaded!

---

## Verifying Upload (What to Check)

After uploading, visit your GitHub repository and verify:

### ✅ What You SHOULD See:
- [ ] All `.py` files (views.py, models.py, etc.)
- [ ] All templates (.html files)
- [ ] CSS/JavaScript in `static/` folder
- [ ] `requirements.txt`
- [ ] `README.md`
- [ ] Migration files in `*/migrations/`
- [ ] `.gitignore` file

### ❌ What You Should NOT See:
- [ ] `db.sqlite3` file
- [ ] `media/` folder
- [ ] `.env` file
- [ ] `venv/` or `env/` folder
- [ ] `__pycache__/` folders
- [ ] Individual image files (`.jpg`, `.png`)

---

## Future Updates: How to Push Changes

### Using GitHub Desktop:
1. Make changes to your code
2. Open GitHub Desktop
3. You'll see changed files listed
4. Write a commit message (e.g., "Added user approval system")
5. Click **Commit to main**
6. Click **Push origin**

### Using Command Line:
```bash
# See what changed
git status

# Add all changes
git add .

# Commit with message
git commit -m "Added user approval system"

# Push to GitHub
git push
```

---

## Common Issues & Solutions

### Issue 1: "db.sqlite3 is being tracked"

**Solution:**
```bash
# Remove from Git tracking (doesn't delete the file)
git rm --cached db.sqlite3

# Commit the removal
git commit -m "Remove database from tracking"
git push
```

### Issue 2: "media/ folder uploaded by mistake"

**Solution:**
```bash
# Remove from Git tracking
git rm -r --cached media/

# Commit the removal
git commit -m "Remove media files from tracking"
git push
```

### Issue 3: ".env file is visible on GitHub"

**Solution:**
```bash
# Remove from Git
git rm --cached .env

# Commit
git commit -m "Remove .env from tracking"
git push

# IMPORTANT: Change your SECRET_KEY in settings.py immediately!
# Generate new key at: https://djecrety.ir/
```

### Issue 4: "How to check before uploading?"

**Solution:**
```bash
# Dry run - see what would be committed
git add --dry-run .

# See what's staged
git status

# See what's being ignored
git status --ignored
```

---

## Setting Up Project on Another Computer

When someone clones your repository, they'll need to:

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/school-lost-and-found.git
cd school-lost-and-found
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env File
Create `.env` manually with:
```
SECRET_KEY=your-new-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Migrations (Creates Empty Database)
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Create Media Folder
```bash
mkdir media
mkdir media\items
```

### 8. Run Server
```bash
python manage.py runserver
```

**Note:** The database will be empty - no items, no users (except superuser you just created). This is intentional!

---

## Best Practices

### ✅ DO:
- Commit code frequently with clear messages
- Use `.gitignore` to exclude sensitive/large files
- Include `requirements.txt` for dependencies
- Document setup instructions in README
- Keep commits small and focused
- Review changes before pushing

### ❌ DON'T:
- Commit database files
- Commit uploaded images
- Commit `.env` files with secrets
- Commit virtual environment
- Make huge commits with 100+ files
- Push sensitive information (passwords, API keys)

---

## Quick Reference Commands

```bash
# Check repository status
git status

# See what's being ignored
git status --ignored

# View commit history
git log --oneline

# Undo last commit (keeps changes)
git reset --soft HEAD~1

# Discard all local changes
git checkout .

# Pull latest changes from GitHub
git pull

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## GitHub Best Practices for Team Projects

### Branching Strategy:
```bash
# Create feature branch
git checkout -b add-email-notifications

# Make changes, commit
git add .
git commit -m "Add email notification system"

# Push branch
git push -u origin add-email-notifications

# Create Pull Request on GitHub
# After review and merge, delete branch
git checkout main
git pull
git branch -d add-email-notifications
```

### Writing Good Commit Messages:
```
✅ GOOD:
"Add user approval workflow for registration"
"Fix image sizing in recently found items section"
"Update README with HTTPS setup instructions"

❌ BAD:
"fixes"
"update"
"changes"
"asdfasdf"
```

---

## Additional Resources

- **GitHub Docs**: https://docs.github.com/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Learn Git Branching**: https://learngitbranching.js.org/
- **gitignore.io**: https://www.toptal.com/developers/gitignore (Generate .gitignore files)

---

## Emergency: If You Pushed Secrets by Accident

If you accidentally pushed `.env` or database with sensitive data:

1. **Immediately change all passwords/keys**
2. **Remove the file from Git history:**
   ```bash
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch .env" \
   --prune-empty --tag-name-filter cat -- --all

   git push origin --force --all
   ```

3. **Contact GitHub support** to purge caches
4. **Rotate all credentials** that were exposed

**Prevention is better!** Always double-check `git status` before committing.

---

## Summary Checklist

Before pushing to GitHub, verify:

- [ ] `.gitignore` is configured
- [ ] Run `git status` - no db.sqlite3, media/, .env visible
- [ ] `requirements.txt` is up to date
- [ ] README.md has setup instructions
- [ ] Sensitive data is in `.env` (not hardcoded)
- [ ] Commit message is descriptive
- [ ] Repository is set to Private (if needed)

**You're all set!** Your code is safely on GitHub without any images or database records. 🎉
