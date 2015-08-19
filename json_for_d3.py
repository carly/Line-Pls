import json
import psycopg2

def db_to_json():
    """Queries Monologues, Characters, and Plays tables in database to create JSON for d3"""

    monologues = psycopg2.connect('dbname=monologues')
    mcur = monologues.cursor()

    mcur.execute("""
    SELECT
          p.title,
          c.char_name,
          m.act_id,
          m.scene_id,
          m.mono_id,
          m.word_count,
          p.date,
          p.genre_id
    FROM
          Characters AS c
    JOIN
          Monologues AS m
          ON m.char_id = c.char_id
    JOIN
          Plays as p
          ON m.play_id = p.play_id

    ORDER BY
          p.title
    """)

    columns = ('title', 'name', 'act', 'scene','mono', 'words', 'date', 'genre')

    d3_json = []
    for row in mcur.fetchall():
        d3_json.append(dict(zip(columns, row)))

    print json.dumps(d3_json, indent=2)


db_to_json()
