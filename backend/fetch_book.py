import requests


"""
This fetches the content that was given just added an error checker. it fetches all the ebook content by book id
"""
def fetch_content(book_id):

    content_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"

   
    content_response = requests.get(content_url)

    if content_response.status_code != 200:
        raise Exception("Failed to fetch content for ", book_id)

    content = content_response.text

    return content

   
    
"""
this fetches the meta data, had to change the url because i was getting an error code but found the correct one, used this to get the title and summary of the book by book id
"""

def fetch_metadata(book_id):

    metadata_url = f"https://gutendex.com/books/?ids={book_id}"

    metadata_response = requests.get(metadata_url)

    if metadata_response.status_code != 200:
        raise Exception("Failed to fetch metadata for ", book_id)
    
    return metadata_response.json()

"""
This is a cleaner function that marks the start and end of the book but it got too complicated in terms of small differences in the markers and spacing so i decided not to include it
"""

"""
def clean_text(text):

    beginning = text.find("*** START OF THE PROJECT GUTENBERG EBOOK HAMLET ***")
    ending = text.find("*** END OF THE PROJECT GUTENBERG EBOOK HAMLET ***")
    
    lenStart = len("*** START OF THE PROJECT GUTENBERG EBOOK HAMLET ***")
    
    if beginning == -1 or ending == -1:
        raise ValueError("Could not find beginning or end in the text")

    return text[beginning + lenStart: ending].strip()
"""

"""
this function gets the name of the book by accessing the metadata json ->results -> title

"""
def getBookName(book_id):
    try:
        metadata = fetch_metadata(book_id)
        res = metadata.get("results", [])
        if res:
            return res[0].get('title', "Unknown Book")
        return "Unknown Book"
    except:
        return "Unknown Book"
    

"""
This is the get summary function that gets the summary paragraph from the metadata json ->results ->summaries
"""
    

def get_summary(book_id):
    try:
        metadata= fetch_metadata(book_id)
        res = metadata.get("results",[])
        if res and "summaries" in res[0]:
            summary = res[0]["summaries"]
        if summary:
            return summary[0]
        else:
            return "Not Available"
    except Exception as e:
        print(e)
        return "Not Available"
    




