# Week 1: Setup + Authentication - Technical Tasks

**Duration:** Nov 23 - Nov 29 (7 days)  
**Goal:** Working Django project with complete user authentication system  
**Team:** 3 Developers

---

## 📦 DEVELOPER 1: BACKEND LEAD

### Task 1.1: Django Project Setup
**Time:** 2 hours  
**Priority:** Critical

**Objectives:**
- Create new Django project and apps
- Configure project settings
- Setup database connections
- Verify basic project runs

**Steps:**
- [ ] Create virtual environment and activate it
- [ ] Install Django and required packages (Pillow, psycopg2)
- [ ] Create Django project named "lostandfound"
- [ ] Create 3 apps: `accounts`, `items`, `claims`
- [ ] Add apps to INSTALLED_APPS in settings.py
- [ ] Configure DATABASES (SQLite for now)
- [ ] Configure MEDIA_ROOT and MEDIA_URL for file uploads
- [ ] Configure STATIC_ROOT and STATIC_URL
- [ ] Set ALLOWED_HOSTS for local development
- [ ] Create requirements.txt with all dependencies
- [ ] Test: Run `python manage.py runserver` - should work

**Deliverables:**
- Working Django project structure
- All apps registered
- Server runs without errors

**Validation:**
- Visit http://localhost:8000 - see Django welcome page

---

### Task 1.2: Custom User Model Design
**Time:** 3 hours  
**Priority:** Critical

**Objectives:**
- Extend Django's default User model
- Create separate profiles for Students and Teachers
- Setup user type differentiation

**Database Logic:**

**User Model (extend AbstractUser):**
- Keep default fields: username, email, password, first_name, last_name
- Add: user_type (choices: 'student', 'teacher', 'admin')
- Add: is_active, date_joined (already in AbstractUser)

**StudentProfile Model (OneToOne with User):**
- user (OneToOneField to User)
- student_id (CharField, will be encrypted)
- grade (IntegerField, choices 1-12)
- created_at (auto)

**TeacherProfile Model (OneToOne with User):**
- user (OneToOneField to User)
- department (CharField, optional, max_length=100)
- created_at (auto)

**Steps:**
- [ ] Create CustomUser model in accounts/models.py extending AbstractUser
- [ ] Add USER_TYPE_CHOICES: student, teacher, admin
- [ ] Add user_type field with choices
- [ ] Create StudentProfile model with OneToOne relationship
- [ ] Add student_id field (CharField for now, encryption later)
- [ ] Add grade field with choices (1-12)
- [ ] Create TeacherProfile model with OneToOne relationship
- [ ] Add department field (optional)
- [ ] Set AUTH_USER_MODEL in settings.py
- [ ] Create migrations
- [ ] Run migrations
- [ ] Test: Create user in shell - should work

**Deliverables:**
- CustomUser model working
- StudentProfile and TeacherProfile models
- Migrations created and applied

**Validation:**
- Open Django shell: `User.objects.create_user()` works
- Can create student/teacher profiles

---

### Task 1.3: Registration Views (Backend Logic)
**Time:** 4 hours  
**Priority:** Critical

**Objectives:**
- Create separate registration views for students and teachers
- Handle form submission and validation
- Create user accounts with appropriate profiles
- Handle errors gracefully

**Registration Logic:**

**Student Registration Flow:**
1. User submits form with: username, email, password, first_name, last_name, student_id, grade
2. Validate all fields (unique username/email, password strength)
3. Create User object with user_type='student'
4. Create StudentProfile linked to user
5. Save student_id (to be encrypted in Week 3)
6. Save grade
7. Redirect to login page with success message

**Teacher Registration Flow:**
1. User submits form with: username, email, password, first_name, last_name, department (optional)
2. Validate all fields
3. Create User object with user_type='teacher'
4. Create TeacherProfile linked to user
5. Save department if provided
6. Redirect to login page with success message

