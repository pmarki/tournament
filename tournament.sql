-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


Create database tournament;
create table players (id serial, name text, win integer, maches integer);
create table matches (id serial, player1 text, player2 text, winner text);
