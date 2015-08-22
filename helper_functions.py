import requests, os, psycopg2
from model import Play, Scene, Genre, Character, Monologue, User, Comment, connect_to_db, db

db_connection = psycopg2.connect('dbname=monologues')
db_cursor = db_connection.cursor()

# DB Queries and functions to create Shakespeare Nodes/Lists

def shakespeare_data():
    """Creates node structure."""
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
