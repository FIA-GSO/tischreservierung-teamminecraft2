SELECT * FROM tische WHERE tischnummer NOT IN
  (SELECT DISTINCT r.tischnummer FROM reservierungen r
   WHERE (? BETWEEN r.zeitpunkt AND Datetime(r.zeitpunkt, '+60 minutes')) AND r.storniert != True)
