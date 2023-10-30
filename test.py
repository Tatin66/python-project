import sqlite3

db = sqlite3.connect("moviesDatabase.db")
dbCursor = db.cursor()
sqlStrFilm = """
    SELECT
        f.id AS film_id,
        f.films_title AS film_title,
        f.films_plot AS film_plot,
        f.films_release_year AS film_release_year,
        f.films_release_date AS film_release_date,
        f.films_rating AS film_rating,
        f.films_image_url AS film_image_url,
        f.films_running_time AS film_running_time,
        GROUP_CONCAT(DISTINCT d.director_first_name) AS director_first_name,
        GROUP_CONCAT(DISTINCT d.director_last_name) AS director_last_names,
        GROUP_CONCAT(DISTINCT d.director_is_awarded) AS director_is_awarded,
        GROUP_CONCAT(DISTINCT d.director_birth_date) AS director_birth_date,
        GROUP_CONCAT(DISTINCT s.style_name) AS style_name
    FROM films f
        LEFT JOIN films_director fd ON f.id = fd.films_director_films_id
        LEFT JOIN director d ON fd.films_director_director_id = d.id
        LEFT JOIN films_style fs ON f.id = fs.films_style_films_id
        LEFT JOIN style s ON fs.films_style_style_id = s.id
    WHERE
        f.id = 0;
        """
dbCursor.execute(sqlStrFilm)
movies = dbCursor.fetchall()
listData = []
for row in movies:
    direcors = {
        "director_first_name": row[8],
        "director_last_name": row[9],
        "director_is_awarded": row[10],
        "director_birth_date": row[11]
    }

    styles = {}
    styleList = row[12].split(",")
    for style in styleList:
        sqlStrStyle = "SELECT * from style WHERE style_name = '" + style + "'"
        dbCursor.execute(sqlStrStyle)
        resStyle = dbCursor.fetchall()
        print(resStyle)

    data_dict = {
        "id": row[0],
        "films_title": row[1],
        "films_plot": row[2],
        "films_release_year": row[3],
        "films_release_date": row[4],
        "films_rating": row[5],
        "films_image_url": row[6],
        "films_running_time": row[7],
        "directors": direcors,
        "styles": styles
    }
    listData.append(data_dict)
json_data = json.loads(json.dumps(listData))