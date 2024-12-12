import json
import argparse

def calculate_damage_rating(items):
    total_damage = 0
    item_count = 0

    for item in items:
        fWear = item.get("fWearAccrued", 0)
        total_damage += fWear
        item_count += 1

    avg_damage = total_damage / item_count if item_count > 0 else 0

    if avg_damage <= 0.5:
        return "E", avg_damage
    elif avg_damage <= 0.8:
        return "D", avg_damage
    elif avg_damage <= 0.95:
        return "C", avg_damage
    elif avg_damage <= 0.99:
        return "B", avg_damage
    else:
        return "A", avg_damage

def calculate_maneuverability_rating(mass, rcs_count):
    ratio = mass / rcs_count if rcs_count > 0 else float('inf')

    if ratio <= 300:
        return "A", ratio
    elif ratio <= 500:
        return "B", ratio
    elif ratio <= 750:
        return "C", ratio
    elif ratio <= 1500:
        return "D", ratio
    else:
        return "E", ratio

def categorize_size(tiles):
    if tiles < 250:
        return "Small"
    elif tiles < 900:
        return "Medium"
    elif tiles < 1600:
        return "Lunamax"
    elif tiles < 2300:
        return "Ceresmax"
    elif tiles < 3000:
        return "Titanmax"
    elif tiles < 3700:
        return "Very large"
    else:
        return "Ultra large"

def analyze_ship(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        for ship in data:
            print(f"\n--- Ship Analysis ---")

            # Size Analysis
            if 'aItems' in ship:
                min_x = min(item['fX'] for item in ship['aItems'])
                max_x = max(item['fX'] for item in ship['aItems'])
                min_y = min(item['fY'] for item in ship['aItems'])
                max_y = max(item['fY'] for item in ship['aItems'])
                cols = int(max_x - min_x + 1)
                rows = int(max_y - min_y + 1)
                tiles = cols * rows
                size_category = categorize_size(tiles)

            # Damage Rating
            if 'aItems' in ship:
                damage_rating, avg_damage = calculate_damage_rating(ship['aItems'])

            # Specialized Room Count
            specialized_rooms = 0
            if 'aRooms' in ship:
                specialized_rooms = sum(1 for room in ship['aRooms'] if room.get('roomSpec') != 'Blank')

            # Maneuverability Rating
            mass = ship.get('fShallowMass', 0)  # Use fShallowMass for mass
            rcs_count = ship.get('nRCSCount', 0)  # Use nRCSCount directly
            maneuverability_rating, ratio = calculate_maneuverability_rating(mass, rcs_count)

            # Ship Rating
            ship_rating = f"{damage_rating}-{specialized_rooms}-{maneuverability_rating}-{size_category}"
            print(f"Ship Rating: {ship_rating}")

            # Ship Details
            attributes = {
                "Designation": ship.get('designation', 'Unknown'),
                "Make": ship.get('make', 'Unnamed'),
                "Model": ship.get('model'),
                "Year": ship.get('year', 'Unknown'),
            }
            for attr, value in attributes.items():
                print(f"{attr}: {value}")

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze ships in a JSON file.")
    parser.add_argument("file_path", help="Path to the JSON file")
    args = parser.parse_args()

    analyze_ship(args.file_path)

