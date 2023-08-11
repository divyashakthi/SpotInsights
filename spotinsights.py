import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

username='l83z3ki3m59kg3gwigkq1n9hu'
client_id='ac60f560de064304ad3cefba50a23cf0'
client_secret='9dce9377d9244127884f22dc8ae1757e'
redirect='https://www.spotify.com/'
oauth_object=spotipy.SpotifyOAuth(client_id,client_secret,redirect)
client_credentials_manager=SpotifyClientCredentials(client_id,client_secret)
sp=spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_tracks():
    # music_list=[]
    artist_list=[]
    playlist=sp.playlist("7tZjUDmiIwSFl28aOZqKr0")
    for item in playlist['tracks']['items']:
        music_track=item['track']
        artists = music_track['artists']
        artist_names = [artist['name'] for artist in artists]
        artist_list.append(artist_names)
        # music_list.append(music_track['name'])
        # print(artist_list)
    # return music_list

    artist_counts = pd.Series(artist_list).value_counts()
    colors = sns.color_palette("flare")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 12
    
    plt.figure(figsize=(10, 6), facecolor='#D8BFD8')
    explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    pie = artist_counts[:10].plot(kind='pie', colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.85, explode=explode)
    title_font = {'family': 'monospace', 'fontname': 'Consolas', 'size': 26, 'weight': 'bold'}
    pie.set_title('Top 10 Artists in Playlist', fontdict=title_font)
    pie.set_ylabel('')
    pie.legend(artist_counts[:10].index, loc='lower left', bbox_to_anchor=(1.2, 0.1), fontsize=10)
    plt.tight_layout()
    plt.show()

# print(get_artists())
get_tracks()