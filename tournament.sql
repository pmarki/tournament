-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--make sure the datebase is empty and brand new :)
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

create table players (id serial PRIMARY KEY, name text, win integer, matches integer);
create table matches (id serial, player1 integer references players (id), player2 integer references players (id), winner1 boolean);
