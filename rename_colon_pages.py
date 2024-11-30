import pywikibot
import re

def move_pages_with_colon():
    # Connect to the wiki
    site = pywikibot.Site()
    site.login()

    # Define a regex to match titles in the format "WORD: ANOTHER SET OF WORDS"
    title_pattern = re.compile(r"^(.*?):\s*(.+)$")

    # Iterate over all pages in the wiki
    for page in site.allpages():
        title = page.title()
        match = title_pattern.match(title)

        if match:
            # Extract the part after the colon
            new_title = match.group(2)

            # Check if the new title already exists
            new_page = pywikibot.Page(site, new_title)
            if new_page.exists():
                print(f"Page '{new_title}' exists. Deleting it to allow move.")
                try:
                    # Delete the existing target page
                    new_page.delete(reason="Deleting to allow move by bot", prompt=False)
                except pywikibot.exceptions.Error as e:
                    print(f"Failed to delete '{new_title}': {e}")
                    continue

            try:
                # Move the page to the new title
                page.move(new_title, reason="Automated page move by bot", movetalk=True, noredirect=False)
                print(f"Moved '{title}' to '{new_title}' successfully.")
            except pywikibot.exceptions.Error as e:
                print(f"Failed to move '{title}' to '{new_title}': {e}")

# Execute the function
move_pages_with_colon()

