
## Imports for Helper Functions

import json
import os
import psycopg2
import requests

from model import Play, Scene, Genre, Character, Monologue, User, Comment, connect_to_db, db

## Defines D3 Json Helper Functions

def to_json(QUERY, (columns)):
    """Queries Monologues, Characters, and Plays tables in database to create JSON for d3. Generates JSON to pass to Command Line"""

    db_connection = psycopg2.connect('dbname=monologues')
    db_cursor = db_connection.cursor()

    db_cursor.execute(QUERY)

    columns_tup = columns

    d3_json = []
    for row in db_cursor.fetchall():
        d3_json.append(dict(zip(columns_tup, row)))

    print json.dumps(d3_json, indent=2)


## USES DATABSE JSON CLASSES

def shakespeare_data():
    """Creates node structure for json for future D3 integration.

    Uses database json functions and then creates node/list arrays to pass into
    D3 force graph. Not currently implemented on front-end.
    """

    nodes = []
    links = []

    genre_q = Genre.query.all()
    play_q = Play.query.all()

    for genre in genre_q:
        nodes.append({"genre_id": genre.genre_id, "name": genre.genre_name })

    for play in play_q:
        nodes.append({"play_id" : play.play_id, "name": play.title, "play_genre": play.genre_id})

    for source_index, source_item in enumerate(nodes):
        for target_index, target_item in enumerate(nodes):
            if source_item.get("genre_id") == target_item.get("play_genre"):
                links.append({"source": source_index, "target": target_index})

    return {"nodes": nodes, "links": links}


    ### Below is unused code.. keeping for future integrations. ######

            # genres = Genre.query.filter(genre_id).all()
            # plays = Play.query.filter(play_id).all()
            # monologues = Monologue.query.filter(mono_id).all()
            # characters = Character.query.filter(char_id).all()
            #
            # for genre in genres:
            #     if genre.genre_id=='c':
            #         shakespeare.children.append(Node(genre.genre_name))
            #     else if genre.genre_id
            #
            # plays = Play.query.filter(play_id).all()
            # for play in plays:
            #     if play
