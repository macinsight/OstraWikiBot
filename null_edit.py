import pywikibot

def null_edit_pages_using_template(template_name, site):
    """
    Perform null edits on all pages using the specified template.

    :param template_name: The name of the template (without namespace prefix).
    :param site: The Pywikibot Site object for the wiki.
    """
    # Build the template page object
    template_page = pywikibot.Page(site, f"Template:{template_name}")

    # Get all pages transcluding the template
    pages = template_page.getReferences(only_template_inclusion=True)

    for page in pages:
        try:
            # Perform a null edit
            page.touch()
            print(f"Null edit performed on: {page.title()}")
        except Exception as e:
            print(f"Failed to null edit {page.title()}: {e}")

if __name__ == "__main__":
    # Connect to the wiki
    site = pywikibot.Site()  # Assumes user-config.py is set up correctly

    # Specify the template name
    template_name = input("Enter the template name (without 'Template:'): ")

    # Run the null edit script
    null_edit_pages_using_template(template_name, site)

