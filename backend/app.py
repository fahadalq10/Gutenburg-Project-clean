from flask import Flask, jsonify, request, render_template
from backend.generator import build_book_data
from urllib.parse import unquote
import json

app = Flask(__name__)


"""
this route gets an empty form and the post takes the book id
analyzes it with the llm and generates a cover image, character
lists, and character interactions, finally it passes them onto the template
"""

characters = {}
interactions = {}

@app.route("/", methods = ["GET", "POST"])
def index():
    global characters, interactions, cover_image
    book_title = ""
    cover_image = ""
    summary = ""

    if request.method == "POST":
        book_id = request.form["book_id"]
        book_title, charData, cover_image, summary = build_book_data(book_id)

        characters = charData
        
        with open("data/interactions.json", "r") as f:
                interactions = json.load(f)

    return render_template("index.html", book_title = book_title, characters = characters, cover_image = cover_image, summary = summary)




"""
This route just takes the character name as an input and finds all
the characters that they interacted with and returns them in a 
json list with the number of interactions
"""

characters = {}

@app.route("/interactions/<name>")
def get_interactions(name):
    
    name = unquote(name).strip().title()

    if name not in interactions:
        return jsonify({"error": "not found"}), 404

    res = []
    for target, count in interactions[name].items(): 
        res.append({"name": target, "count": count})
    return jsonify(res)

if __name__ == "__main__":
     app.run(debug = True)
