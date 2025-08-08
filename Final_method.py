from flask import Flask, request, render_template_string, redirect
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)

# ====== UPDATE THESE ======
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '**********',
    'database': 'admissions'
}

# ==========================

def run_query(sql, params=(), fetch=False, dicts=False):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=dicts)
    cursor.execute(sql, params)
    rows = cursor.fetchall() if fetch else None
    conn.commit()
    cursor.close()
    conn.close()
    return rows

# ---------- Templates (very simple) ----------
enquiries_tpl = """
<h2>Enquiries</h2>
<table border="1" cellpadding="6">
<tr>
  <th>ID</th><th>Date</th><th>Parent</th><th>Email</th><th>Phone</th>
  <th>Nationality</th><th>Children</th><th>Curriculum</th>
  <th>Owner</th><th>Next Step</th><th>Status</th><th>Action</th>
</tr>
{% for r in rows %}
<tr>
<form method="post" action="/enquiries/{{ r.enquiry_id }}/update">
  <td>{{ r.enquiry_id }}</td>
  <td>{{ r.enquiry_date }}</td>
  <td>{{ r.parent_first_name }} {{ r.parent_last_name }}</td>
  <td>{{ r.parent_email }}</td>
  <td>{{ r.country_code }} {{ r.phone_number }}</td>
  <td>{{ r.nationality }}{% if r.nationality == 'Other' and r.nationality_other %} ({{ r.nationality_other }}){% endif %}</td>
  <td>{{ r.number_of_children }}</td>
  <td>{{ r.current_curriculum }}</td>
  <td>{{ r.lead_owner }}</td>
  <td>
    <select name="next_step">
      <option value="" {% if not r.next_step %}selected{% endif %}>--</option>
      <option value="Tour Booked" {% if r.next_step == 'Tour Booked' %}selected{% endif %}>Tour Booked</option>
      <option value="Assessment Booked" {% if r.next_step == 'Assessment Booked' %}selected{% endif %}>Assessment Booked</option>
      <option value="No Reply" {% if r.next_step == 'No Reply' %}selected{% endif %}>No Reply</option>
      <option value="Closed Lead" {% if r.next_step == 'Closed Lead' %}selected{% endif %}>Closed Lead</option>
    </select>
  </td>
  <td>{{ r.lead_status }}</td>
  <td><button type="submit">Update</button></td>
</form>
</tr>
{% endfor %}
</table>
<p>
  <a href="/tours">Tours</a> |
  <a href="/assessments">Assessments</a> |
  <a href="/offered">Offered</a> |
  <a href="/appointments">Appointments</a>
</p>
"""

tours_tpl = """
<h2>Tours</h2>
<table border="1" cellpadding="6">
<tr>
  <th>ID</th><th>Parent</th><th>Date</th><th>Time</th><th>Took?</th><th>Next Step</th><th>Save</th>
</tr>
{% for r in rows %}
<tr>
<form method="post" action="/tours/{{ r.enquiry_id }}/update">
  <td>{{ r.enquiry_id }}</td>
  <td>{{ r.parent_first_name }} {{ r.parent_last_name }}</td>
  <td><input type="date" name="tour_date" value="{{ r.tour_date or '' }}"></td>
  <td><input type="time" name="tour_time" value="{{ r.tour_time or '' }}"></td>
  <td>
    <select name="took_the_tour">
      <option value=""></option>
      <option value="Yes" {% if r.took_the_tour == 'Yes' %}selected{% endif %}>Yes</option>
      <option value="No"  {% if r.took_the_tour == 'No' %}selected{% endif %}>No</option>
    </select>
  </td>
  <td>
    <select name="next_step_after_tour">
      <option value=""></option>
      <option value="Assessment Booked" {% if r.next_step_after_tour == 'Assessment Booked' %}selected{% endif %}>Assessment Booked</option>
      <option value="No Reply" {% if r.next_step_after_tour == 'No Reply' %}selected{% endif %}>No Reply</option>
      <option value="Closed Lead" {% if r.next_step_after_tour == 'Closed Lead' %}selected{% endif %}>Closed Lead</option>
    </select>
  </td>
  <td><button>Save</button></td>
</form>
</tr>
{% endfor %}
</table>
<p><a href="/">Back</a></p>
"""

