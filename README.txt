=====
vagquery
=====

A python library for generating and executing queries for the VAG public transport system
`start.vag.de <https://start.vag.de>`_.

This enables users with disabilities, hackers and you to receive information from the start.vag website.

General usage
============

Two classes are usually used:
    
    import vagquery
    # Query for stations beginning with 'Schwe'
    stations = vagquery.StationQuery("Schwe").query()
    for station in stations:
        print(station)
    
    # Query for next departures of the main railway station (id: 510)
    departures = vagquery.DepartureQuery(510).query()
    for departure in departures:
        print(departure)

Specialized usage
============================

For repeated queries, the query object can be created and run again and again:

    dquery = vagquery.DepartureQuery(510)
    departures = dquery.query()
    # ...
    # much later
    # ...
    departures = dquery.query()

For a custom formating of the departures, the properties of a departure object can be used:
    
    departures = vagquery.DepartureQuery(510).query()
    for departure in departures:
        print(departure.product + " " + str(departure.latitude) + str(departure.longitude))

License
=======

*vagquery* is licensed under the MIT license.
