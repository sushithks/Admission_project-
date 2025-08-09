CREATE DATABASE IF NOT EXISTS admissions;
USE admissions;

CREATE TABLE IF NOT EXISTS enquiries (
  enquiry_id INT AUTO_INCREMENT PRIMARY KEY,
  enquiry_date DATE,
  source ENUM('Facebook','Instagram','LinkedIn','Website','Call','WhatsApp'),
  parent_first_name VARCHAR(100),
  parent_last_name VARCHAR(100),
  parent_email VARCHAR(255),
  country_code VARCHAR(10),
  phone_number VARCHAR(20),
  nationality ENUM('Saudi','British','American','Canadian','Egyptian','Pakistani','Other'),
  nationality_other VARCHAR(100) NULL,
  number_of_children INT,
  current_curriculum ENUM('British','American','National','IB'),
  child1_name VARCHAR(100),
  child1_dob DATE,
  child1_year_group VARCHAR(50),
  child2_name VARCHAR(100),
  child2_dob DATE,
  child2_year_group VARCHAR(50),
  child3_name VARCHAR(100),
  child3_dob DATE,
  child3_year_group VARCHAR(50),
  notes TEXT,
  lead_owner ENUM('Jala','Waad','Sherihane'),
  next_step ENUM('Tour Booked','Assessment Booked','No Reply','Closed Lead') NULL,
  lead_status ENUM('Live','Closed') DEFAULT 'Live'
);


CREATE TABLE IF NOT EXISTS tours (
  -- copied from enquiries
  enquiry_id INT,
  enquiry_date DATE,
  source ENUM('Facebook','Instagram','LinkedIn','Website','Call','WhatsApp'),
  parent_first_name VARCHAR(100),
  parent_last_name VARCHAR(100),
  parent_email VARCHAR(255),
  country_code VARCHAR(10),
  phone_number VARCHAR(20),
  nationality ENUM('Saudi','British','American','Canadian','Egyptian','Pakistani','Other'),
  nationality_other VARCHAR(100) NULL,
  number_of_children INT,
  current_curriculum ENUM('British','American','National','IB'),
  child1_name VARCHAR(100),
  child1_dob DATE,
  child1_year_group VARCHAR(50),
  child2_name VARCHAR(100),
  child2_dob DATE,
  child2_year_group VARCHAR(50),
  child3_name VARCHAR(100),
  child3_dob DATE,
  child3_year_group VARCHAR(50),
  notes TEXT,
  lead_owner ENUM('Jala','Waad','Sherihane'),
  next_step ENUM('Tour Booked','Assessment Booked','No Reply','Closed Lead') NULL,
  lead_status ENUM('Live','Closed') DEFAULT 'Live',
  -- extra
  tour_date DATE NULL,
  tour_time TIME NULL,
  took_the_tour ENUM('Yes','No') NULL,
  next_step_after_tour ENUM('Tour Booked','Assessment Booked','No Reply','Closed Lead') NULL,
  KEY (enquiry_id)
);




CREATE TABLE IF NOT EXISTS assessments (
  -- copied from enquiries
  enquiry_id INT,
  enquiry_date DATE,
  source ENUM('Facebook','Instagram','LinkedIn','Website','Call','WhatsApp'),
  parent_first_name VARCHAR(100),
  parent_last_name VARCHAR(100),
  parent_email VARCHAR(255),
  country_code VARCHAR(10),
  phone_number VARCHAR(20),
  nationality ENUM('Saudi','British','American','Canadian','Egyptian','Pakistani','Other'),
  nationality_other VARCHAR(100) NULL,
  number_of_children INT,
  current_curriculum ENUM('British','American','National','IB'),
  child1_name VARCHAR(100),
  child1_dob DATE,
  child1_year_group VARCHAR(50),
  child2_name VARCHAR(100),
  child2_dob DATE,
  child2_year_group VARCHAR(50),
  child3_name VARCHAR(100),
  child3_dob DATE,
  child3_year_group VARCHAR(50),
  notes TEXT,
  lead_owner ENUM('Jala','Waad','Sherihane'),
  next_step ENUM('Tour Booked','Assessment Booked','No Reply','Closed Lead') NULL,
  lead_status ENUM('Live','Closed') DEFAULT 'Live',
  -- extra
  assessment_date DATE NULL,
  assessment_time TIME NULL,
  assessment_notes_link VARCHAR(512) NULL,
  offered ENUM('Yes','No') NULL,
  letter_sent ENUM('Yes','No') NULL,
  KEY (enquiry_id)
);




