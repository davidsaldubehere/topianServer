from flask import Flask
import json
from ytmusicapi import YTMusic
from youtube_dl import YoutubeDL
app = Flask(__name__)
@app.route('/search/<query>')
def search(query):
#find all songs with the query in the title from youtube and return the url, artist name, song title, and thumbnail url
    ytmusic = YTMusic()
    result = ytmusic.search(query, filter='songs')
    titles = [val['title'] for val in result][:4]
    artists = [val['artists'][0]['name'] for val in result][:4]
    thumbnails = [val['thumbnails'][0]['url'] for val in result][:4]
    ids = [val['videoId'] for val in result][:4]
    return json.dumps({'artists': artists, 'titles': titles, 'thumbnails': thumbnails, 'videoId': ids})
@app.route('/download/<videoId>')
def getAudioLink(videoId):
    ydl_opts = {
    'format': 'bestaudio',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f'https://www.youtube.com/watch?v={videoId}', download=False)
        return (info['formats'][0]['url'])



if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=80)