**Steps:**
- [ ] Create StudentRegistrationView in accounts/views.py
- [ ] Handle GET: Display empty form
- [ ] Handle POST: Validate and create student user + profile
- [ ] Validate: username unique, email unique, password min 8 chars
- [ ] Create user with user_type='student'
- [ ] Create StudentProfile automatically
- [ ] Add success message
- [ ] Create TeacherRegistrationView
- [ ] Handle GET: Display empty form
- [ ] Handle POST: Validate and create teacher user + profile
- [ ] Create user with user_type='teacher'
- [ ] Create TeacherProfile automatically
- [ ] Add error handling for all validations
- [ ] Redirect to login after success

**Deliverables:**
- Two working registration views
- Users created with correct type
- Profiles auto-created

**Validation:**
- Submit student form → user created with student profile
- Submit teacher form → user created with teacher profile
- Duplicate username → error shown

---

### Task 1.4: Login/Logout Functionality
**Time:** 2 hours  
**Priority:** Critical

**Objectives:**
- Implement login view with authentication
- Implement logout functionality
- Handle authentication errors
- Redirect users appropriately

**Login Logic:**
1. User submits username and password
2. Authenticate credentials against database
3. If valid: Create session, redirect to home page
4. If invalid: Show error message
5. If account inactive: Show error message

**Steps:**
- [ ] Create LoginView in accounts/views.py
- [ ] Handle GET: Display login form
- [ ] Handle POST: Authenticate user
- [ ] Use Django's authenticate() function
- [ ] Check if user exists and password correct
- [ ] If valid: Call login() to create session
- [ ] Redirect to home page after successful login
- [ ] If invalid: Show "Invalid credentials" error
- [ ] Create LogoutView
- [ ] Call logout() to destroy session
- [ ] Redirect to login page with message
- [ ] Add login_required decorator for protected views

**Deliverables:**
- Working login view
- Working logout view
- Session management working

**Validation:**
- Login with valid credentials → redirects to home
- Login with invalid credentials → shows error
- Logout → session destroyed, redirected to login

---

### Task 1.5: URL Configuration
**Time:** 1 hour  
**Priority:** Critical

**Objectives:**
- Setup URL routing for all authentication views
- Create clean, RESTful URL structure

**URLs Needed:**
```
/register/student/    → StudentRegistrationView
/register/teacher/    → TeacherRegistrationView
/login/              → LoginView
/logout/             → LogoutView
/                    → Home page (placeholder for now)
```

**Steps:**
- [ ] Create accounts/urls.py
- [ ] Add path for student registration
- [ ] Add path for teacher registration
- [ ] Add path for login
- [ ] Add path for logout
- [ ] Include accounts.urls in main urls.py
- [ ] Create temporary home page view
- [ ] Add path for home page (/)
- [ ] Test all URLs resolve correctly

**Deliverables:**
- All URLs working
- No 404 errors on defined paths

**Validation:**
- Visit each URL → correct view loads

---

## 🎨 DEVELOPER 2: FRONTEND LEAD

### Task 2.1: Base Template Structure
**Time:** 3 hours  
**Priority:** Critical

**Objectives:**
- Create base HTML template with Bootstrap
- Design navigation bar
- Setup template inheritance structure
- Ensure responsive design

**Template Structure:**

**base.html:**
- HTML5 doctype
- Bootstrap 5 CDN links
- Navigation bar with logo and menu items
- Main content block (for child templates)
- Footer
- Messages display area
- Responsive meta tags

**Navigation Items:**
- Logo/Brand (links to home)
- Home
- Search Items
- Report Item (if logged in as teacher)
- My Items (if logged in as teacher)
- My Claims (if logged in as student)
- Admin (if logged in as admin)
- Login/Register (if not logged in)
- Profile + Logout (if logged in)