CREATE TABLE IF NOT EXISTS follow_ups_required (
  -- copied from enquiries
  enquiry_id INT,
  enquiry_date DATE,
  source ENUM('Facebook','Instagram','LinkedIn','Website','Call','WhatsApp'),
  parent_first_name VARCHAR(100),
  parent_last_name VARCHAR(100),
  parent_email VARCHAR(255),
  country_code VARCHAR(10),
  phone_number VARCHAR(20),
  nationality ENUM('Saudi','British','American','Canadian','Egyptian','Pakistani','Other'),
  nationality_other VARCHAR(100) NULL,
  number_of_children INT,
  current_curriculum ENUM('British','American','National','IB'),
  child1_name VARCHAR(100),
  child1_dob DATE,
  child1_year_group VARCHAR(50),
  child2_name VARCHAR(100),
  child2_dob DATE,
  child2_year_group VARCHAR(50),
  child3_name VARCHAR(100),
  child3_dob DATE,
  child3_year_group VARCHAR(50),
  notes TEXT,
  lead_owner ENUM('Jala','Waad','Sherihane'),
  next_step ENUM('Tour Booked','Assessment Booked','No Reply','Closed Lead') NULL,
  lead_status ENUM('Live','Closed') DEFAULT 'Live',
  -- extra
  follow_up_by DATE NULL,
  KEY (enquiry_id)
);



CREATE TABLE IF NOT EXISTS closed_leads (
  enquiry_id INT,
  enquiry_date DATE,
  source ENUM('Facebook','Instagram','LinkedIn','Website','Call','WhatsApp'),
  parent_first_name VARCHAR(100),
  parent_last_name VARCHAR(100),
  parent_email VARCHAR(255),
  country_code VARCHAR(10),
  phone_number VARCHAR(20),
  nationality ENUM('Saudi','British','American','Canadian','Egyptian','Pakistani','Other'),
  nationality_other VARCHAR(100) NULL,
  number_of_children INT,
  current_curriculum ENUM('British','American','National','IB'),
  child1_name VARCHAR(100),
  child1_dob DATE,
  child1_year_group VARCHAR(50),
  child2_name VARCHAR(100),
  child2_dob DATE,
  child2_year_group VARCHAR(50),
  child3_name VARCHAR(100),
  child3_dob DATE,
  child3_year_group VARCHAR(50),
  notes TEXT,
  lead_owner ENUM('Jala','Waad','Sherihane'),
  next_step ENUM('Tour Booked','Assessment Booked','No Reply','Closed Lead') NULL,
  lead_status ENUM('Live','Closed') DEFAULT 'Live',
  KEY (enquiry_id)
);



CREATE TABLE IF NOT EXISTS offered (
  enquiry_id INT,
  enquiry_date DATE,
  parent_first_name VARCHAR(100),
  parent_last_name VARCHAR(100),
  parent_email VARCHAR(255),
  phone_number VARCHAR(20),
  -- for context
  assessment_date DATE,
  assessment_time TIME,
  assessment_notes_link VARCHAR(512),
  letter_sent ENUM('Yes','No'),
  -- offer tracking
  offer_date DATE,
  offer_status ENUM('Accepted','Rejected'),
  payment_status ENUM('Deposit Paid','Term 1 Fees Paid','Annual Fees Paid','No Payment'),
  follow_up_needed DATE,
  KEY (enquiry_id)
);



CREATE OR REPLACE VIEW appointments AS
SELECT
  tour_date AS appointment_date,
  tour_time AS appointment_time,
  CONCAT(parent_first_name, ' ', parent_last_name) AS parent_name,
  phone_number,
  'Tour' AS appointment_type
FROM tours
WHERE tour_date IS NOT NULL
UNION
SELECT
  assessment_date AS appointment_date,
  assessment_time AS appointment_time,
  CONCAT(parent_first_name, ' ', parent_last_name) AS parent_name,
  phone_number,
  'Assessment' AS appointment_type
FROM assessments
WHERE assessment_date IS NOT NULL;
