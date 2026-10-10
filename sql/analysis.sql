USE nimcet_analytics;

-- ============================================================
-- 1. Study Hours vs NIMCET Performance
-- ============================================================
SELECT
    c.study_hours_daily,
    COUNT(*) AS candidates,
    ROUND(AVG(ep.nimcet_total_marks), 2) AS avg_total_marks,
    ROUND(AVG(ep.nimcet_rank), 2) AS avg_rank
FROM candidates c
JOIN exam_performance ep
    ON c.candidate_id = ep.candidate_id
GROUP BY c.study_hours_daily
ORDER BY c.study_hours_daily;


-- ============================================================
-- 2. Preparation Duration vs NIMCET Performance
-- ============================================================
SELECT
    c.preparation_months,
    COUNT(*) AS candidates,
    ROUND(AVG(ep.nimcet_total_marks), 2) AS avg_total_marks,
    ROUND(AVG(ep.nimcet_rank), 2) AS avg_rank
FROM candidates c
JOIN exam_performance ep
    ON c.candidate_id = ep.candidate_id
GROUP BY c.preparation_months
ORDER BY c.preparation_months;


-- ============================================================
-- 3. Mock Tests vs Performance
-- ============================================================
SELECT
    ep.mock_tests_count,
    COUNT(*) AS candidates,
    ROUND(AVG(ep.mock_average_score), 2) AS avg_mock_score,
    ROUND(AVG(ep.nimcet_total_marks), 2) AS avg_total_marks,
    ROUND(AVG(ep.nimcet_rank), 2) AS avg_rank
FROM exam_performance ep
GROUP BY ep.mock_tests_count
ORDER BY ep.mock_tests_count;


-- ============================================================
-- 4. Category-wise Performance
-- ============================================================
SELECT
    cat.category_name,
    COUNT(*) AS candidates,
    ROUND(AVG(ep.nimcet_total_marks), 2) AS avg_total_marks,
    ROUND(AVG(ep.nimcet_rank), 2) AS avg_rank
FROM candidates c
JOIN categories cat
    ON c.category_id = cat.category_id
JOIN exam_performance ep
    ON c.candidate_id = ep.candidate_id
GROUP BY cat.category_name
ORDER BY avg_total_marks DESC;


-- ============================================================
-- 5. Graduation Stream vs Performance
-- ============================================================
SELECT
    gs.stream_name,
    COUNT(*) AS candidates,
    ROUND(AVG(ep.nimcet_total_marks), 2) AS avg_total_marks,
    ROUND(AVG(ep.nimcet_rank), 2) AS avg_rank
FROM candidates c
JOIN graduation_streams gs
    ON c.graduation_stream_id = gs.stream_id
JOIN exam_performance ep
    ON c.candidate_id = ep.candidate_id
GROUP BY gs.stream_name
ORDER BY avg_total_marks DESC;


-- ============================================================
-- 6. Social Media Usage vs Performance
-- ============================================================
SELECT
    sm.band_label AS social_media_usage,
    COUNT(*) AS candidates,
    ROUND(AVG(ep.nimcet_total_marks), 2) AS avg_total_marks,
    ROUND(AVG(ep.nimcet_rank), 2) AS avg_rank
FROM candidates c
JOIN social_media_usage_bands sm
    ON c.social_media_band_id = sm.band_id
JOIN exam_performance ep
    ON c.candidate_id = ep.candidate_id
GROUP BY sm.band_label
ORDER BY sm.band_id;


-- ============================================================
-- 7. Difficulty Level vs Performance
-- ============================================================
SELECT
    dl.difficulty_name,
    COUNT(*) AS candidates,
    ROUND(AVG(ep.nimcet_total_marks), 2) AS avg_total_marks,
    ROUND(AVG(ep.nimcet_rank), 2) AS avg_rank
FROM exam_performance ep
JOIN difficulty_levels dl
    ON ep.difficulty_id = dl.difficulty_id
GROUP BY dl.difficulty_name
ORDER BY avg_total_marks DESC;


-- ============================================================
-- 8. Subject-wise Performance
-- ============================================================
SELECT
    ROUND(AVG(maths_marks), 2) AS avg_maths,
    ROUND(AVG(reasoning_marks), 2) AS avg_reasoning,
    ROUND(AVG(computer_marks), 2) AS avg_computer,
    ROUND(AVG(nimcet_total_marks), 2) AS avg_total
FROM exam_performance;


-- ============================================================
-- 9. Top 10 Candidates
-- ============================================================
SELECT
    c.candidate_id,
    c.age,
    c.gender,
    c.study_hours_daily,
    c.preparation_months,
    ep.mock_average_score,
    ep.nimcet_total_marks,
    ep.nimcet_rank
FROM candidates c
JOIN exam_performance ep
    ON c.candidate_id = ep.candidate_id
ORDER BY ep.nimcet_rank ASC
LIMIT 10;


-- ============================================================
-- 10. Study Mode vs Performance
-- ============================================================
SELECT
    sm.mode_name,
    COUNT(DISTINCT c.candidate_id) AS candidates,
    ROUND(AVG(ep.nimcet_total_marks), 2) AS avg_total_marks,
    ROUND(AVG(ep.nimcet_rank), 2) AS avg_rank
FROM candidates c
JOIN candidate_study_modes csm
    ON c.candidate_id = csm.candidate_id
JOIN study_modes sm
    ON csm.mode_id = sm.mode_id
JOIN exam_performance ep
    ON c.candidate_id = ep.candidate_id
GROUP BY sm.mode_name
ORDER BY avg_total_marks DESC;