assess_tpl = """
<h2>Assessments</h2>
<table border="1" cellpadding="6">
<tr>
  <th>ID</th><th>Parent</th><th>Date</th><th>Time</th><th>Notes Link</th>
  <th>Offered?</th><th>Letter Sent?</th><th>Save</th>
</tr>
{% for r in rows %}
<tr>
<form method="post" action="/assessments/{{ r.enquiry_id }}/update">
  <td>{{ r.enquiry_id }}</td>
  <td>{{ r.parent_first_name }} {{ r.parent_last_name }}</td>
  <td><input type="date" name="assessment_date" value="{{ r.assessment_date or '' }}"></td>
  <td><input type="time" name="assessment_time" value="{{ r.assessment_time or '' }}"></td>
  <td><input type="text" name="assessment_notes_link" value="{{ r.assessment_notes_link or '' }}" size="40"></td>
  <td>
    <select name="offered">
      <option value=""></option>
      <option value="Yes" {% if r.offered == 'Yes' %}selected{% endif %}>Yes</option>
      <option value="No"  {% if r.offered == 'No' %}selected{% endif %}>No</option>
    </select>
  </td>
  <td>
    <select name="letter_sent">
      <option value=""></option>
      <option value="Yes" {% if r.letter_sent == 'Yes' %}selected{% endif %}>Yes</option>
      <option value="No"  {% if r.letter_sent == 'No' %}selected{% endif %}>No</option>
    </select>
  </td>
  <td><button>Save</button></td>
</form>
</tr>
{% endfor %}
</table>
<p><a href="/">Back</a></p>
"""

offered_tpl = """
<h2>Offered</h2>
<table border="1" cellpadding="6">
<tr>
  <th>ID</th><th>Parent</th><th>Offer Date</th><th>Status</th><th>Payment</th><th>Follow-up</th><th>Save</th>
</tr>
{% for r in rows %}
<tr>
<form method="post" action="/offered/{{ r.enquiry_id }}/update">
  <td>{{ r.enquiry_id }}</td>
  <td>{{ r.parent_first_name }} {{ r.parent_last_name }}</td>
  <td><input type="date" name="offer_date" value="{{ r.offer_date or '' }}"></td>
  <td>
    <select name="offer_status">
      <option value=""></option>
      <option value="Accepted" {% if r.offer_status == 'Accepted' %}selected{% endif %}>Accepted</option>
      <option value="Rejected" {% if r.offer_status == 'Rejected' %}selected{% endif %}>Rejected</option>
    </select>
  </td>
  <td>
    <select name="payment_status">
      <option value=""></option>
      <option value="Deposit Paid" {% if r.payment_status == 'Deposit Paid' %}selected{% endif %}>Deposit Paid</option>
      <option value="Term 1 Fees Paid" {% if r.payment_status == 'Term 1 Fees Paid' %}selected{% endif %}>Term 1 Fees Paid</option>
      <option value="Annual Fees Paid" {% if r.payment_status == 'Annual Fees Paid' %}selected{% endif %}>Annual Fees Paid</option>
      <option value="No Payment" {% if r.payment_status == 'No Payment' %}selected{% endif %}>No Payment</option>
    </select>
  </td>
  <td>{{ r.follow_up_needed or '' }}</td>
  <td><button>Save</button></td>
</form>
</tr>
{% endfor %}
</table>
<p><a href="/">Back</a></p>
"""

appts_tpl = """
<h2>Appointments</h2>
<table border="1" cellpadding="6">
<tr><th>Date</th><th>Time</th><th>Parent</th><th>Phone</th><th>Type</th></tr>
{% for r in rows %}
<tr>
  <td>{{ r.appointment_date }}</td>
  <td>{{ r.appointment_time }}</td>
  <td>{{ r.parent_name }}</td>
  <td>{{ r.phone_number }}</td>
  <td>{{ r.appointment_type }}</td>
</tr>
{% endfor %}
</table>
<p><a href="/">Back</a></p>
"""

# ---------- Routes ----------
@app.route('/')
def enquiries_list():
    rows = run_query("SELECT * FROM enquiries ORDER BY enquiry_id DESC", fetch=True, dicts=True)
    return render_template_string(enquiries_tpl, rows=rows)

