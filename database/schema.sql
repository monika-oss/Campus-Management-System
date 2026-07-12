CREATE DATABASE IF NOT EXISTS smart_campus;
USE smart_campus;

-- Table 1: users
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  role ENUM('admin','faculty','student') NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP
);

-- Table 2: departments
CREATE TABLE departments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  code VARCHAR(20) UNIQUE NOT NULL
);

-- Table 3: students
CREATE TABLE students (
  student_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNIQUE,
  name VARCHAR(100) NOT NULL,
  roll_number VARCHAR(20) UNIQUE NOT NULL,
  department_id INT,
  year INT CHECK (year BETWEEN 1 AND 4),
  section VARCHAR(5),
  email VARCHAR(150) UNIQUE NOT NULL,
  phone VARCHAR(15),
  address TEXT,
  date_of_birth DATE,
  profile_photo VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Table 4: faculty
CREATE TABLE faculty (
  faculty_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNIQUE,
  name VARCHAR(100) NOT NULL,
  employee_id VARCHAR(20) UNIQUE NOT NULL,
  department_id INT,
  designation VARCHAR(100),
  email VARCHAR(150) UNIQUE NOT NULL,
  phone VARCHAR(15),
  qualification VARCHAR(100),
  experience_years INT,
  profile_photo VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Table 5: subjects
CREATE TABLE subjects (
  subject_id INT AUTO_INCREMENT PRIMARY KEY,
  subject_name VARCHAR(150) NOT NULL,
  subject_code VARCHAR(20) UNIQUE NOT NULL,
  department_id INT,
  year INT,
  credits INT DEFAULT 3,
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Table 6: attendance
CREATE TABLE attendance (
  attendance_id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  faculty_id INT,
  subject_id INT,
  date DATE NOT NULL,
  status ENUM('present','absent','late') NOT NULL,
  marked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(student_id),
  FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
  FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

-- Table 7: leave_requests
CREATE TABLE leave_requests (
  leave_id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  leave_type ENUM('medical','personal','academic','other') NOT NULL,
  from_date DATE NOT NULL,
  to_date DATE NOT NULL,
  reason TEXT NOT NULL,
  status ENUM('pending','approved','rejected') DEFAULT 'pending',
  reviewed_by INT,
  reviewed_at DATETIME,
  applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(student_id),
  FOREIGN KEY (reviewed_by) REFERENCES faculty(faculty_id)
);

-- Table 8: results
CREATE TABLE results (
  result_id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  subject_id INT NOT NULL,
  marks_obtained DECIMAL(5,2) NOT NULL,
  max_marks DECIMAL(5,2) DEFAULT 100,
  grade VARCHAR(5),
  semester INT,
  academic_year VARCHAR(10),
  is_published BOOLEAN DEFAULT FALSE,
  entered_by INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(student_id),
  FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
  FOREIGN KEY (entered_by) REFERENCES faculty(faculty_id)
);

-- Table 9: notifications
CREATE TABLE notifications (
  notification_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  target_role ENUM('all','student','faculty') DEFAULT 'all',
  created_by INT,
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Table 10: notification_reads
CREATE TABLE notification_reads (
  id INT AUTO_INCREMENT PRIMARY KEY,
  notification_id INT,
  user_id INT,
  read_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (notification_id) REFERENCES notifications(notification_id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
