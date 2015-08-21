import requests, os, psycopg2
from model import Play, Scene, Genre, Character, Monologue, User, Comment, connect_to_db, db

db_connection = psycopg2.connect('dbname=monologues')
db_cursor = db_connection.cursor()

# First, create a node class

class Node(object):
    """Node that will turn into json eventually"""

    def __init__(self, name, children=None):
        self.data = data
        self.children = children or []

    def __repr__(self):
        return "<Node %s>" % self.name

    def find(self, name):
        """Return node object with this name.

        Start at this node. Return if not found."""

        to_visit = [self]

        while to_visit:
            node = to_visit.pop()

            if node.name == name:
                return node

            to_visit.extend(node.children)

# Create a tree class so that you an search from Root (may not be necessary, but we shall see)
class Tree(object):
    """Tree. so we can search by root"""

    def __init__(self, root):
        self.root = root

    def __repr__(self):
        return "<Tree root=%s>" % repr(self.root)

    def find(self, name):
        """Return node object with this name.

        Return none if not found."""

        return self.root.find(data)

# DB Queries and functions to create Shakespeare Search Tree

def shakespeare_data(genre_data):
    """Creates node structure."""

    shakespeare = Node("shakespeare")

    genres = Genre.query.filter(genre_id).all()
    plays = Play.query.filter(play_id).all()
    monologues = Monologue.query.filter(mono_id).all()
    characters = Character.query.filter(char_id).all()

    for genre in genres:
        if genre.genre_id=='c':
            shakespeare.children.append(Node(genre.genre_name))
        else if genre.genre_id

    plays = Play.query.filter(play_id).all()
    for play in plays:
        if play
