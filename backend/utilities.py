from openai import OpenAI
import os
from dotenv import load_dotenv
import re
import json
load_dotenv()

client = OpenAI()


#hamlet has about 35k chars so need to chunk to prevent exceeding max tokens


def split_chunks(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    curr_chunk = ""

    for sent in sentences:
        if len(curr_chunk) + len(sent) < 3000:
            curr_chunk += sent + " "
        else:
            chunks.append(curr_chunk.strip())
            curr_chunk = sent + " "
    
    if curr_chunk:
        chunks.append(curr_chunk.strip())
    
    return chunks

"""
This function gets all the characters in the text
"""

def get_characters(text):
    prompt = (
        "You are analyzing a literary work (book/play/novel/etc..). "
        "List all major and minor chatacters mentioned in the text. "
        "output all character names, only output one character name per line, no additional explanation or commentary. "
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt + "\n\n" + text[:3000]}],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
"""
This function gets all the character interactions in the text and returns them
as a json of character to object that maps out to the number of interactions
this prompt otok multiple tries to get it to work
"""
def get_interactions(text):
    prompt = (
        "You are analyzing a literary work (book/play/novel/etc..). "
        "For each speaking character, return a JSON object where each key is a character, "
    "and the value is another object mapping other characters they *speak to* or *mention by name*, with the number of times they do. "
    "Ignore interactions where characters only speak to themselves or narrate. Do not include the speaker as their own interaction. "
    "Use Title Case for all names. Format exactly as valid JSON.\n\n"
    "Format:\n"

        "Format your answer like this:\n\n"
        "{\n"
        "  \"Character A\": {\"Character B\": 3, \"Character C\": 2},\n"
        "  \"Character B\": {\"Character A\": 1}\n"
        "}\n\n"
        "Only returna valid JSON. No explanations or commentary.\n\n"
        "Text:\n" + text
         )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("failed to parse JSON")
        return {}
    

"""
This is the Dall-e functio that calls it ot generate a image that works well
as a cover for it, i just thought this would be a nice addition
"""
def generate_book_cover(bookName = None):
    
    prompt = f"give me a illlustration that fits as a movie poster for the book: '{bookName}', no added text or title"
        
    try:
        response = client.images.generate(
            model = "dall-e-3",
            prompt = prompt,
            size = "1024x1024",
            quality = "standard",
            n = 1
        )
        return response.data[0].url
    except:
        return None
