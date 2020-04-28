SELECT t.tutorial_title, s.tutorial_series, c.tutorial_category
FROM main_tutorial as t
INNER JOIN main_tutorialseries as s
ON t.tutorial_series_id = s.id
INNER JOIN main_tutorialcategory as c
ON s.tutorial_category_id = c.id
WHERE c.tutorial_category LIKE "%web%";