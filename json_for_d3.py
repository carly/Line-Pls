import json
import psycopg2

def to_json(QUERY, (columns)):
    """Queries Monologues, Characters, and Plays tables in database to create JSON for d3"""

    monologues = psycopg2.connect('dbname=monologues')
    mcur = monologues.cursor()

    mcur.execute(QUERY)

    columns_tup = columns

    d3_json = []
    for row in mcur.fetchall():
        d3_json.append(dict(zip(columns_tup, row)))

    print json.dumps(d3_json, indent=2)
