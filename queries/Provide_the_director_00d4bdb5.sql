-- Query: Provide the director that directed the most movies in the year 2002

-- Response: [('nm1966600', 3657)]

SELECT d.director, COUNT(*) as movie_count
FROM directors d
JOIN crew c ON c.id = d.id
JOIN productions p ON p.id = c.id
WHERE p.year = 2002 AND c.crewtype = 'director'
GROUP BY d.director
ORDER BY movie_count DESC
LIMIT 1;
