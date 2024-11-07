# # create_document.py

def create_document(filename: str, title: str, content: str) -> None:
    """Creates a document with the specified title and content."""
    try:
        with open(filename, 'w') as file:
            file.write(f'# {title}\n\n')  # Adding a title with Markdown format
            file.write(content)
        print(f'Document "{filename}" created successfully.')
    except Exception as e:
        print(f'An error occurred while creating the document: {e}')



# def create_document(filename: str, title: str, content: str) -> None:
#     """Creates a document with the specified title and content."""
#     try:
#         with open(filename, 'w') as file:
#             file.write(f'# {title}\n\n')  # Adding a title with Markdown format
#             file.write(content)
#         print(f'Document "{filename}" created successfully.')
#     except Exception as e:
#         print(f'An error occurred while creating the document: {e}')

# if __name__ == '__main__':
#     # Seed data with the specified format and updated subheaders
#     seed_documents = [
#         {
#             "filename": "news_report_1.md",
#             "title": "Breaking News: Major Event Happens",
#             "content": """### Topic
# This is a brief overview of the major event that occurred.

# ### Description
# Here, we will discuss the details about the event, including its implications and reactions from the public.

# ### Works Cited
# 1. Author Name, "Title of Source," Publisher, Date.
# 2. Author Name, "Another Source," Publisher, Date.
# """
#         },
#         {
#             "filename": "news_report_2.md",
#             "title": "Weather Update: Storm Approaching",
#             "content": """### Topic
# This report provides an update on the upcoming storm expected to hit the area.

# ### Description
# Residents are advised to prepare for potential disruptions and to stay informed through official channels.

# ### Works Cited
# 1. National Weather Service, "Severe Weather Alerts," Date.
# 2. Local News Outlet, "Storm Forecast," Date.
# """
#         },
#         {
#             "filename": "news_report_3.md",
#             "title": "Sports Update: Local Team Wins Championship",
#             "content": """### Topic
# In an exciting match, the local team clinched the championship title.

# ### Description
# Fans are celebrating this remarkable victory, marking a significant achievement for the community.

# ### Works Cited
# 1. Sports Network, "Championship Highlights," Date.
# 2. Local Newspaper, "Victory Celebration," Date.
# """
#         },
#         {
#             "filename": "news_report_4.md",
#             "title": "Health Alert: New Virus Detected",
#             "content": """### Topic
# A new virus has been detected in the region, prompting health officials to issue a warning.

# ### Description
# Authorities are investigating the source of the virus and advising the public on safety measures to prevent its spread.

# ### Works Cited
# 1. World Health Organization, "Virus Outbreak Update," Date.
# 2. Local Health Department, "Public Safety Guidelines," Date.
# """
#         },
#         {
#             "filename": "news_report_5.md",
#             "title": "Tech Innovation: Breakthrough in AI",
#             "content": """### Topic
# A significant breakthrough in artificial intelligence has been announced.

# ### Description
# This advancement promises to revolutionize various industries, including healthcare and finance.

# ### Works Cited
# 1. Tech Magazine, "AI Breakthrough Report," Date.
# 2. Research Journal, "Innovations in Artificial Intelligence," Date.
# """
#         }
#     ]

#     # Create seed documents
#     for doc in seed_documents:
#         create_document(doc["filename"], doc["title"], doc["content"])
