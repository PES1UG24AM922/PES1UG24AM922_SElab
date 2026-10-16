"""Hostel room allocation and portal utilities."""

import os
import secrets
import yaml
from flask import Flask, request
from markupsafe import escape

rooms = {}
allocations = {}
waitlist = []
app = Flask(__name__)

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""


def load_config(text=CONFIG):
    """Load hostel configuration and initialize rooms."""
    config = yaml.safe_load(text)
    for block in config["blocks"]:
        info = config["blocks"][block]
        for n in range(1, info["rooms"] + 1):
            rooms[block + str(n)] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }
    return config


def allocate_room(student_id, name, gender, year, preferred=None):
    """Allocate a student to an available room."""
    if not isinstance(year, int):
        return None
    if preferred is None:
        preferred = []

    if student_id in allocations:
        return allocations[student_id]["room"]

    for room_no in preferred + list(rooms.keys()):
        room = rooms.get(room_no)
        if room is None or room["gender"] != gender:
            continue
        if len(room["occupants"]) >= room["capacity"]:
            continue

        room["occupants"].append(student_id)
        allocations[student_id] = {"name": name, "room": room_no, "year": year}
        return room_no

    if student_id not in waitlist:
        waitlist.append(student_id)


def vacate_room(student_id):
    """Remove a student from the allocation records and assigned room."""
    if student_id in allocations:
        room_no = allocations[student_id]["room"]
        if student_id in rooms[room_no]["occupants"]:
            rooms[room_no]["occupants"].remove(student_id)
        del allocations[student_id]


def monthly_fee(student_id, days_stayed):
    """Calculate the fee for completed 30-day periods."""
    if student_id not in allocations:
        return 0
    room = rooms[allocations[student_id]["room"]]
    months = days_stayed // 30
    return months * room["fee"]


def priority_order(students, seniors_first=True):
    """Sort students by academic year."""
    return sorted(students, key=lambda s: s["year"], reverse=seniors_first)


def room_lottery(student_ids):
    """Return student IDs in a cryptographically randomized order."""
    return secrets.SystemRandom().sample(student_ids, len(student_ids))


def vacant_beds():
    """Count total available individual beds across all rooms."""
    total = 0
    for room in rooms.values():
        total += room["capacity"] - len(room["occupants"])
    return total


def connect_warden_db():
    """Connect to the warden database using an environment variable."""
    password = os.environ.get("WARDEN_DB_PASSWORD")
    if not password:
        raise ValueError(
            "Critical Security Error: WARDEN_DB_PASSWORD is not set!"
        )
    return sqlite_connect(host="localhost", user="warden", password=password)


def sqlite_connect(host, user, password):
    """Simulate a database connection and report its status."""
    return {"host": host, "user": user, "connected": len(password) > 0}


@app.route("/room")
def room_lookup():
    """Return the allocation details for a requested student safely."""
    sid = request.args.get("id", "")
    details = escape(str(allocations.get(sid)))
    return f"<h1>Room for {escape(sid)}: {details}</h1>"


def main():
    """Run the hostel allocation demonstration."""
    load_config()
    print("Rooms:", list(rooms.keys()))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))

    print("Occupants of A1 before vacating:", rooms["A1"]["occupants"])
    vacate_room("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Vacant beds:", vacant_beds())


if __name__ == "__main__":
    main()
