SELECT * FROM tische WHERE tischnummer NOT IN
  (SELECT DISTINCT r.tischnummer FROM reservierungen r
   WHERE (? BETWEEN Datetime(r.zeitpunkt, '-30 minutes') AND Datetime(r.zeitpunkt, '+30 minutes')) AND r.storniert != True)
