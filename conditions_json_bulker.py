import pywikibot
import json
import sys

# Parse conditions.json-like data into a usable structure
def parse_conditions(data):
    parsed_conditions = []
    for condition in data:
        parsed_condition = {
            "name": condition.get("strName", ""),
            "friendlyName": condition.get("strNameFriendly", ""),
            "description": condition.get("strDesc", ""),
            "color": condition.get("strColor"),
            "reset_timer": condition.get("bResetTimer", False),
            "display_self": condition.get("nDisplaySelf",),
            "display_other": condition.get("nDisplayOther",),
            "duration": condition.get("fDuration"),
            "removeAll": condition.get("bRemoveAll", False),
            "persists": condition.get("bPersists", False),
            "fatal": condition.get("bFatal", False),
            "blocks": condition.get("strAnti"),
            "loot": ", ".join(condition.get("aPer", [])),
        }
        parsed_conditions.append(parsed_condition)
    return parsed_conditions

# Generate the wikitext for a single condition page
def generate_wikitext(condition):
    wikitext = f"""{{{{DISPLAYTITLE:{condition['friendlyName']}}}}}
{{{{Infobox Condition|
|Name={condition['name']}
|FriendlyName={condition['friendlyName']}
|Description={condition['description']}
|Color={condition['color']}
|DisplaySelf={condition['display_self']}
|DisplayOther={condition['display_other']}
|ResetTimer={condition['reset_timer']}
|Duration={condition['duration']}
|Fatal={condition['fatal']}
|RemoveAll={condition['removeAll']}
|Persists={condition['persists']}
|Loot={condition['loot']}
|Blocks={condition['blocks']}
}}}}
"""
    return wikitext

# Upload pages to the wiki
def upload_conditions(conditions, site, parent_page):
    for condition in conditions:
        # Define the page title as a subpage of the parent
        page_title = f"{parent_page}/{condition['friendlyName']}"
        wikitext = generate_wikitext(condition)
        page = pywikibot.Page(site, page_title)

        if page.exists():
            print(f"Page {page_title} already exists. Skipping.")
        else:
            page.text = wikitext
            page.save(f"Added condition page for {condition['name']}.")
            print(f"Uploaded page: {page_title}")

# Main function
def main():
    # Check for conditions file path argument
    if len(sys.argv) < 3:
        print("Usage: python3 upload_conditions_new_structure.py <conditions_file.json> <parent_page>")
        sys.exit(1)

    conditions_file = sys.argv[1]
    parent_page = sys.argv[2]  # Parent page under which subpages will be created

    # Load the conditions file
    try:
        with open(conditions_file, "r") as file:
            conditions_data = json.load(file)
    except Exception as e:
        print(f"Error loading file {conditions_file}: {e}")
        sys.exit(1)

    # Parse the conditions data
    conditions = parse_conditions(conditions_data)

    # Load the MediaWiki site
    site = pywikibot.Site()  # Assumes the default site configuration
    site.login()

    # Upload the conditions to the wiki
    upload_conditions(conditions, site, parent_page)

if __name__ == "__main__":
    main()

