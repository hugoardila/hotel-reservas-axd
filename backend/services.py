from datetime import date, timedelta
from math import ceil

from repositories import HotelRepository


class AvailabilityService:

    @staticmethod
    def season(day):
        # Configuración demostrativa.
        # Alta: diciembre, enero, junio y julio.
        if day.month in (12, 1, 6, 7):
            return "alta"

        return "baja"


    @staticmethod
    def search(city, room_type, check_in, check_out, guests):

        try:
            start = date.fromisoformat(check_in)
            end = date.fromisoformat(check_out)
        except ValueError:
            raise ValueError("Las fechas deben usar formato AAAA-MM-DD.")

        if end <= start:
            raise ValueError(
                "La fecha de salida debe ser posterior a la fecha de entrada."
            )

        if guests < 1:
            raise ValueError(
                "La cantidad de personas debe ser mayor a cero."
            )

        inventory = HotelRepository.get_inventory(
            city,
            room_type
        )

        if not inventory:
            raise LookupError(
                "La sede no dispone de ese tipo de alojamiento."
            )

        rooms_required = ceil(
            guests / inventory["room_capacity"]
        )

        occupied = HotelRepository.occupied_rooms(
            inventory["hotel_id"],
            inventory["room_type_id"],
            check_in,
            check_out
        )

        available_rooms = max(
            0,
            inventory["total_rooms"] - occupied
        )

        available = available_rooms >= rooms_required

        nights = (end - start).days

        total = 0
        breakdown = []

        current = start

        while current < end:

            season = AvailabilityService.season(current)

            rate = HotelRepository.get_rate(
                inventory["hotel_id"],
                inventory["room_type_id"],
                season
            )

            if not rate:
                raise LookupError(
                    "No existe una tarifa configurada."
                )

            daily_total = (
                rooms_required * rate["base_rate"]
                + guests * rate["person_rate"]
            )

            total += daily_total

            breakdown.append({
                "date": current.isoformat(),
                "season": season,
                "room_rate": rate["base_rate"],
                "person_rate": rate["person_rate"],
                "subtotal": daily_total
            })

            current += timedelta(days=1)

        return {
            "hotel": inventory["city"],
            "room_type": inventory["room_type"],
            "guests": guests,
            "capacity_per_room": inventory["room_capacity"],

            "rooms_required": rooms_required,
            "total_rooms": inventory["total_rooms"],
            "occupied_rooms": occupied,
            "available_rooms": available_rooms,

            "available": available,

            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,

            "total": total if available else None,

            "currency": "COP",

            "breakdown": breakdown
        }
