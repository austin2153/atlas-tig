#!/usr/bin/env python3
"""
Solar system planet data - outputs InfluxDB line protocol to stdout.
Executed by Telegraf's inputs.exec plugin on a configured interval.
Telegraf collects the output and forwards it to InfluxDB.
"""

from influxdb_client_3 import Point

PLANETS = [
    ("Earth",   "Terrestrial", False, 1.0,   12742,  1.0,    365.25,  1,   15),
    ("Mercury", "Terrestrial", False, 0.39,  4879,   0.055,  88.0,    0,   167),
    ("Venus",   "Terrestrial", False, 0.72,  12104,  0.815,  225.0,   0,   464),
    ("Mars",    "Terrestrial", False, 1.52,  6779,   0.107,  687.0,   2,   -65),
    ("Jupiter", "Gas Giant",   True,  5.20,  139820, 317.8,  4333.0,  95,  -110),
    ("Saturn",  "Gas Giant",   True,  9.54,  116460, 95.2,   10759.0, 146, -140),
    ("Uranus",  "Ice Giant",   True,  19.19, 50724,  14.5,   30687.0, 28,  -195),
    ("Neptune", "Ice Giant",   True,  30.07, 49244,  17.1,   60190.0, 16,  -200),
    ("Pluto",   "Dwarf",       False, 39.48, 2376,   0.0022, 90560.0, 5,   -225),
]

for name, ptype, has_rings, dist, diam, mass, orbital, moons, temp in PLANETS:
    line = (
        Point("planet_stats")
        .tag("name", name)
        .tag("type", ptype)
        .tag("has_rings", str(has_rings).lower())
        .field("distance_from_sun_au", dist)
        .field("diameter_km", diam)
        .field("mass_earth_masses", mass)
        .field("orbital_period_days", orbital)
        .field("moons", moons)
        .field("avg_temp_celsius", temp)
        .to_line_protocol()
    )
    print(line)
