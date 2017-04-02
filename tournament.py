#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    player_count = 0
    c.execute("select count(*) as pcount from players;")
    player_count = int(c.fetchone()[0])
    conn.commit()
    conn.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database."""

    conn = connect()
    c = conn.cursor()
    d = conn.cursor()
    c.execute("INSERT INTO players(name) values(%s);", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins."""

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM standings;")
    player_standings = c.fetchall()
    conn.commit()
    conn.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players."""

    conn = connect()
    w = conn.cursor()
    w.execute("INSERT INTO matches(winner_id, loser_id) values(%s, %s);", (winner, loser))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match."""

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT standings.id, standings.name FROM standings")
    players = c.fetchall()
    conn.commit()
    conn.close()
    swiss_pairing = []
    row = 0
    total_rows = len(players)
    while row < total_rows-1:
        p1 = players[row]
        p2 = players[row+1]
        t = (p1[0], p1[1], p2[0], p2[1])
        swiss_pairing.append(t)
        row += 2

    return swiss_pairing
