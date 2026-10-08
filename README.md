# Emergency Contact Management Application

A simple and attractive web application for managing emergency and
important contacts. The application allows users to register, log in,
save family and emergency contacts, edit or delete contacts, search
contacts, and directly call saved numbers using the device's phone
functionality.

## Project Overview

**Project Name:** Emergency Contact Management Application

**Technology Stack:** - Frontend: HTML, CSS, JavaScript - Backend:
Python Flask - Database: MongoDB - Template Engine: Jinja2 - Password
Security: Werkzeug password hashing - Calling: HTML `tel:` links

## Main Features

### 1. User Registration

Users can create an account using: - Full name - Email address - Phone
number - Password - Confirm password

Passwords are stored using secure password hashing.

### 2. User Login and Logout

Registered users can: - Log in using email and password - Stay
authenticated using Flask sessions - Log out securely

### 3. Dashboard

The dashboard provides quick access to: - Family Contacts - Emergency
Contacts - Emergency Services - User Profile - Important emergency
numbers - Recently saved contacts

### 4. Family Contacts

Users can: - Add family members - Select their relationship - Save phone
numbers - View saved family contacts - Search contacts - Edit contacts -
Delete contacts - Directly call contacts

Supported relationships include: - Father - Mother - Brother - Sister -
Grandfather - Grandmother - Uncle - Aunt - Other

### 5. Emergency Contacts

Users can save important people and organizations such as: - Doctors -
Teachers - Hospitals - Workplace contacts - Friends - Neighbours - Other
contacts

Each contact can be: - Added - Searched - Edited - Deleted - Directly
called

### 6. Emergency Numbers

The application provides quick access to important emergency services:

  Service                Number
  -------------------- --------
  Police                    100
  Ambulance                 108
  Fire Brigade              101
  National Emergency        112

The numbers use `tel:` links so they can be dialed directly from a
supported device.

### 7. Search

Search functionality is available for: - Family contacts - Emergency
contacts

The search works instantly using JavaScript and checks the information
displayed in each contact card.

### 8. Profile

The profile page displays the logged-in user's: - Name - Email - Phone
number

It also provides access to logout and dashboard navigation.

### 9. Edit and Delete

Users can edit or delete their own saved family and emergency contacts.

Database operations are restricted using the logged-in user's session ID
so that users only access their own contacts.

## Project Structure

``` text
EmergencyContactManager/
│
├── app.py
├── requirements.txt
│
├── templates/
│   ├── navbar.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── family_contacts.html
│   ├── emergency_contacts.html
│   ├── emergency_numbers.html
│   ├── profile.html
│   ├── edit_family_contact.html
│   └── edit_emergency_contact.html
│
└── static/
    └── css/
        └── style.css
```

## Database Structure

The application uses MongoDB.

### Database

``` text
emergency_contact_db
```

### Collections

``` text
users
family_contacts
emergency_contacts
```

### Users Collection

Example document:

``` json
{
    "name": "Shivam Patil",
    "email": "user@example.com",
    "phone": "9876543210",
    "password": "hashed_password"
}
```

### Family Contacts Collection

Example document:

``` json
{
    "user_id": "user_object_id",
    "name": "Mother",
    "relationship": "Mother",
    "phone": "9876543210"
}
```

### Emergency Contacts Collection

Example document:

``` json
{
    "user_id": "user_object_id",
    "name": "Dr. Sharma",
    "category": "Doctor",
    "phone": "9876543210"
}
```

## Requirements

Install the following software:

-   Python 3.x
-   MongoDB Community Server
-   MongoDB Compass (optional)
-   VS Code or another code editor
-   A modern web browser

## Python Packages

The project uses:

``` text
Flask
pymongo
Werkzeug
```

These are listed in `requirements.txt`.

## Installation

### Step 1: Download or Clone the Project

Open the project folder in VS Code.

### Step 2: Create a Virtual Environment

Windows:

``` bash
python -m venv venv
```

Activate it:

``` bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

Run:

``` bash
pip install -r requirements.txt
```

Or install them individually:

``` bash
pip install Flask pymongo Werkzeug
```

### Step 4: Start MongoDB

Make sure MongoDB is running locally.

The application connects using:

``` text
mongodb://localhost:27017/
```

The database and collections are created automatically when data is
inserted.

### Step 5: Run the Flask Application

Run:

``` bash
python app.py
```

The application will normally be available at:

``` text
http://127.0.0.1:5000
```

## Application Flow

``` text
Register
   ↓
Login
   ↓
Dashboard
   ↓
 ┌───────────────┬──────────────────┬──────────────────┐
 ↓               ↓                  ↓
Family        Emergency          Emergency
Contacts      Contacts            Numbers
 ↓               ↓                  ↓
Add/Edit/      Add/Edit/          Direct
Delete/Search  Delete/Search      Calling
```

## Navigation

The application uses a common Jinja navigation component:

``` html
{% include 'navbar.html' %}
```

The navigation bar provides links to:

-   Dashboard
-   Family Contacts
-   Emergency Contacts
-   Emergency Numbers
-   Profile
-   Logout

Using a shared navbar keeps the design consistent across the
application.

## Direct Calling

Saved contacts use HTML telephone links:

``` html
<a href="tel:{{ contact.phone }}">
    📞 Call
</a>
```

Emergency services use the same method:

``` html
<a href="tel:{{ service.number }}">
    📞 Call Now
</a>
```

On supported mobile devices, selecting the button opens the phone
dialer.

## Authentication

The application uses Flask sessions to identify logged-in users.

Example:

``` python
session["user_id"] = str(user["_id"])
session["user_name"] = user["name"]
```

Protected pages check whether the user is logged in before displaying
private information.

Passwords are not stored as plain text. They are hashed using Werkzeug:

``` python
generate_password_hash(password)
```

and verified using:

``` python
check_password_hash(...)
```

## UI Design

The application uses: - Responsive layouts - Centered page content -
Cards for contacts and services - Consistent navigation - Search boxes -
Call buttons - Edit and delete buttons - Mobile-friendly styling -
Simple emergency-focused design

The main content uses a common centered container:

``` css
.dashboard-content {
    max-width: 1020px;
    margin: 0 auto;
    padding: 45px 25px;
}
```

This keeps the Dashboard, Family Contacts, Emergency Contacts, and
Emergency Numbers pages visually consistent.

## Security Considerations

The project includes basic security measures suitable for a college
project:

-   Password hashing
-   Session-based authentication
-   Login protection for private pages
-   User-specific MongoDB queries
-   User-specific edit and delete operations
-   Confirmation before deleting contacts

For a production application, additional security measures would be
required, including stronger secret-key management, CSRF protection,
input validation, rate limiting, HTTPS, and production database
security.

## Testing Checklist

The following functions should be tested:

-   [ ] User registration
-   [ ] Duplicate email registration
-   [ ] Password confirmation
-   [ ] User login
-   [ ] Incorrect login credentials
-   [ ] Dashboard access
-   [ ] Add family contact
-   [ ] Search family contact
-   [ ] Edit family contact
-   [ ] Delete family contact
-   [ ] Call family contact
-   [ ] Add emergency contact
-   [ ] Search emergency contact
-   [ ] Edit emergency contact
-   [ ] Delete emergency contact
-   [ ] Call emergency contact
-   [ ] Emergency service call buttons
-   [ ] Profile page
-   [ ] Logout
-   [ ] Protected page access after logout
-   [ ] MongoDB data storage

## Future Improvements

Possible future improvements include: - Contact profile pictures -
Emergency contact priority levels - Location sharing - SMS emergency
alerts - Email notifications - GPS-based emergency assistance -
Emergency alert button - Contact import from phone - Admin panel - Cloud
database deployment - Progressive Web App support

## Author

**Name:** Shivam Patil

## Project Purpose

This application is developed as an academic project to demonstrate the
use of:

-   Python Flask
-   HTML
-   CSS
-   JavaScript
-   MongoDB
-   Jinja templates
-   CRUD operations
-   User authentication
-   Session management
-   Responsive web design

The project focuses on providing a simple and practical way to organize
important emergency contacts and quickly access emergency numbers.
