import json
import sqlite3
def update_director_info(conn, director_id, director_is_awarded, director_birth_date):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE directeur
        SET director_is_awarded = ?,
            director_birth_date = ?
        WHERE id = ?
    """, (director_is_awarded, director_birth_date, director_id))
    conn.commit()

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except json.JSONDecodeError as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def update_director_info(conn, director_id, director_is_awarded, director_birth_date):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE director
        SET director_is_awarded = ?,
            director_birth_date = ?
        WHERE id = ?
    """, (director_is_awarded, director_birth_date, director_id))
    conn.commit()

def update_style_info(conn, style_id, definition):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE style
        SET style_description = ?
        WHERE id = ?
    """, (definition, style_id))
    conn.commit()

def run():
    conn = sqlite3.connect("../moviesDatabase.db")
    json_file_path = "directorsInfo.json"
    elements_list = read_json_file(json_file_path)
    if elements_list:
        for element in elements_list:
            if element['director_is_awarded'] == None:
                element['director_is_awarded'] = False
            update_director_info(conn, element['id'], element['director_is_awarded'], element['director_birth_date'])

    json_file_path = "styleInfo.json"
    elements_list = read_json_file(json_file_path)
    if elements_list:
        for element in elements_list:
            update_style_info(conn, element['id'], element['definition'])
