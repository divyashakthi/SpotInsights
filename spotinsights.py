import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request
import re

app = Flask(__name__)

client_id = 'ab49552708ba40b3ac524a77d47f8558'
client_secret = 'dbff214ff84949bebfe907965df65440'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        playlist_url = request.form['playlist_url']
        pattern = r'playlist\/([a-zA-Z0-9]+)'
        match = re.search(pattern, playlist_url)
        if match:
            playlist_id = match.group(1)
            get_tracks(playlist_id)
    return render_template('index.html')

def get_tracks(playlist_id):
    artist_list = []
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        music_track = item['track']
        artists = music_track['artists']
        artist_names = [artist['name'] for artist in artists]
        artist_list.extend(artist_names)

    artist_counts = pd.Series(artist_list).value_counts()
    colors = sns.color_palette("flare")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 12

    plt.figure(figsize=(10, 6), facecolor='#D8BFD8')
    explode = tuple(0.1 if i == 0 else 0 for i in range(len(artist_counts[:10])))
    pie = artist_counts[:10].plot(kind='pie', colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.85, explode=explode)
    title_font = {'family': 'monospace', 'fontname': 'Consolas', 'size': 26, 'weight': 'bold'}
    pie.set_title('Top 10 Artists in Playlist', fontdict=title_font)
    pie.set_ylabel('')
    pie.legend(artist_counts[:10].index, loc='lower left', bbox_to_anchor=(1.2, 0.1), fontsize=10)
    plt.tight_layout()
    plt.savefig('static/div_insights.png')
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)