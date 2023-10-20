PRAGMA temp_store = 2;
CREATE TEMP TABLE Reserved(TableNumber INTEGER PRIMARY KEY);

INSERT INTO Reserved (Name)
VALUES (SELECT DISTINCT r.tischnummer
        FROM reservierungen r
        WHERE (Datetime('now', 'localtime') BETWEEN r.zeitpunkt
               AND Datetime(r.zeitpunkt, '+60 minutes'))
              AND r.storniert != True);

SELECT * FROM tische WHERE tischnummer NOT IN @Reserved