# Sequence Diagrams for API routes

## /api/v1/table/reserve

```plantuml
@startuml
title /api/v1/table/reserve
 
participant client as c
participant API as a
database database as d
 
c->a: reserve(info)
note left
info = {
  at: "now" | ISODateString,
  persons: int
}
end note
activate a
a->a: validate request date
activate a
deactivate a
alt request date is not valid
a-->>c: reserve(-): HTTP 400 "invalid request date"
else
a->a: validate "persons" parameter
activate a
deactivate a
alt "persons" parameter is not valid
a-->>c: reserve(-): HTTP 400 "invalid 'persons' parameter" 
else
a->d: get_free_tables(datetime, persons)
deactivate a
activate d
d-->>a: get_free_tables(-): tables
deactivate d
activate a
alt no free tables for given parameters
a-->>c: reserve(-): HTTP 404 "no free tables found for given parameters"
else
a->a: determine table to reserve on
activate a
deactivate a
a->d: save_new_reservation(table, datetime)
deactivate a
activate d
d-->>a: save_new_reservation(-): success
deactivate d
activate a
a-->>c: reserve(-): reservation
note left
reservation = {
  reservierungsnummer: int,
  zeitpunkt: ISODateString,
  tischnummer: int,
  pin: string
}
end note
deactivate a
end
end
end
```