@app.route('/enquiries/<int:eid>/update', methods=['POST'])
def enquiries_update(eid):
    next_step = request.form.get('next_step') or None
    run_query("UPDATE enquiries SET next_step=%s WHERE enquiry_id=%s", (next_step, eid))

    # list of columns to copy (keep order consistent across tables)
    cols = """
      enquiry_id,enquiry_date,source,parent_first_name,parent_last_name,parent_email,
      country_code,phone_number,nationality,nationality_other,number_of_children,
      current_curriculum,child1_name,child1_dob,child1_year_group,
      child2_name,child2_dob,child2_year_group,
      child3_name,child3_dob,child3_year_group,
      notes,lead_owner,next_step,lead_status
    """

    # pull enquiry_date for follow-up calc
    row = run_query("SELECT enquiry_date FROM enquiries WHERE enquiry_id=%s", (eid,), fetch=True, dicts=True)
    enquiry_date = row[0]['enquiry_date'] if row else None

    if next_step == 'Tour Booked':
        run_query(f"INSERT INTO tours ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id=%s", (eid,))
    elif next_step == 'Assessment Booked':
        run_query(f"INSERT INTO assessments ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id=%s", (eid,))
    elif next_step == 'No Reply':
        run_query(f"INSERT INTO follow_ups_required ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id=%s", (eid,))
        if enquiry_date:
            follow_up_by = enquiry_date + timedelta(days=5)
            run_query("UPDATE follow_ups_required SET follow_up_by=%s WHERE enquiry_id=%s", (follow_up_by, eid))
    elif next_step == 'Closed Lead':
        run_query("UPDATE enquiries SET lead_status='Closed' WHERE enquiry_id=%s", (eid,))
        run_query(f"INSERT INTO closed_leads ({cols}) SELECT {cols} FROM enquiries WHERE enquiry_id=%s", (eid,))

    return redirect('/')

# ---- Tours ----
@app.route('/tours')
def tours_list():
    rows = run_query("SELECT * FROM tours ORDER BY tour_date IS NULL, tour_date, tour_time", fetch=True, dicts=True)
    return render_template_string(tours_tpl, rows=rows)

@app.route('/tours/<int:eid>/update', methods=['POST'])
def tours_update(eid):
    tour_date = request.form.get('tour_date') or None
    tour_time = request.form.get('tour_time') or None
    took = request.form.get('took_the_tour') or None
    ns = request.form.get('next_step_after_tour') or None

    run_query("""
      UPDATE tours
      SET tour_date=%s, tour_time=%s, took_the_tour=%s, next_step_after_tour=%s
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
    # cascade actions after tour
    if ns == 'Assessment Booked':
        run_query(f"INSERT INTO assessments ({cols}) SELECT {cols} FROM tours WHERE enquiry_id=%s", (eid,))
    elif ns == 'No Reply':
        run_query(f"INSERT INTO follow_ups_required ({cols}) SELECT {cols} FROM tours WHERE enquiry_id=%s", (eid,))
        # get enquiry_date from tours for follow-up calc
        row = run_query("SELECT enquiry_date FROM tours WHERE enquiry_id=%s", (eid,), fetch=True, dicts=True)
        if row and row[0]['enquiry_date']:
            follow_up_by = row[0]['enquiry_date'] + timedelta(days=5)
            run_query("UPDATE follow_ups_required SET follow_up_by=%s WHERE enquiry_id=%s", (follow_up_by, eid))
    elif ns == 'Closed Lead':
        run_query("UPDATE enquiries SET lead_status='Closed' WHERE enquiry_id=%s", (eid,))
        run_query(f"INSERT INTO closed_leads ({cols}) SELECT {cols} FROM tours WHERE enquiry_id=%s", (eid,))

    return redirect('/tours')

# ---- Assessments ----
@app.route('/assessments')
def assessments_list():
    rows = run_query("SELECT * FROM assessments ORDER BY assessment_date IS NULL, assessment_date, assessment_time", fetch=True, dicts=True)
    return render_template_string(assess_tpl, rows=rows)

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

    # copy to offered if offered = Yes
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
        """, (eid,))

    return redirect('/assessments')

# ---- Offered ----
@app.route('/offered')
def offered_list():
    rows = run_query("SELECT * FROM offered ORDER BY offer_date IS NULL, offer_date", fetch=True, dicts=True)
    return render_template_string(offered_tpl, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
