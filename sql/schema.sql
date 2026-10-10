CREATE DATABASE IF NOT EXISTS nimcet_analytics;

USE nimcet_analytics;


-- =========================================
-- 1. CATEGORIES
-- =========================================

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);


-- =========================================
-- 2. GRADUATION STREAMS
-- =========================================

CREATE TABLE graduation_streams (
    stream_id INT AUTO_INCREMENT PRIMARY KEY,
    stream_name VARCHAR(100) NOT NULL UNIQUE
);


-- =========================================
-- 3. SOCIAL MEDIA USAGE
-- =========================================

CREATE TABLE social_media_usage_bands (
    band_id INT AUTO_INCREMENT PRIMARY KEY,
    band_label VARCHAR(20) NOT NULL UNIQUE,
    min_hours DECIMAL(4,2),
    max_hours DECIMAL(4,2)
);


-- =========================================
-- 4. DIFFICULTY LEVELS
-- =========================================

CREATE TABLE difficulty_levels (
    difficulty_id INT AUTO_INCREMENT PRIMARY KEY,
    difficulty_name VARCHAR(50) NOT NULL UNIQUE
);


-- =========================================
-- 5. COLLEGES
-- =========================================

CREATE TABLE colleges (
    college_id INT AUTO_INCREMENT PRIMARY KEY,
    college_name VARCHAR(150) NOT NULL UNIQUE,
    college_type VARCHAR(50)
);


-- =========================================
-- 6. STUDY MODES
-- =========================================

CREATE TABLE study_modes (
    mode_id INT AUTO_INCREMENT PRIMARY KEY,
    mode_name VARCHAR(50) NOT NULL UNIQUE
);


-- =========================================
-- 7. PREPARATION ISSUES
-- =========================================

CREATE TABLE preparation_issues (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_name VARCHAR(150) NOT NULL UNIQUE
);


-- =========================================
-- 8. CANDIDATES
-- =========================================

CREATE TABLE candidates (
    candidate_id INT AUTO_INCREMENT PRIMARY KEY,

    response_timestamp DATETIME,

    age INT,
    gender VARCHAR(20),

    preferred_study_time VARCHAR(50),

    jee_prepared BOOLEAN,

    study_hours_daily DECIMAL(5,2),

    preparation_months INT,

    background_12th VARCHAR(100),

    social_media_band_id INT,

    category_id INT,

    college_id INT,

    graduation_stream_id INT,

    is_dropper BOOLEAN,

    FOREIGN KEY (social_media_band_id)
        REFERENCES social_media_usage_bands(band_id),

    FOREIGN KEY (category_id)
        REFERENCES categories(category_id),

    FOREIGN KEY (college_id)
        REFERENCES colleges(college_id),

    FOREIGN KEY (graduation_stream_id)
        REFERENCES graduation_streams(stream_id)
);


-- =========================================
-- 9. CANDIDATE ↔ STUDY MODE
-- =========================================

CREATE TABLE candidate_study_modes (
    candidate_id INT,
    mode_id INT,

    PRIMARY KEY (candidate_id, mode_id),

    FOREIGN KEY (candidate_id)
        REFERENCES candidates(candidate_id)
        ON DELETE CASCADE,

    FOREIGN KEY (mode_id)
        REFERENCES study_modes(mode_id)
        ON DELETE CASCADE
);


-- =========================================
-- 10. CANDIDATE ↔ PREPARATION ISSUES
-- =========================================

CREATE TABLE candidate_preparation_issues (
    candidate_id INT,
    issue_id INT,

    PRIMARY KEY (candidate_id, issue_id),

    FOREIGN KEY (candidate_id)
        REFERENCES candidates(candidate_id)
        ON DELETE CASCADE,

    FOREIGN KEY (issue_id)
        REFERENCES preparation_issues(issue_id)
        ON DELETE CASCADE
);


-- =========================================
-- 11. EXAM PERFORMANCE
-- =========================================

CREATE TABLE exam_performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,

    candidate_id INT NOT NULL UNIQUE,

    mock_average_score INT,

    mock_tests_count INT,

    maths_marks DECIMAL(6,2),

    reasoning_marks DECIMAL(6,2),

    computer_marks DECIMAL(6,2),

    nimcet_total_marks DECIMAL(6,2),

    nimcet_rank INT,

    difficulty_id INT,

    FOREIGN KEY (candidate_id)
        REFERENCES candidates(candidate_id)
        ON DELETE CASCADE,

    FOREIGN KEY (difficulty_id)
        REFERENCES difficulty_levels(difficulty_id)
);