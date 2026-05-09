import pandas as pd
from os import system
import subprocess
from concurrent.futures import ThreadPoolExecutor


def downloadSong(name):
    system(
        f'yt-dlp -x --audio-format mp3 --embed-thumbnail --add-metadata "ytsearch1:{name}"'
    )


df = pd.read_csv("~/Music/liked.csv")
df = df["Track Name"]

# i set the no. of workers to be 16 cause my cpu can handle it, don't blindly put anything in there or you might make ur computer a toaster ! if you have no idea of what ur cpu can handle start with a 2 or 4, or if u have a really potato pc, start with a 1
with ThreadPoolExecutor(max_workers=16) as executor:
    executor.map(downloadSong, df)


# this is just some shit i needed to download my spotify playlost offline
# 1. go to exportify and export your playlist to a csv
# 2. come here and get the name
# 3. feed the names as search keywords for yt-dlp, so that it downloads the audio from the first search result
#  yt-dlp -x --audio-format mp3 --embed-thumbnail --add-metadata "ytsearch1:kabhi jo badal barse"
#  yeah ik that its not that reliable cause the first search result isnt often the needed one but what do you want ? me to download 177 songs from the internet manually ?


#  Nothing serious just a utility/hobby/ idiotic project to just get a free commit !

