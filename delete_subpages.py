import pywikibot

def delete_subpages(parent_page_title):
    # Connect to the site
    site = pywikibot.Site()
    site.login()

    # Get the parent page
    parent_page = pywikibot.Page(site, parent_page_title)

    # Fetch subpages
    subpages = site.allpages(prefix=parent_page.title() + "/")

    # Delete subpages
    for subpage in subpages:
        try:
            print(f"Attempting to delete subpage: {subpage.title()}")
            subpage.delete(reason=f"Deleting subpage of {parent_page.title()}", prompt=False)
            print(f"Deleted subpage: {subpage.title()}")
        except Exception as e:
            print(f"Error deleting {subpage.title()}: {e}")

# Main function
if __name__ == "__main__":
    parent_page_title = "Condition"  # Replace with the title of your parent page
    delete_subpages(parent_page_title)
