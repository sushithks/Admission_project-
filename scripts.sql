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




INSERT INTO enquiries (
    enquiry_date, source, parent_first_name, parent_last_name, parent_email,
    country_code, phone_number, nationality, number_of_children,
    current_curriculum, child1_name, child1_dob, child1_year_group,
    child2_name, child2_dob, child2_year_group,
    child3_name, child3_dob, child3_year_group,
    notes, lead_owner, next_step, lead_status
) VALUES
-- 1 Tour Booked
('2025-08-04', 'Website', 'Mona', 'Hassan', 'mona.hassan@email.com', '+20', '102334455', 'Egyptian', 1,
 'British', 'Yousef', '2020-02-10', 'FS2',
 NULL, NULL, NULL,
 NULL, NULL, NULL,
 'Requested weekend tour', 'Jala', 'Tour Booked', 'Live'),

-- 2 Assessment Booked
('2025-08-05', 'WhatsApp', 'Ali', 'Rashid', 'ali.rashid@email.com', '+92', '3345566778', 'Pakistani', 2,
 'National', 'Hina', '2019-07-21', 'Year 1',
 'Owais', '2021-09-14', 'FS1',
 NULL, NULL, NULL,
 'Interested in curriculum change', 'Waad', 'Assessment Booked', 'Live'),

-- 3 No Reply
('2025-08-06', 'Facebook', 'Linda', 'Brown', 'linda.brown@email.com', '+1', '4169988776', 'Canadian', 1,
 'American', 'Ella', '2018-05-05', 'Year 2',
 NULL, NULL, NULL,
 NULL, NULL, NULL,
 'Left voicemail, awaiting reply', 'Sherihane', 'No Reply', 'Live'),

-- 4 Closed Lead
('2025-08-07', 'Instagram', 'George', 'Williams', 'george.williams@email.com', '+44', '7800556677', 'British', 2,
 'IB', 'Lucas', '2017-04-18', 'Year 4',
 'Olivia', '2019-03-12', 'Year 2',
 NULL, NULL, NULL,
 'Family moving abroad', 'Jala', 'Closed Lead', 'Closed'),

-- 5 Tour Booked
('2025-08-08', 'Website', 'Noura', 'Al Saud', 'noura.alsaud@email.com', '+966', '501112223', 'Saudi', 3,
 'British', 'Fahad', '2016-12-30', 'Year 5',
 'Maha', '2019-10-25', 'Year 2',
 'Rakan', '2021-08-09', 'FS1',
 'Wants to see sports facilities', 'Waad', 'Tour Booked', 'Live'),

-- 6 Assessment Booked
('2025-08-09', 'Call', 'Peter', 'Johnson', 'peter.johnson@email.com', '+1', '9053345566', 'Canadian', 1,
 'American', 'Jack', '2018-07-14', 'Year 2',
 NULL, NULL, NULL,
 NULL, NULL, NULL,
 'Asking about scholarship options', 'Sherihane', 'Assessment Booked', 'Live'),

-- 7 No Reply
('2025-08-10', 'LinkedIn', 'Sara', 'Karim', 'sara.karim@email.com', '+20', '100223344', 'Egyptian', 2,
 'IB', 'Mariam', '2017-08-19', 'Year 4',
 'Hassan', '2019-09-25', 'Year 2',
 NULL, NULL, NULL,
 'Sent email follow-up', 'Jala', 'No Reply', 'Live'),

-- 8 Closed Lead
('2025-08-11', 'WhatsApp', 'Omar', 'Khalid', 'omar.khalid@email.com', '+92', '3349988776', 'Pakistani', 1,
 'National', 'Bilal', '2020-04-12', 'FS2',
 NULL, NULL, NULL,
 NULL, NULL, NULL,
 'Decided on another school', 'Waad', 'Closed Lead', 'Closed'),

-- 9 Tour Booked
('2025-08-12', 'Facebook', 'Huda', 'Abdullah', 'huda.abdullah@email.com', '+966', '503456789', 'Saudi', 2,
 'British', 'Amal', '2019-01-11', 'Year 1',
 'Yara', '2021-05-20', 'FS1',
 NULL, NULL, NULL,
 'Prefers female tour guide', 'Sherihane', 'Tour Booked', 'Live'),

-- 10 Assessment Booked
('2025-08-13', 'Website', 'David', 'Clark', 'david.clark@email.com', '+44', '7700667788', 'British', 3,
 'American', 'James', '2017-11-09', 'Year 4',
 'Henry', '2019-08-15', 'Year 2',
 'Isla', '2021-03-30', 'FS1',
 'Looking for transport facilities', 'Jala', 'Assessment Booked', 'Live');




ALTER TABLE tours ADD UNIQUE (enquiry_id);
ALTER TABLE assessments ADD UNIQUE (enquiry_id);
ALTER TABLE follow_ups_required ADD UNIQUE (enquiry_id);
ALTER TABLE closed_leads ADD UNIQUE (enquiry_id);



ALTER TABLE enquiries
  ADD COLUMN last_activity_at DATETIME NULL,
  ADD COLUMN auto_follow_up_by DATE NULL;

-- (optional but recommended for filters/sorting)
CREATE INDEX idx_enquiries_auto_follow_up_by ON enquiries(auto_follow_up_by);
CREATE INDEX idx_enquiries_last_activity_at ON enquiries(last_activity_at);
