"""
The purpose of this simplistic flask server is for the 
front end (Javascript) to retrieve the audio generated from 
the conversation with ChatGPT.
"""

from flask import Flask, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/audio")
def get_audio():

    file_path = "audio/message.wav"

    return send_file(
        file_path,
        mimetype="audio/wav", 
        as_attachment=True, 
    )

app.run(debug=True)