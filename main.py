
from datetime import datetime, timedelta
import mysql.connector

# UPDATE THIS with your credentials
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123.Canada',
    'database': 'admissions'
}
def insert_enquiry_and_handle_next_step(data):
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
        ''
    )

    cursor.execute(insert_query, values)
    enquiry_id = cursor.lastrowid

    # Columns to copy
    cols = """
        enquiry_id, enquiry_date, source, parent_first_name, parent_last_name, parent_email,
        country_code, phone_number, nationality, number_of_children,
        current_curriculum, child1_name, child1_dob, child1_year_group,
        notes, lead_owner, next_step, lead_status
    """

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
    return enquiry_id


