**Steps:**
- [ ] Create templates/base.html
- [ ] Add Bootstrap 5 CSS CDN link in head
- [ ] Add Bootstrap 5 JS CDN link before closing body
- [ ] Create responsive navbar using Bootstrap
- [ ] Add brand/logo area (text for now)
- [ ] Add navigation menu items
- [ ] Use Django template tags for conditional menu items ({% if user.is_authenticated %})
- [ ] Create main content block {% block content %}
- [ ] Add messages display area using Bootstrap alerts
- [ ] Create simple footer with copyright
- [ ] Add Font Awesome CDN for icons
- [ ] Test responsiveness on mobile, tablet, desktop

**Deliverables:**
- Responsive base template
- Working navigation
- Template blocks defined

**Validation:**
- Base template loads without errors
- Nav items show/hide based on login status
- Mobile menu works (hamburger icon)

---

### Task 2.2: Registration Forms Design
**Time:** 4 hours  
**Priority:** Critical

**Objectives:**
- Create student registration form page
- Create teacher registration form page
- Style forms with Bootstrap
- Add client-side validation

**Form Design Requirements:**

**Student Registration Form:**
- Fields: First Name, Last Name, Username, Email, Student ID, Grade (dropdown 1-12), Password, Confirm Password
- All fields required except department
- Inline validation hints
- Clear labels and placeholders
- Bootstrap styling (form-control classes)
- Submit button (primary color)
- Link to login page
- Link to teacher registration

**Teacher Registration Form:**
- Fields: First Name, Last Name, Username, Email, Department (optional), Password, Confirm Password
- Similar styling to student form
- Link to student registration

**Steps:**
- [ ] Create templates/accounts/register_student.html
- [ ] Extend base.html
- [ ] Create form with all required fields
- [ ] Use Bootstrap form classes (form-control, form-label)
- [ ] Add placeholder text for each field
- [ ] Add grade dropdown with options 1-12
- [ ] Add password requirements hint (min 8 chars)
- [ ] Add confirm password field
- [ ] Style submit button as btn btn-primary
- [ ] Add link to "Register as Teacher" and "Login"
- [ ] Create templates/accounts/register_teacher.html
- [ ] Copy structure from student form
- [ ] Replace student_id and grade with department field
- [ ] Make department optional (placeholder: "Optional")
- [ ] Add links to student registration and login
- [ ] Test forms display correctly

**Deliverables:**
- Two styled registration forms
- Responsive form layout
- Clear user guidance

**Validation:**
- Forms display properly
- All fields visible and styled
- Links work correctly

---

### Task 2.3: Login Page Design
**Time:** 2 hours  
**Priority:** Critical

**Objectives:**
- Create clean, professional login page
- Add form validation styling
- Include helpful user guidance

**Login Page Design:**
- Centered login card/panel
- Username field
- Password field
- "Remember me" checkbox (optional)
- Login button (large, primary color)
- Links: "Register as Student" | "Register as Teacher"
- Forgot password link (disabled for now, placeholder)
- Clean, minimal design
- Bootstrap card component

**Steps:**
- [ ] Create templates/accounts/login.html
- [ ] Extend base.html
- [ ] Create centered container (Bootstrap container)
- [ ] Use Bootstrap card for login form
- [ ] Add card header with "Login" title
- [ ] Create form with username and password fields
- [ ] Use form-control classes for inputs
- [ ] Add login button (btn btn-primary btn-lg)
- [ ] Add links to registration pages below form
- [ ] Add "Forgot password?" link (disabled styling)
- [ ] Center card on page using flexbox or margin auto
- [ ] Test on different screen sizes

**Deliverables:**
- Professional login page
- Responsive design
- Clear call-to-action

**Validation:**
- Login page displays centered
- Form fields properly styled
- Links work

---

### Task 2.4: Home Page Layout
**Time:** 3 hours  
**Priority:** High

**Objectives:**
- Create welcoming home page
- Display site purpose and features
- Show recent items (placeholder for now)
- Add call-to-action buttons

**Home Page Design:**

**Hero Section:**
- Large heading: "School Lost & Found"
- Subheading: "Reunite students with their belongings"
- Two buttons: "Search Items" | "Report Found Item"

