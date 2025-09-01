from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '***********',
    'database': 'admissions'
}

BASE_COLS = """
  enquiry_id,enquiry_date,source,parent_first_name,parent_last_name,parent_email,
  country_code,phone_number,nationality,nationality_other,number_of_children,
  current_curriculum,child1_name,child1_dob,child1_year_group,
  child2_name,child2_dob,child2_year_group,
  child3_name,child3_dob,child3_year_group,
  notes,lead_owner,next_step,lead_status
"""

def copy_once(src_table: str, dst_table: str, eid: int):
    run_query(f"""
        INSERT INTO {dst_table} ({BASE_COLS})
        SELECT {BASE_COLS} FROM {src_table} WHERE enquiry_id=%s
        ON DUPLICATE KEY UPDATE {dst_table}.enquiry_id = {dst_table}.enquiry_id
    """, (eid,))





def run_query(sql, params=(), fetch=False, dicts=True):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=dicts)
    cursor.execute(sql, params)
    rows = cursor.fetchall() if fetch else None
    conn.commit()
    cursor.close()
    conn.close()
    return rows

# -------------------- ENQUIRIES --------------------
@app.route('/enquiries/<int:eid>/update', methods=['POST'])
def enquiries_update(eid):
    next_step = request.form.get('next_step') or None

    # Touch activity timestamp and reset auto_follow_up_by by default
    run_query("""
        UPDATE enquiries
        SET last_activity_at=NOW(),
            auto_follow_up_by=NULL
        WHERE enquiry_id=%s
    """, (next_step, eid))

    row = run_query("SELECT enquiry_date FROM enquiries WHERE enquiry_id=%s", (eid,), fetch=True)
    enquiry_date = row[0]['enquiry_date'] if row else None

    if next_step == 'Tour Booked':
        copy_once('enquiries', 'tours', eid)

    elif next_step == 'Assessment Booked':
        copy_once('enquiries', 'assessments', eid)

    elif next_step == 'No Reply':
        copy_once('enquiries', 'follow_ups_required', eid)
        if enquiry_date:
            follow_up_by = enquiry_date + timedelta(days=5)

            # Persist on follow_ups_required (existing behavior)
            run_query("""
                UPDATE follow_ups_required
                SET follow_up_by=%s
                WHERE enquiry_id=%s
            """, (follow_up_by, eid))

            # NEW: persist on enquiries as well (the transformation)
            run_query("""
                UPDATE enquiries
                SET auto_follow_up_by=%s
                WHERE enquiry_id=%s
            """, (follow_up_by, eid))

    elif next_step == 'Closed Lead':
        run_query("UPDATE enquiries SET lead_status='Closed', auto_follow_up_by=NULL WHERE enquiry_id=%s", (eid,))
        copy_once('enquiries', 'closed_leads', eid)

    return redirect(url_for('enquiries_list'))

# -------------------- TOURS --------------------
@app.route('/tours')
def tours_list():
    rows = run_query("""
        SELECT
          t.*,
          DATEDIFF(CURDATE(), t.enquiry_date) AS lead_age_days
        FROM tours t
        ORDER BY t.tour_date IS NULL, t.tour_date, t.tour_time
    """, fetch=True)
    return render_template('app.html', page='tours', rows=rows)

@app.route('/tours/<int:eid>/update', methods=['POST'])
def tours_update(eid):
    tour_date = request.form.get('tour_date') or None
    tour_time = request.form.get('tour_time') or None
    took = request.form.get('took_the_tour') or None
    ns = request.form.get('next_step_after_tour') or None

    run_query("""
      UPDATE tours SET tour_date=%s, tour_time=%s, took_the_tour=%s, next_step_after_tour=%s
      WHERE enquiry_id=%s
    """, (tour_date, tour_time, took, ns, eid))

    cols = """
      enquiry_id,enquiry_date,source,parent_first_name,parent_last_name,parent_email,
      country_code,phone_number,nationality,nationality_other,number_of_children,
      current_curriculum,child1_name,child1_dob,child1_year_group,
      child2_name,child2_dob,child2_year_group,
      child3_name,child3_dob,child3_year_group,
      notes,lead_owner,next_step,lead_status
    """

    if ns == 'Assessment Booked':
        copy_once('tours', 'assessments', eid)

    elif ns == 'No Reply':
        copy_once('tours', 'follow_ups_required', eid)
        row = run_query("SELECT enquiry_date FROM tours WHERE enquiry_id=%s", (eid,), fetch=True)
        if row and row[0]['enquiry_date']:
            follow_up_by = row[0]['enquiry_date'] + timedelta(days=5)
            run_query("UPDATE follow_ups_required SET follow_up_by=%s WHERE enquiry_id=%s",
                      (follow_up_by, eid))

    elif ns == 'Closed Lead':
        run_query("UPDATE enquiries SET lead_status='Closed' WHERE enquiry_id=%s", (eid,))
        copy_once('tours', 'closed_leads', eid)

    return redirect(url_for('tours_list'))

