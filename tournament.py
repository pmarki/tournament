#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    DB = connect()
    cur = DB.cursor()
    cur.execute("delete from matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("delete from players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("select count(id) as num from players;")
    sql = cur.fetchone();
    DB.close()
    return sql[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("insert into players (name, win, matches) values (%s, 0, 0);", (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("select id, name, win, matches from players order by win desc; ")
    sql = cur.fetchall()
    DB.close()
    return sql



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute('select win, matches from players where ID = %s;', (winner,))
    win = cur.fetchall();
    cur.execute('select win, matches from players where ID = %s;', (loser,))
    lost = cur.fetchall();
    cur.execute('update players set win = %s, matches = %s  where ID = %s; ', (win[0][0]+1, win[0][1]+1, winner))
    cur.execute('update players set matches = %s  where ID = %s; ',  (lost[0][1]+1,loser))
    DB.commit()
    DB.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("select id, name from players order by win desc; ")
    sql = cur.fetchall()
    n = 0
    output = []
    rowEven = ()
    for row in sql:
        if n%2 == 0:
            rowEven = row
        else:    
            output.append((row + rowEven))
        n += 1
    DB.close()
    return output

