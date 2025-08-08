from flask import Flask, request, render_template_string
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)

# UPDATE these with your database credentials
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '***********',
    'database': 'admissions'
}

# HTML Form Template
form_template = """
<!DOCTYPE html>
<html>
<head><title>Admissions Enquiry Form</title></head>
<body>
    <h2>Admissions Enquiry Form</h2>
    <form method="post">
        Date of Enquiry: <input type="date" name="enquiry_date" required><br><br>
        Source: <select name="source">
            <option>Facebook</option><option>Instagram</option><option>LinkedIn</option>
            <option>Website</option><option>Call</option><option>WhatsApp</option>
        </select><br><br>
        Parent First Name: <input type="text" name="parent_first_name" required><br><br>
        Parent Last Name: <input type="text" name="parent_last_name" required><br><br>
        Parent Email: <input type="email" name="parent_email" required><br><br>
        Country Code: <input type="text" name="country_code" required>
        Phone Number: <input type="text" name="phone_number" required><br><br>
        Nationality: <select name="nationality">
            <option>Saudi</option><option>British</option><option>American</option>
            <option>Canadian</option><option>Egyptian</option><option>Pakistani</option>
            <option>Other</option>
        </select><br><br>
        Number of Children: <input type="number" name="number_of_children" required><br><br>
        Curriculum: <select name="current_curriculum">
            <option>British</option><option>American</option><option>National</option><option>IB</option>
        </select><br><br>
        Child 1 Name: <input type="text" name="child1_name"><br><br>
        Child 1 DOB: <input type="date" name="child1_dob"><br><br>
        Child 1 Year Group: <input type="text" name="child1_year_group"><br><br>
        Notes:<br><textarea name="notes" rows="4" cols="40"></textarea><br><br>
        Lead Owner: <select name="lead_owner">
            <option>Jala</option><option>Waad</option><option>Sherihane</option>
        </select><br><br>
        Next Step: <select name="next_step">
            <option value="">None</option>
            <option>Tour Booked</option>
            <option>Assessment Booked</option>
            <option>No Reply</option>
            <option>Closed Lead</option>
        </select><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def admission_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO enquiries (
            enquiry_date, source, parent_first_name, parent_last_name, parent_email,
            country_code, phone_number, nationality, number_of_children,
            current_curriculum, child1_name, child1_dob, child1_year_group,
            notes, lead_owner, next_step, lead_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data.get('enquiry_date'),
            data.get('source'),
            data.get('parent_first_name'),
            data.get('parent_last_name'),
            data.get('parent_email'),
            data.get('country_code'),
            data.get('phone_number'),
            data.get('nationality'),
            int(data.get('number_of_children') or 0),
            data.get('current_curriculum'),
            data.get('child1_name'),
            data.get('child1_dob'),
            data.get('child1_year_group'),
            data.get('notes'),
            data.get('lead_owner'),
            data.get('next_step'),
            'Live'
        )

        cursor.execute(insert_query, values)
        enquiry_id = cursor.lastrowid

        cols = """
            enquiry_id, enquiry_date, source, parent_first_name, parent_last_name, parent_email,
            country_code, phone_number, nationality, number_of_children,
            current_curriculum, child1_name, child1_dob, child1_year_group,
            notes, lead_owner, next_step, lead_status
        """

        # Handle 'Next Step' logic
        if data.get('next_step') == "Tour Booked":
            cursor.execute(f"INSERT INTO tours ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id = %s", (enquiry_id,))
        elif data.get('next_step') == "Assessment Booked":
            cursor.execute(f"INSERT INTO assessments ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id = %s", (enquiry_id,))
        elif data.get('next_step') == "No Reply":
            follow_up_by = (datetime.strptime(data['enquiry_date'], "%Y-%m-%d") + timedelta(days=5)).strftime('%Y-%m-%d')
            cursor.execute(f"INSERT INTO follow_ups_required ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id = %s", (enquiry_id,))
            cursor.execute("UPDATE follow_ups_required SET follow_up_by = %s WHERE enquiry_id = %s", (follow_up_by, enquiry_id))
        elif data.get('next_step') == "Closed Lead":
            cursor.execute("UPDATE enquiries SET lead_status = 'Closed' WHERE enquiry_id = %s", (enquiry_id,))
            cursor.execute(f"INSERT INTO closed_leads ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id = %s", (enquiry_id,))

        conn.commit()
        cursor.close()
        conn.close()

    return render_template_string(form_template)

if __name__ == '__main__':
    app.run(debug=True)




