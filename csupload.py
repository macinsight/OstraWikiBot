import pywikibot
import json
import sys

# Parse conditions_simple.json-like data into a usable structure
def parse_conditions(data):
    parsed_conditions = []
    for condition_group in data:
        if "aValues" in condition_group:
            values = condition_group["aValues"]
            for i in range(0, len(values), 6):  # Step through entries in chunks of 6
                condition = {
                    "key": values[i],
                    "name": values[i + 1],
                    "description": values[i + 2],
                    "show_to_us": int(values[i + 3]),
                    "show_to_them": int(values[i + 4]),
                    "color_code": values[i + 5]
                }
                parsed_conditions.append(condition)
    return parsed_conditions

# Generate the wikitext for a single condition page
def generate_wikitext(condition):
    wikitext = f"""{{{{DISPLAYTITLE:{condition['name']}}}}}
{{{{Infobox Condition Simple|
|title={condition['name']}
|Name={condition['name']}
|CodeName={condition['key']}
|Description={condition['description']}
|ShowToUs={condition['show_to_us']}
|ShowToThem={condition['show_to_them']}
|Color={condition['color_code']}}}}}
"""
    return wikitext

# Upload pages to the wiki
def upload_conditions(conditions, site, parent_page):
    for condition in conditions:
        # Define the page title as a subpage of the parent
        page_title = f"{parent_page}/{condition['name']}"
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
        print("Usage: python3 upload_conditions_human_readable.py <conditions_file.json> <parent_page>")
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