**Features Section:**
- 3 cards showing key features:
  1. Report Items: Teachers can report found items
  2. Search & Claim: Students can search and claim
  3. Manage: Admins can review and approve

**Recent Items Section (Placeholder):**
- Grid of 4-6 placeholder item cards
- Each card: Image placeholder, Item name, Location, Date

**Steps:**
- [ ] Create templates/home.html
- [ ] Extend base.html
- [ ] Create hero section with jumbotron or custom styling
- [ ] Add main heading and subheading
- [ ] Add two CTA buttons (Search Items, Report Item)
- [ ] Create features section with 3 columns
- [ ] Use Bootstrap cards for each feature
- [ ] Add icons (Font Awesome) for each feature
- [ ] Create recent items section header
- [ ] Add placeholder cards in grid (2 columns on mobile, 3-4 on desktop)
- [ ] Style with Bootstrap grid system
- [ ] Make fully responsive

**Deliverables:**
- Complete home page layout
- Responsive design
- Placeholder content

**Validation:**
- Home page loads
- Buttons link correctly
- Responsive on all devices

---

### Task 2.5: CSS Custom Styling
**Time:** 2 hours  
**Priority:** Medium

**Objectives:**
- Create custom CSS file
- Define color scheme
- Add custom styles beyond Bootstrap
- Ensure consistent branding

**Styling Requirements:**

**Color Scheme:**
- Primary color (buttons, links): Choose school colors or professional blue
- Secondary color: Accent color for highlights
- Success color: Green for approved/success
- Danger color: Red for rejected/errors
- Background: Light gray or white

**Custom Styles:**
- Card shadows and hover effects
- Button hover states
- Form focus states
- Navigation hover effects
- Consistent spacing and padding

**Steps:**
- [ ] Create static/css/style.css
- [ ] Define CSS variables for colors
- [ ] Add custom button styles (hover effects)
- [ ] Style form inputs (focus states, borders)
- [ ] Add card hover effects (subtle shadow increase)
- [ ] Style navigation hover states
- [ ] Add custom spacing utilities if needed
- [ ] Style messages/alerts consistently
- [ ] Link style.css in base.html after Bootstrap
- [ ] Test all custom styles work

**Deliverables:**
- Custom CSS file
- Consistent color scheme
- Enhanced user interactions

**Validation:**
- Custom styles apply correctly
- Colors consistent across pages
- Hover effects work

---

## 🔧 DEVELOPER 3: INTEGRATION & TESTING

### Task 3.1: Project Setup & Version Control
**Time:** 2 hours  
**Priority:** Critical

**Objectives:**
- Initialize Git repository
- Setup .gitignore properly
- Create project documentation
- Setup team collaboration structure

**Git Structure:**

**Branches:**
- main: Production-ready code
- develop: Development branch
- feature branches: Individual features

**Files to Ignore:**
- venv/
- *.pyc
- __pycache__/
- db.sqlite3
- .env
- media/ (except placeholder images)
- .DS_Store

**Steps:**
- [ ] Initialize git repository (git init)
- [ ] Create .gitignore with Python/Django entries
- [ ] Add venv, pyc, pycache, db.sqlite3 to gitignore
- [ ] Create README.md with project description
- [ ] Add setup instructions to README
- [ ] List team members and roles
- [ ] Create develop branch
- [ ] Setup GitHub repository (or GitLab/Bitbucket)
- [ ] Push initial commit to GitHub
- [ ] Invite team members as collaborators
- [ ] Document branching strategy in README

**Deliverables:**
- Git repository initialized
- GitHub repo created
- Team has access
- Documentation started

**Validation:**
- All team members can clone repo
- .gitignore working (no unwanted files)
- README is clear

---

### Task 3.2: Environment Configuration
**Time:** 2 hours  
**Priority:** Critical

**Objectives:**
- Setup environment variables
- Create .env file structure
- Configure settings for development
- Document configuration for team

**Environment Variables Needed:**
- SECRET_KEY (Django secret)
- DEBUG (True/False)
- ALLOWED_HOSTS (comma separated)
- DATABASE_URL (for production later)
- EMAIL settings (for later)

