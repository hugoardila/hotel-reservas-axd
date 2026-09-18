from db import get_connection

class HotelRepository:

    @staticmethod
    def list_hotels():
        db = get_connection()

        rows = db.execute("""
            SELECT
                h.id,
                h.city,
                h.room_capacity,
                rt.name AS room_type,
                hr.total_rooms
            FROM hotel_rooms hr
            JOIN hotels h ON h.id = hr.hotel_id
            JOIN room_types rt ON rt.id = hr.room_type_id
            ORDER BY h.city, rt.name
        """).fetchall()

        db.close()

        return [dict(row) for row in rows]


    @staticmethod
    def get_inventory(city, room_type):
        db = get_connection()

        row = db.execute("""
            SELECT
                h.id AS hotel_id,
                h.city,
                h.room_capacity,
                rt.id AS room_type_id,
                rt.name AS room_type,
                hr.total_rooms
            FROM hotel_rooms hr
            JOIN hotels h ON h.id = hr.hotel_id
            JOIN room_types rt ON rt.id = hr.room_type_id
            WHERE lower(h.city) = lower(?)
            AND lower(rt.name) = lower(?)
        """, (city, room_type)).fetchone()

        db.close()

        return dict(row) if row else None


    @staticmethod
    def occupied_rooms(hotel_id, room_type_id, check_in, check_out):
        db = get_connection()

        row = db.execute("""
            SELECT COALESCE(SUM(rooms),0) AS occupied
            FROM bookings
            WHERE hotel_id = ?
            AND room_type_id = ?
            AND status = 'active'
            AND check_in < ?
            AND check_out > ?
        """, (
            hotel_id,
            room_type_id,
            check_out,
            check_in
        )).fetchone()

        db.close()

        return int(row["occupied"])


    @staticmethod
    def get_rate(hotel_id, room_type_id, season):
        db = get_connection()

        row = db.execute("""
            SELECT *
            FROM rates
            WHERE hotel_id = ?
            AND room_type_id = ?
            AND season = ?
        """, (
            hotel_id,
            room_type_id,
            season
        )).fetchone()

        db.close()

        return dict(row) if row else None
