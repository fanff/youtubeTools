import os
import json
import argparse,pprint 
# use of https://github.com/rg3/youtube-dl/#embedding-youtube-dl
import youtube_dl

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath
    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

if __name__ == "__main__":
    
    
    parser = argparse.ArgumentParser(description='download playlist.')
    parser.add_argument('--pl',type=str,required=True,
                               help='playlistFile')
    
    args = parser.parse_args()    
    # read playlist to download
    with open(args.pl,"r") as buff:
        listPlaylistUrl = buff.read()

    for urlPlaylist in listPlaylistUrl.split():
        # recuperation des infos d'une playlist 
        ydl_opts = {'playliststart':1,'playlistend':1,'ignoreerrors':'',}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlistInfos = ydl.extract_info(urlPlaylist,False)
        playlistTitle = playlistInfos['title']
        # creer dossier pour playlist et cd dedans
        os.mkdir(playlistTitle)
        with cd(playlistTitle):
            ydl_opts = {'verbose':'','ignoreerrors':''}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([urlPlaylist])
