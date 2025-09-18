# Admissions Console

A full-stack **Flask + Python + MySQL** application that centralizes **school admissions** workflows — from enquiries to tours, assessments, offers, follow‑ups, and payments — with a clean data model designed for **analytics dashboards** (Power BI/Tableau/Looker Studio).

![Banner](admissions-console-banner.png)

## ✨ Highlights
- **Unified Master Sheet** for enquiries with validated data entry (UK short dates, email/phone checks, integer constraints).
- **Next Step automations** to move rows into **Tours**, **Assessments**, **Follow Ups**, and **Closed Leads**, with due‑date logic and conditional formatting rules.
- **Appointments view** that auto‑aggregates **Tours** and **Assessments** by day (parent name, phone, date/time, type).
- **Offer management** with status & payment tracking and follow‑up scheduling.
- **Analytics‑ready schema** for funnels, conversion rates, weekly KPIs, and source effectiveness.

## 🧱 Data Model (Sheets / Tables)
**1) master_enquiries**  
Fields include:
- `id` (PK, unique), `enquiry_date` (DD/MM/YY), `source` (Facebook/Instagram/LinkedIn/Website/Call/WhatsApp)  
- Parent: `parent_first_name`, `parent_last_name`, `parent_email`, `country_code`, `phone_number`, `parent_nationality`, `parent_nationality_other`  
- Children: `child1_name`, `child1_dob`, `child1_year_2526`, `child2_*`, `child3_*`  
- `current_curriculum` (British/American/National/IB)
- `notes`, `lead_owner` (Jala/Waad/Sherihane), `next_step`, `lead_status` (Live/Closed)

**2) tours**  
- Copy of master row + `tour_date`, `tour_time`, `took_tour` (Y/N), `next_step` (same actions as master).

**3) assessments**  
- Copy of master row + `assessment_date`, `assessment_time`, `notes_link` (OneDrive URL), `offered_yn` (Y/N), `letter_sent_yn` (Y/N).  
- If `offered_yn = Y` ⇒ row copied to **offered**.

**4) followups_required**  
- Copy of master row + `follow_up_by` (owner), `follow_up_date = enquiry_date + 5 days` with RED highlight when overdue.

**5) closed_leads**  
- Copy of master row when lead is closed via Next Step.

**6) offered**  
- Copy of assessment row + `offer_date`, `offer_status` (Accepted/Rejected), `payment_status` (Deposit Paid/Term 1 Fees Paid/Annual Fees Paid/No Payment).  
- Conditional colours: **GREEN** for Term 1/Annual, **ORANGE** for Deposit, **RED** for No Payment.  
- If `payment_status = "No Payment"` ⇒ show `follow_up_required = Y` and `follow_up_date = offer_date + 7 days`.

**7) appointments** (generated)  
- `appt_date`, `appt_time`, `type` (Tour/Assessment), `parent_name`, `phone`, `child_name`, `year_group`.

## 🔁 Workflow Logic (Next Step)
- **Tour Booked** → copy to `tours` (+ date, time).  
- **Assessment Booked** → copy to `assessments` (+ date, time).  
- **No Reply** → copy to `followups_required` with `follow_up_date = enquiry_date + 5 days` and overdue highlight.  
- **Closed Lead** → set `lead_status = Closed` and copy to `closed_leads`.

## 📊 Dashboard & KPIs
- **Lead volume over time** (by day/week/month).  
- **Conversion funnel**: Enquiries → Assessments → Offers → Accepted → Paid.  
- **Source effectiveness** by Accepted/Paying leads.  
- **Follow‑up impact** (time‑to‑reply vs conversion).  
- **Outstanding follow‑ups & payments**.  
- **Weekly snapshot** (select any week, including current):  
  -  Enquiries, Tours Booked/Conducted, Assessments Booked/Conducted  
  -  Offers Sent/Accepted/Rejected  
  - % Enquiries → Tours / Assessments / Offers  
  - Total Enrolled (filterable by Year Group)  
  - Pipeline Follow Ups and Lead Source % mix
