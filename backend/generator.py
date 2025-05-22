from fetch_book import fetch_content, getBookName, get_summary
from utilities import get_characters, split_chunks, generate_book_cover, get_interactions
import json

"""
This build function calls all of the fetchers in the fetch_content file and gets the raw text, title of book, summary of the book
it then calls the plit chunk function to split of the text into multiple chunks to help limit the characters and token usage in gpt 4
i split it into 1 chunk to test most of this project and scaled it up to 10, it cost a lot of money per run to do 10
I then made sure to merge the json files that my get-character and get interaction functions in utlities produces and makes sure they arent duplicated
fially i dump all of the interactions into interactios.json so that i can can use them in the flask app. I also call the cover image function which prompts dall-e to generate
an ai image of the book thats inputted this funtion returns the title of the book, the characters(unteractions), the cover image, and the summary
"""

def build_book_data(book_id):
    text = fetch_content(book_id)
    title = getBookName(book_id)
    summary = get_summary(book_id)
    chunks = split_chunks(text)

    character_set = set()
    for chunk in chunks[:10]:
        try:
            result = get_characters(chunk)
            lines = [line.strip().title() for line in result.splitlines() if line.strip()]
            character_set.update(lines)
        except Exception as e:
            print(e)
            continue
    characters = sorted(list(character_set))

    merged_interactions = {}
    for chunk in chunks[:5]:
        try:
            result = get_interactions(chunk)
            for speaker, targets in result.items():
                speaker = speaker.strip().title()
                if speaker not in merged_interactions:
                    merged_interactions[speaker] = {}
                for target, count in targets.items():
                    target = target.strip().title()
                    if speaker == target:
                        continue
                    merged_interactions[speaker][target] = (
                        merged_interactions[speaker].get(target, 0) + count
                    )
        except Exception as e:
            print(e)
            continue



    with open("data/interactions.json", "w") as f:
        json.dump(merged_interactions, f, indent=2)

    cover_image = generate_book_cover(title)
        
    return title, characters, cover_image, summary
