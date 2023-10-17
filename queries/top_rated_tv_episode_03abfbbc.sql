-- Query: top rated tv episodes

-- Response: [('tt10040060', 'Dil Hi Toh Hai', 10.0), ('tt11690882', 'Dream Life', 10.0), ('tt12150458', "dewlover420's Vloog", 10.0), ('tt21089348', 'Ukraine on Fire 2', 10.0), ('tt21338442', 'Stories of Us', 10.0), ('tt21610506', 'The Challenge Show', 10.0), ('tt1249530', 'Bir Dilim Ask', 10.0), ('tt13005530', 'Entertainment Tonight', 10.0), ('tt4401318', "Recipe TV Featuring the World's Greatest Chefs", 10.0), ('tt4401350', "Recipe TV Featuring the World's Greatest Chefs", 10.0)]

SELECT episodes.id, productions.title, ratings.averagerating
FROM episodes
JOIN productions ON episodes.episodeof = productions.id
JOIN ratings ON episodes.id = ratings.id
ORDER BY ratings.averagerating DESC
LIMIT 10;
