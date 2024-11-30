import pywikibot
import re

# Define categories to check
CATEGORY_DUID = "Pages with DRUID infoboxes"
CATEGORY_BROKEN_FILES = "Pages with broken file links"

def process_pages():
    # Connect to the wiki
    site = pywikibot.Site()
    site.login()

    # Retrieve pages in both categories
    category_druid = pywikibot.Category(site, CATEGORY_DUID)
    category_broken = pywikibot.Category(site, CATEGORY_BROKEN_FILES)

    # Get intersection of pages in both categories
    pages_druid = set(category_druid.articles())
    pages_broken = set(category_broken.articles())
    pages_to_check = pages_druid.intersection(pages_broken)

    print(f"Found {len(pages_to_check)} pages in both categories.")

    # Define the pattern to find and replace
    search_pattern = r":Intact,\n\s*\.png:Damaged"
    replacement = ""

    # Iterate through the pages and process them
    for page in pages_to_check:
        print(f"Processing page: {page.title()}")

        try:
            # Get the page content
            text = page.text

            # Check if the "Infobox item" template contains the search pattern
            if "|images=" in text and re.search(search_pattern, text):
                # Replace the pattern with the replacement string
                updated_text = re.sub(search_pattern, replacement, text)

                if updated_text != text:
                    # Save the changes
                    page.text = updated_text
                    page.save(summary="Fixing Infobox item image links by removing :Intact,.png:Damaged.")
                    print(f"Updated page: {page.title()}")
            else:
                print(f"No changes needed for: {page.title()}")

        except pywikibot.exceptions.Error as e:
            print(f"Error processing page {page.title()}: {e}")

# Execute the function
process_pages()