# -------------------- ASSESSMENTS --------------------
@app.route('/assessments')
def assessments_list():
    rows = run_query("""
        SELECT
          a.*,
          DATEDIFF(CURDATE(), a.enquiry_date) AS lead_age_days
        FROM assessments a
        ORDER BY a.assessment_date IS NULL, a.assessment_date, a.assessment_time
    """, fetch=True)
    return render_template('app.html', page='assessments', rows=rows)



@app.route('/assessments/<int:eid>/update', methods=['POST'])
def assessments_update(eid):
    adate = request.form.get('assessment_date') or None
    atime = request.form.get('assessment_time') or None
    link = request.form.get('assessment_notes_link') or None
    offered = request.form.get('offered') or None
    letter = request.form.get('letter_sent') or None

    run_query("""
      UPDATE assessments SET assessment_date=%s, assessment_time=%s,
      assessment_notes_link=%s, offered=%s, letter_sent=%s
      WHERE enquiry_id=%s
    """, (adate, atime, link, offered, letter, eid))

    if offered == 'Yes':
        run_query("""
          INSERT INTO offered (
            enquiry_id, enquiry_date, parent_first_name, parent_last_name, parent_email, phone_number,
            assessment_date, assessment_time, assessment_notes_link, letter_sent,
            offer_date, offer_status, payment_status, follow_up_needed
          )
          SELECT
            enquiry_id, enquiry_date, parent_first_name, parent_last_name, parent_email, phone_number,
            assessment_date, assessment_time, assessment_notes_link, letter_sent,
            NULL, NULL, NULL, NULL
          FROM assessments WHERE enquiry_id=%s
          ON DUPLICATE KEY UPDATE enquiry_id = enquiry_id
        """, (eid,))

    return redirect(url_for('assessments_list'))

# -------------------- OFFERED --------------------
@app.route('/offered')
def offered_list():
    rows = run_query("""
        SELECT
          o.*,
          DATEDIFF(CURDATE(), o.enquiry_date) AS lead_age_days
        FROM offered o
        ORDER BY o.offer_date IS NULL, o.offer_date
    """, fetch=True)
    return render_template('app.html', page='offered', rows=rows)

@app.route('/offered/<int:eid>/update', methods=['POST'])
def offered_update(eid):
    offer_date = request.form.get('offer_date') or None
    offer_status = request.form.get('offer_status') or None
    payment = request.form.get('payment_status') or None

    follow_up = None
    if payment == 'No Payment' and offer_date:
        follow_up = (datetime.strptime(offer_date, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")

    run_query("""
      UPDATE offered SET offer_date=%s, offer_status=%s, payment_status=%s, follow_up_needed=%s
      WHERE enquiry_id=%s
    """, (offer_date, offer_status, payment, follow_up, eid))

    return redirect(url_for('offered_list'))

# -------------------- APPOINTMENTS --------------------
@app.route('/appointments')
def appointments_list():
    rows = run_query("""
        SELECT
          ap.*,
          DATEDIFF(CURDATE(), ap.appointment_date) AS lead_age_days
        FROM appointments ap
        ORDER BY ap.appointment_date, ap.appointment_time
    """, fetch=True)
    return render_template('app.html', page='appointments', rows=rows)
if __name__ == '__main__':
    app.run(debug=True)
