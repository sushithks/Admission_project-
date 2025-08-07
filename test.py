import mysql.connector


conn = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "123.Canada",
    database = "admissions"
)
cursor = conn.cursor()

insert_query = """
INSERT INTO enquiries (
    enquiry_date, source, parent_first_name, parent_last_name, parent_email,
    country_code, phone_number, nationality, number_of_children,
    current_curriculum, child1_name, child1_dob, child1_year_group,
    notes, lead_owner, next_step, lead_status
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Sample data (match exactly 17 values)
values = (
    "2025-08-06", "Facebook", "John", "Doe", "john.doe@example.com",
    "+966", "512345678", "British", 1,
    "British", "Alice", "2015-05-01", "Year 5",
    "Interested in a tour", "Waad", "Tour Booked", "Live"
)

cursor.execute(insert_query, values)
conn.commit()
cursor.close()
conn.close()