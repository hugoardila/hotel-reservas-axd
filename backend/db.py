import os
import sqlite3

DB_PATH = os.getenv("HOTEL_DB_PATH", "/data/hotel.sqlite")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()

    conn.executescript("""
    CREATE TABLE IF NOT EXISTS hotels (
        id INTEGER PRIMARY KEY,
        city TEXT NOT NULL UNIQUE,
        room_capacity INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS room_types (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS hotel_rooms (
        id INTEGER PRIMARY KEY,
        hotel_id INTEGER NOT NULL,
        room_type_id INTEGER NOT NULL,
        total_rooms INTEGER NOT NULL,
        FOREIGN KEY(hotel_id) REFERENCES hotels(id),
        FOREIGN KEY(room_type_id) REFERENCES room_types(id),
        UNIQUE(hotel_id, room_type_id)
    );

    CREATE TABLE IF NOT EXISTS rates (
        id INTEGER PRIMARY KEY,
        hotel_id INTEGER NOT NULL,
        room_type_id INTEGER NOT NULL,
        season TEXT NOT NULL,
        base_rate REAL NOT NULL,
        person_rate REAL NOT NULL,
        FOREIGN KEY(hotel_id) REFERENCES hotels(id),
        FOREIGN KEY(room_type_id) REFERENCES room_types(id),
        UNIQUE(hotel_id, room_type_id, season)
    );

    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY,
        hotel_id INTEGER NOT NULL,
        room_type_id INTEGER NOT NULL,
        check_in TEXT NOT NULL,
        check_out TEXT NOT NULL,
        rooms INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        FOREIGN KEY(hotel_id) REFERENCES hotels(id),
        FOREIGN KEY(room_type_id) REFERENCES room_types(id)
    );
    """)

    hotels = [
        (1, "Barranquilla", 4),
        (2, "Cali", 6),
        (3, "Cartagena", 8),
        (4, "Bogotá", 6)
    ]

    conn.executemany(
        "INSERT OR IGNORE INTO hotels(id,city,room_capacity) VALUES(?,?,?)",
        hotels
    )

    room_types = [
        (1, "estandar"),
        (2, "premium"),
        (3, "vip")
    ]

    conn.executemany(
        "INSERT OR IGNORE INTO room_types(id,name) VALUES(?,?)",
        room_types
    )

    inventory = [
        # Barranquilla
        (1, 1, 1, 30),
        (2, 1, 2, 3),

        # Cali
        (3, 2, 2, 20),
        (4, 2, 3, 2),

        # Cartagena
        (5, 3, 1, 10),
        (6, 3, 2, 1),

        # Bogotá
        (7, 4, 1, 20),
        (8, 4, 2, 20),
        (9, 4, 3, 2)
    ]

    conn.executemany("""
        INSERT OR IGNORE INTO hotel_rooms
        (id,hotel_id,room_type_id,total_rooms)
        VALUES(?,?,?,?)
    """, inventory)

    # Tarifas DE PRUEBA porque el enunciado no define valores.
    rates = [
        (1,1,1,"baja",180000,15000),
        (2,1,1,"alta",240000,20000),
        (3,1,2,"baja",260000,20000),
        (4,1,2,"alta",340000,25000),

        (5,2,2,"baja",250000,18000),
        (6,2,2,"alta",330000,24000),
        (7,2,3,"baja",420000,25000),
        (8,2,3,"alta",560000,35000),

        (9,3,1,"baja",220000,18000),
        (10,3,1,"alta",320000,25000),
        (11,3,2,"baja",340000,25000),
        (12,3,2,"alta",480000,35000),

        (13,4,1,"baja",200000,15000),
        (14,4,1,"alta",260000,20000),
        (15,4,2,"baja",290000,20000),
        (16,4,2,"alta",380000,28000),
        (17,4,3,"baja",450000,30000),
        (18,4,3,"alta",600000,40000)
    ]

    conn.executemany("""
        INSERT OR IGNORE INTO rates
        (id,hotel_id,room_type_id,season,base_rate,person_rate)
        VALUES(?,?,?,?,?,?)
    """, rates)

    # Reservas simuladas para demostrar disponibilidad.
    conn.executemany("""
        INSERT OR IGNORE INTO bookings
        (id,hotel_id,room_type_id,check_in,check_out,rooms,status)
        VALUES(?,?,?,?,?,?,?)
    """, [
        (1,4,1,"2026-10-10","2026-10-15",5,"active"),
        (2,3,1,"2026-12-20","2026-12-27",3,"active")
    ])

    conn.commit()
    conn.close()
