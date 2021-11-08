DROP TABLE IF EXISTS player;

CREATE TABLE player (
	player_id SERIAL NOT NULL PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	current_club TEXT,
	nationality TEXT NOT NULL,
	dob DATE NOT NULL,
	preffered_pos TEXT,
	modified TIMESTAMP DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION trigger_update_modified()
RETURNS TRIGGER AS
$$
BEGIN
	NEW.modified = NOW();
	RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER update_modified
BEFORE UPDATE ON player
FOR EACH ROW
EXECUTE FUNCTION trigger_update_modified();
