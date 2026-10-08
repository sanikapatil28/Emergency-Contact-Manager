from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "emergency_contact_secret_key"


# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["emergency_contact_db"]

users_collection = db["users"]
family_collection = db["family_contacts"]
emergency_collection = db["emergency_contacts"]


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return redirect(url_for("login"))


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match!"

        existing_user = users_collection.find_one({"email": email})

        if existing_user:
            return "Email already registered!"

        user = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": generate_password_hash(password)
        }

        users_collection.insert_one(user)

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):

            session["user_id"] = str(user["_id"])
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        return "Invalid email or password!"

    return render_template("login.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    family_contacts = list(
        family_collection.find(
            {"user_id": session["user_id"]}
        ).limit(4)
    )

    emergency_contacts = list(
        emergency_collection.find(
            {"user_id": session["user_id"]}
        ).limit(4)
    )

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        family_contacts=family_contacts,
        emergency_contacts=emergency_contacts
    )


# =========================
# FAMILY CONTACTS
# =========================

@app.route("/family-contacts", methods=["GET", "POST"])
def family_contacts():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]
        relationship = request.form["relationship"]
        phone = request.form["phone"]

        contact = {
            "user_id": session["user_id"],
            "name": name,
            "relationship": relationship,
            "phone": phone
        }

        family_collection.insert_one(contact)

        return redirect(url_for("family_contacts"))

    contacts = list(
        family_collection.find({
            "user_id": session["user_id"]
        })
    )

    return render_template(
        "family_contacts.html",
        contacts=contacts
    )


# =========================
# DELETE FAMILY CONTACT
# =========================

@app.route("/delete-family-contact/<contact_id>")
def delete_family_contact(contact_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    family_collection.delete_one({
        "_id": ObjectId(contact_id),
        "user_id": session["user_id"]
    })

    return redirect(url_for("family_contacts"))

# =========================
# EMERGENCY CONTACTS
# =========================

@app.route("/emergency-contacts", methods=["GET", "POST"])
def emergency_contacts():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        phone = request.form["phone"]

        contact = {
            "user_id": session["user_id"],
            "name": name,
            "category": category,
            "phone": phone
        }

        emergency_collection.insert_one(contact)

        return redirect(url_for("emergency_contacts"))

    contacts = list(
        emergency_collection.find({
            "user_id": session["user_id"]
        })
    )

    return render_template(
        "emergency_contacts.html",
        contacts=contacts
    )


# =========================
# DELETE EMERGENCY CONTACT
# =========================

@app.route("/delete-emergency-contact/<contact_id>")
def delete_emergency_contact(contact_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    emergency_collection.delete_one({
        "_id": ObjectId(contact_id),
        "user_id": session["user_id"]
    })

    return redirect(url_for("emergency_contacts"))
    # =========================
# EMERGENCY NUMBERS
# =========================

@app.route("/emergency-numbers")
def emergency_numbers():

    if "user_id" not in session:
        return redirect(url_for("login"))

    emergency_services = [
        {
            "name": "Police",
            "number": "100",
            "icon": "👮",
            "description": "For police and law enforcement emergencies."
        },
        {
            "name": "Ambulance",
            "number": "108",
            "icon": "🚑",
            "description": "For medical emergencies and ambulance services."
        },
        {
            "name": "Fire Brigade",
            "number": "101",
            "icon": "🚒",
            "description": "For fire and rescue emergencies."
        },
        {
            "name": "National Emergency",
            "number": "112",
            "icon": "🆘",
            "description": "Single emergency number for immediate assistance."
        }
    ]

    return render_template(
        "emergency_numbers.html",
        services=emergency_services
    )
    # =========================
# PROFILE
# =========================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = users_collection.find_one({
        "_id": ObjectId(session["user_id"])
    })

    if not user:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        user=user
    )
    # =========================
# EDIT FAMILY CONTACT
# =========================

@app.route("/edit-family-contact/<contact_id>", methods=["GET", "POST"])
def edit_family_contact(contact_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    contact = family_collection.find_one({
        "_id": ObjectId(contact_id),
        "user_id": session["user_id"]
    })

    if not contact:
        return "Contact not found!"

    if request.method == "POST":

        family_collection.update_one(
            {
                "_id": ObjectId(contact_id),
                "user_id": session["user_id"]
            },
            {
                "$set": {
                    "name": request.form["name"],
                    "relationship": request.form["relationship"],
                    "phone": request.form["phone"]
                }
            }
        )

        return redirect(url_for("family_contacts"))

    return render_template(
        "edit_family_contact.html",
        contact=contact
    )


# =========================
# EDIT EMERGENCY CONTACT
# =========================

@app.route("/edit-emergency-contact/<contact_id>", methods=["GET", "POST"])
def edit_emergency_contact(contact_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    contact = emergency_collection.find_one({
        "_id": ObjectId(contact_id),
        "user_id": session["user_id"]
    })

    if not contact:
        return "Contact not found!"

    if request.method == "POST":

        emergency_collection.update_one(
            {
                "_id": ObjectId(contact_id),
                "user_id": session["user_id"]
            },
            {
                "$set": {
                    "name": request.form["name"],
                    "category": request.form["category"],
                    "phone": request.form["phone"]
                }
            }
        )

        return redirect(url_for("emergency_contacts"))

    return render_template(
        "edit_emergency_contact.html",
        contact=contact
    )
# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)