**Steps:**
- [ ] Install python-decouple package
- [ ] Create .env.example file (template with no sensitive data)
- [ ] List all required environment variables
- [ ] Add .env to .gitignore
- [ ] Create each team member's .env file
- [ ] Generate new SECRET_KEY for each environment
- [ ] Configure settings.py to read from .env
- [ ] Use decouple for SECRET_KEY, DEBUG, ALLOWED_HOSTS
- [ ] Test that settings load from .env correctly
- [ ] Document .env setup in README

**Deliverables:**
- .env.example template
- Each dev has working .env
- Settings configured properly

**Validation:**
- Server runs with .env variables
- No hardcoded secrets in code
- .env not in git

---

### Task 3.3: Form Validation Logic
**Time:** 3 hours  
**Priority:** Critical

**Objectives:**
- Implement frontend and backend validation
- Ensure data integrity
- Provide clear error messages
- Prevent invalid submissions

**Validation Rules:**

**Username:**
- Required, 3-20 characters
- Alphanumeric and underscores only
- Must be unique
- Case-insensitive check

**Email:**
- Required, valid email format
- Must be unique
- Case-insensitive check

**Password:**
- Required, minimum 8 characters
- Must contain at least one letter and one number
- Passwords must match (password == confirm_password)

**Student ID:**
- Required for students
- Alphanumeric, 5-10 characters
- Pattern validation

**Grade:**
- Required for students
- Integer between 1-12

**Steps:**
- [ ] Create validation functions in accounts/utils.py
- [ ] Validate username: length, characters, uniqueness
- [ ] Validate email: format, uniqueness
- [ ] Validate password: length, strength, match
- [ ] Validate student_id: format, length
- [ ] Validate grade: range 1-12
- [ ] Add validation to registration views
- [ ] Return specific error messages for each field
- [ ] Add JavaScript validation in forms (optional enhancement)
- [ ] Test each validation rule
- [ ] Test validation error messages display correctly

**Deliverables:**
- Comprehensive validation functions
- Clear error messages
- No invalid data in database

**Validation:**
- Try invalid username → error shown
- Try duplicate email → error shown
- Try weak password → error shown
- Valid data → user created successfully

---

### Task 3.4: User Flow Testing
**Time:** 3 hours  
**Priority:** High

**Objectives:**
- Test complete registration to login flow
- Test error handling
- Verify database entries
- Document any bugs

**Test Scenarios:**

**Student Registration Flow:**
1. Visit /register/student/
2. Fill valid data → submit
3. Check user created in database
4. Check StudentProfile created
5. Redirected to login
6. Login with new credentials
7. Verify session created
8. Access protected page

**Teacher Registration Flow:**
1. Visit /register/teacher/
2. Fill valid data → submit
3. Check user created with user_type='teacher'
4. Check TeacherProfile created
5. Login and verify access

**Error Scenarios:**
1. Duplicate username → error shown
2. Duplicate email → error shown
3. Password mismatch → error shown
4. Invalid student ID format → error shown
5. Invalid grade → error shown

**Steps:**
- [ ] Create test plan document
- [ ] Test student registration with valid data
- [ ] Verify user appears in Django admin
- [ ] Verify StudentProfile created correctly
- [ ] Test teacher registration with valid data
- [ ] Verify TeacherProfile created correctly
- [ ] Test login with new student account
- [ ] Test login with new teacher account
- [ ] Test logout functionality
- [ ] Test each error scenario
- [ ] Verify error messages display correctly
- [ ] Test on different browsers (Chrome, Firefox)
- [ ] Test on mobile device
- [ ] Document all bugs found
- [ ] Create bug tracking spreadsheet

**Deliverables:**
- Complete test results
- Bug list with severity
- Testing documentation

**Validation:**
- All happy paths work
- All error cases handled
- No crashes or 500 errors

---

### Task 3.5: Authentication Decorators & Permissions
**Time:** 2 hours  
**Priority:** High

