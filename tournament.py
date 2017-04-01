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
    c.execute("UPDATE Matches SET wins = 0, matchesplayed = 0;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM Players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    player_count = 0
    c.execute("select count(*) as pcount from Players;")
    player_count = int(c.fetchone()[0])
    conn.commit()
    conn.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database."""

    conn = connect()
    c = conn.cursor()
    d = conn.cursor()
    c.execute("INSERT INTO Players(name) values(%s);", (name,))
    c.execute("SELECT max(pid) from Players")
    pid = int(c.fetchone()[0])
    d.execute("""INSERT INTO Matches(pid, matchesplayed, wins)
              values(%s, 0, 0);""", (pid,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins."""

    conn = connect()
    c = conn.cursor()
    c.execute("""SELECT Players.pid, Players.name, Matches.wins,
              Matches.matchesplayed FROM Players LEFT JOIN Matches on
              Players.pid=Matches.pid ORDER BY Matches.wins;""")
    player_standings = c.fetchall()
    conn.commit()
    conn.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players."""

    conn = connect()
    w = conn.cursor()
    l = conn.cursor()
    w.execute("""UPDATE Matches SET wins=wins + 1,
              matchesplayed=matchesplayed + 1 WHERE pid=%s""", (winner,))
    l.execute("""UPDATE Matches SET matchesplayed = matchesplayed + 1 WHERE
              pid = %s """, (loser,))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match."""

    conn = connect()
    c = conn.cursor()
    c.execute("""SELECT Players.pid, Players.name FROM Players LEFT JOIN Matches on
              Players.pid=Matches.pid ORDER BY Matches.wins""")
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
