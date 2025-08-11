from flask import Flask, request, render_template_string, redirect
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '*********',
    'database': 'admissions'
}


# HTML for displaying enquiries
list_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Enquiries List</title>
</head>
<body>
<h2>Enquiries</h2>
<table border="1" cellpadding="5">
<tr>
    <th>ID</th>
    <th>Date</th>
    <th>Source</th>
    <th>Parent</th>
    <th>Email</th>
    <th>Phone</th>
    <th>Nationality</th>
    <th>Children</th>
    <th>Curriculum</th>
    <th>Lead Owner</th>
    <th>Next Step</th>
    <th>Action</th>
</tr>
{% for row in enquiries %}
<tr>
    <form method="post" action="/update/{{ row[0] }}">
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }} {{ row[4] }}</td>
        <td>{{ row[5] }}</td>
        <td>{{ row[6] }} {{ row[7] }}</td>
        <td>{{ row[8] }}</td>
        <td>{{ row[9] }}</td>
        <td>{{ row[10] }}</td>
        <td>{{ row[15] }}</td>
        <td>
            <select name="next_step">
                <option value="">None</option>
                <option {% if row[16] == 'Tour Booked' %}selected{% endif %}>Tour Booked</option>
                <option {% if row[16] == 'Assessment Booked' %}selected{% endif %}>Assessment Booked</option>
                <option {% if row[16] == 'No Reply' %}selected{% endif %}>No Reply</option>
                <option {% if row[16] == 'Closed Lead' %}selected{% endif %}>Closed Lead</option>
            </select>
        </td>
        <td><input type="submit" value="Update"></td>
    </form>
</tr>
{% endfor %}
</table>
</body>
</html>
"""

@app.route('/')
def list_enquiries():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enquiries order by enquiry_id asc")
    enquiries = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string(list_template, enquiries=enquiries)

@app.route('/update/<int:enquiry_id>', methods=['POST'])
def update_next_step(enquiry_id):
    next_step = request.form.get('next_step')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Update main table
    cursor.execute("UPDATE enquiries SET next_step = %s WHERE enquiry_id = %s", (next_step, enquiry_id))

    # Column list for copying
    cols = """
        enquiry_id, enquiry_date, source, parent_first_name, parent_last_name, parent_email,
        country_code, phone_number, nationality, number_of_children,
        current_curriculum, child1_name, child1_dob, child1_year_group,
        notes, lead_owner, next_step, lead_status
    """

    # Get enquiry date for follow-up calculation
    cursor.execute("SELECT enquiry_date FROM enquiries WHERE enquiry_id = %s", (enquiry_id,))
    enquiry_date = cursor.fetchone()[0]

    # Handle copying based on next_step
    if next_step == "Tour Booked":
        cursor.execute(f"INSERT INTO tours ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id = %s", (enquiry_id,))
    elif next_step == "Assessment Booked":
        cursor.execute(f"INSERT INTO assessments ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id = %s", (enquiry_id,))
    elif next_step == "No Reply":
        follow_up_by = (enquiry_date + timedelta(days=5)).strftime('%Y-%m-%d')
        cursor.execute(f"INSERT INTO follow_ups_required ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id = %s", (enquiry_id,))
        cursor.execute("UPDATE follow_ups_required SET follow_up_by = %s WHERE enquiry_id = %s", (follow_up_by, enquiry_id))
    elif next_step == "Closed Lead":
        cursor.execute("UPDATE enquiries SET lead_status = 'Closed' WHERE enquiry_id = %s", (enquiry_id,))
        cursor.execute(f"INSERT INTO closed_leads ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id = %s", (enquiry_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)