**Objectives:**
- Setup login_required decorator
- Create custom permission decorators
- Protect views based on user type
- Test access control

**Permission Logic:**

**Protected Views:**
- Report Item: Teachers only
- My Items: Teachers only  
- My Claims: Students only
- Admin Dashboard: Admins only

**Access Control:**
- Unauthenticated users → redirect to login
- Wrong user type → show "Access Denied" message
- Correct user type → allow access

**Steps:**
- [ ] Import login_required from django.contrib.auth.decorators
- [ ] Create custom decorators in accounts/decorators.py
- [ ] Create teacher_required decorator
- [ ] Check if user.user_type == 'teacher'
- [ ] Redirect if not teacher
- [ ] Create student_required decorator
- [ ] Check if user.user_type == 'student'
- [ ] Create admin_required decorator
- [ ] Check if user.is_staff or user.user_type == 'admin'
- [ ] Apply login_required to all protected views
- [ ] Apply user type decorators where needed
- [ ] Test access control for each user type
- [ ] Create "Access Denied" error page (403.html)

**Deliverables:**
- Working permission decorators
- Protected views secured
- Custom error pages

**Validation:**
- Student can't access teacher pages
- Teacher can't access student pages
- Unauthenticated redirected to login
- Proper error messages shown

---

## 📋 Week 1 Checklist Summary

### Critical Path (Must Complete)
- [ ] Django project setup and running
- [ ] User model with student/teacher profiles
- [ ] Student registration working
- [ ] Teacher registration working
- [ ] Login/logout working
- [ ] Base template with navigation
- [ ] Registration forms styled
- [ ] Login page styled
- [ ] Form validation (backend)
- [ ] Access control/permissions

### Important (Should Complete)
- [ ] Home page layout
- [ ] Custom CSS styling
- [ ] Comprehensive testing
- [ ] Git repository setup
- [ ] Environment configuration
- [ ] Error handling
- [ ] Responsive design verified

### Nice to Have (If Time)
- [ ] JavaScript form validation
- [ ] Advanced CSS animations
- [ ] Additional test coverage
- [ ] Performance optimization

---

## 📊 Week 1 Success Metrics

### By End of Week 1:
✅ **Functional:**
- Users can register as student or teacher
- Users can login with credentials
- Users can logout
- Navigation shows correct items based on login status
- Database has users with profiles

✅ **Technical:**
- Django project structure complete
- All apps created and configured
- Database models migrated
- Git repository active with commits

✅ **Design:**
- Base template responsive
- Registration forms styled
- Login page professional
- Home page layout complete

✅ **Quality:**
- No critical bugs
- All validations working
- Error messages clear
- Code committed to Git

---

## 🚨 Week 1 Blockers to Avoid

**Common Issues:**
1. **Migrations fail** → Delete db.sqlite3 and migrations folder, recreate
2. **AUTH_USER_MODEL error** → Set before first migration
3. **Static files not loading** → Check STATIC_URL and run collectstatic
4. **Bootstrap not working** → Verify CDN links, check internet connection
5. **Forms not submitting** → Check CSRF token in template
6. **Git conflicts** → Communicate before pushing, pull before push

**If Stuck:**
- Check Django documentation
- Search error message on Stack Overflow
- Ask team for help in Discord
- Don't spend more than 30 min stuck - ask for help

---

## 📝 Week 1 Deliverables

**Code:**
- Django project with 3 apps
- User authentication system
- Registration views and templates
- Login/logout functionality

**Design:**
- Base template with navigation
- Registration forms
- Login page
- Home page layout

**Documentation:**
- README with setup instructions
- requirements.txt
- .env.example
- Test results

**Git:**
- Initial commit
- Feature branches
- Regular commits
- No sensitive data

---

**Week 1 Motto:** "Build the foundation solid - everything else depends on it!"

**End of Week 1 Goal:** A user can register, login, and see a navigation menu. That's it. Perfect this before moving to Week 2!
