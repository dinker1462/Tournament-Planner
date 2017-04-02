-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE Players (
    id serial PRIMARY KEY,
    name TEXT
);

CREATE TABLE matches (
   match_id SERIAL PRIMARY KEY,
   winner_id INT REFERENCES players(id) ON DELETE CASCADE,
   loser_id INT REFERENCES players(id) ON DELETE CASCADE,
   CHECK (winner_id <> loser_id)
);

CREATE VIEW winner_count AS
SELECT players.id, players.name, COUNT(matches.winner_id) AS total_wins
FROM players LEFT JOIN matches
ON players.id = matches.winner_id
GROUP BY players.id;

CREATE VIEW matches_count AS
SELECT players.id, players.name, COUNT(matches) AS total_matches
FROM players LEFT JOIN matches
ON players.id = matches.winner_id OR players.id = matches.loser_id
GROUP BY players.id;

CREATE OR REPLACE VIEW standings AS
SELECT winner_count.id, winner_count.name, winner_count.total_wins, matches_count.total_matches
FROM winner_count JOIN matches_count ON winner_count.id = matches_count.id
ORDER BY winner_count.total_wins DESC;
