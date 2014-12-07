from subprocess import call,check_output,CalledProcessError
import os
import ast
import json
import argparse,pprint 
# seem possible to use this 
# -> https://github.com/rg3/youtube-dl/#embedding-youtube-dl
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


commandName = "youtube-dl"

if __name__ == "__main__":
    
    
    parser = argparse.ArgumentParser(description='download playlist.')
    parser.add_argument('--pl',type=str,required=True,
                               help='playlistFile')

    args = parser.parse_args()
    noDashManifest = "--youtube-skip-dash-manifest"
    
    # read playlist to download
    with open(args.pl,"r") as buff:
        listPlaylistUrl = buff.read()

    for urlPlaylist in listPlaylistUrl.split():
        
        print "Working on"
        print urlPlaylist
        # recuperation des infos d'une playlist 
        try:
            playlistInfos =  check_output([commandName, "-J", "-i", urlPlaylist])
            
            print "after check" 
            #playlistInfosDict = ast.literal_eval(playlistInfos)
            playlistInfosDict = json.loads(playlistInfos)
            playlistTitle = playlistInfosDict['title']
            # creer dossier pour playlist et cd dedans
            os.mkdir(playlistTitle)
            with cd(playlistTitle):
                call([commandName, "-v","-i", noDashManifest,urlPlaylist])
        except(CalledProcessError):
            print "no download of playlist "+ urlPlaylist

