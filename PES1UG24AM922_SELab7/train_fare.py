
BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]


def parse_pnr(pnr):
    if not isinstance(pnr, str):
        raise ValueError("PNR must be a string")

    pnr = pnr.strip()

    if len(pnr) != 10 or not pnr.isascii() or not pnr.isdigit():
        raise ValueError("PNR must contain exactly 10 digits")

    return int(pnr[0]), int(pnr[1:])


def journey_distance(distances_csv):
    if not isinstance(distances_csv, str):
        raise ValueError("Distances must be a CSV string")

    parts = [part.strip() for part in distances_csv.split(",")]

    if len(parts) < 2:
        raise ValueError("At least two station distances are required")

    if any(not part or not part.isascii() or not part.isdigit()
           for part in parts):
        raise ValueError("All distances must be non-negative integers")

    distances = [int(part) for part in parts]

    if any(distances[i] > distances[i + 1]
           for i in range(len(distances) - 1)):
        raise ValueError("Distances must be in ascending order")

    return distances[-1] - distances[0]


def berth_type(seat):
    if not isinstance(seat, str):
        raise ValueError("Seat must be a string")

    parts = seat.strip().split("-")

    if len(parts) != 2:
        raise ValueError("Seat must be in COACH-NUMBER format")

    coach, number = parts[0].strip(), parts[1].strip()

    if (
        not coach
        or not coach.isascii()
        or not coach[0].isalpha()
        or not coach.isalnum()
    ):
        raise ValueError("Invalid coach name")

    if not number or not number.isascii() or not number.isdigit():
        raise ValueError("Seat number must be a positive integer")

    number = int(number)

    if number < 1:
        raise ValueError("Seat number must be greater than zero")

    return coach.upper(), BERTHS[number % len(BERTHS)]


def main():
    try:
        print("==== Running parse_pnr ====")
        user_input = input("Enter a 10 digit PNR (e.g. 4521367890): ")
        result = parse_pnr(user_input)
        print("Zone and Number:", result)

        print("\n==== Running journey_distance ====")
        user_input = input("Enter station distances as CSV (e.g. 0,120,340): ")
        result = journey_distance(user_input)
        print("Total Distance:", result)

        print("\n==== Running berth_type ====")
        user_input = input("Enter coach and seat (e.g. S3-45): ")
        result = berth_type(user_input)
        print("Coach and Berth:", result)

    except ValueError as error:
        print("Invalid input:", error)


if __name__ == "__main__":
    main()

