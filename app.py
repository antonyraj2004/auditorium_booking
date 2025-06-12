import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect("hall_bookings.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hall_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone_no TEXT NOT NULL,
            department TEXT NOT NULL,
            event_name TEXT NOT NULL,
            no_of_days INTEGER NOT NULL,
            date_from TEXT NOT NULL,
            date_to TEXT,
            hall TEXT NOT NULL,
            time_slot TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

@app.route("/")
def home():
    return render_template("index.html")

# Route for the form
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone_no = request.form["phone_no"]
        department = request.form["department"]
        event_name = request.form["event_name"]
        no_of_days = request.form["no_of_days"]
        date_from = request.form["date_from"]
        date_to = request.form["to"]
        hall = request.form["hall"]
        time_slot = request.form["timeSlot"]

        # Insert data into the database
        conn = sqlite3.connect("hall_bookings.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO hall_bookings (name, email, phone_no, department, event_name, no_of_days, date_from, date_to, hall, time_slot)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, phone_no, department, event_name, no_of_days, date_from, date_to, hall, time_slot))
        conn.commit()
        conn.close()

        return redirect(url_for('confirmation'))

    return render_template("form-eg.html")

# Confirmation Page
@app.route("/confirmation")
def confirmation():
    return render_template("confi.html")

@app.route("/booked_slot")
def booked_slot():
    con = sqlite3.connect("hall_bookings.db")
    con.row_factory=sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from hall_bookings")
    con.commit()
    data=cur.fetchall()
    con.close()
    return render_template("table.html",data=data)

# Route to check hall availability
@app.route("/check_availability")
def check_availability():
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    hall = request.args.get("hall")
    time_slot = request.args.get("time_slot")

    if not date_from or not date_to or not hall or not time_slot:
        return jsonify({"error": "Missing required parameters"}), 400

    conn = sqlite3.connect("hall_bookings.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(*) FROM hall_bookings 
        WHERE hall = ? AND time_slot = ? 
        AND (
            (date_from BETWEEN ? AND ?) 
            OR (date_to BETWEEN ? AND ?) 
            OR (? BETWEEN date_from AND date_to) 
            OR (? BETWEEN date_from AND date_to)
        )
    ''', (hall, time_slot, date_from, date_to, date_from, date_to, date_from, date_to))

    count = cursor.fetchone()[0]
    conn.close()

    return jsonify({"available": count == 0})

@app.route("/check_availability")
def check_hall_availability():
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    hall = request.args.get("hall")
    time_slot = request.args.get("time_slot")

    if not date_from or not date_to or not hall or not time_slot:
        return jsonify({"error": "Missing required parameters"}), 400

    conn = sqlite3.connect("hall_bookings.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(*) FROM hall_bookings 
        WHERE hall = ? AND time_slot = ? 
        AND (
            (date_from BETWEEN ? AND ?) 
            OR (date_to BETWEEN ? AND ?) 
            OR (? BETWEEN date_from AND date_to) 
            OR (? BETWEEN date_from AND date_to)
        )
    ''', (hall, time_slot, date_from, date_to, date_from, date_to, date_from, date_to))

    count = cursor.fetchone()[0]
    conn.close()

    return jsonify({"available": count == 0})


if __name__ == "__main__":
    app.run(debug=True)
