from flask import Flask
import json
from ytmusicapi import YTMusic
from youtube_dl import YoutubeDL
app = Flask(__name__)
def catch(resultList, item, index=None):
    if resultList == None:
        return "John Doe"
    try:
        if index!=None:
            try:
                return resultList[item][index]
            except TypeError:
                return None
        else:
            return resultList[item]
    except KeyError:
        return None
@app.route('/search/<query>')
def search(query):
#find all songs with the query in the title from youtube and return the url, artist name, song title, and thumbnail url
    ytmusic = YTMusic()
    result = ytmusic.search(query, limit=4)
    titles = [catch(val, 'title') for val in result]
    artists = [catch(catch(val, 'artists', 0), 'name') for val in result]
    thumbnails = [catch(catch(val, 'thumbnails', 0), 'url') for val in result]
    ids = [catch(val, 'videoId') for val in result]
    resultType = [catch(val, 'resultType') for val in result]
    return json.dumps({'artists': artists, 'titles': titles, 'thumbnails': thumbnails, 'videoId': ids, 'resultType': resultType})
@app.route('/download/<videoId>')
def getAudioLink(videoId):
    ydl_opts = {
    'format': 'bestaudio',
    'cookiefile': 'cookies.txt',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f'https://www.youtube.com/watch?v={videoId}', download=False)
        return info['url']



if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=80)
