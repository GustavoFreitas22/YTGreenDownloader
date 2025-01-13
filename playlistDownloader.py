from pytubefix import Playlist
from pytubefix.cli import on_progress
from pydub import AudioSegment
import os

url = "https://www.youtube.com/watch?v=p3dHMZiqhgk&list=PLBMjfM9i8btx_otD64WrPTzVT_ftHMfL5&ab_channel=AmAmatel"

path = './musicas/'
 
if not os.path.exists(path):
    os.mkdir(path)
 
pl = Playlist(url)  
for video in pl.videos:
    ys = video.streams.get_audio_only()
    ys.download(path)

for file_name in os.listdir(path):
    if file_name.endswith(".m4a") or file_name.endswith(".webm"):
        file_path = os.path.join(path, file_name)
        audio = AudioSegment.from_file(file_path)
        mp3_file_path = os.path.splitext(file_path)[0] + ".mp3"
        audio.export(mp3_file_path, format="mp3")
        os.remove(file_path)  # Remove o arquivo original após a conversão