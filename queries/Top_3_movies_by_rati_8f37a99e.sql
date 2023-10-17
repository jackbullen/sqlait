-- Query: Top 3 movies by rating directed by Christopher Nolan

-- Response: [('The Dark Knight', 9.0), ('Inception', 8.8), ('Interstellar', 8.7)]

SELECT productions.title, ratings.averagerating
FROM productions
JOIN directors ON productions.id = directors.id
JOIN persons ON directors.director = persons.pid
JOIN ratings ON productions.id = ratings.id
WHERE persons.personname = 'Christopher Nolan'
ORDER BY ratings.averagerating DESC
LIMIT 3;