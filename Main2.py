from weird_shenanigan import logo, the_true_b_and_a_magic
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify as Spotify_magic
from youtube_search import YoutubeSearch
import yt_dlp
from datetime import datetime
from os import path, rename, remove
from mutagen.mp4 import MP4, MP4Cover
import urllib.request

logo=logo()
the_true_b_and_a_magic()
def ecrire_fichier(folder_path, file_name, text):
    if not path.exists(folder_path):
        print("The specified directory does not exist.")
    else:
        full_file_path = path.join(folder_path, file_name)

        if path.exists(full_file_path):
            file = open(full_file_path, 'a', encoding="utf-8")
        else:
            file = open(full_file_path, 'w', encoding="utf-8")

        file.write(text)
        file.close()

def lire_fichier(chemin_fichier,coupe = ""):
    """
    Lit un fichier texte et cree une liste pour chaque ligne.

    Args:
        chemin_fichier (str): Chemin du fichier à lire.
        coupe (str): Entre quelle caractaire couper "" <=> "\\n" 

    Returns:
        list: Liste contenant chaque ligne.
    """
    variables = []

    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()

    for i, ligne in enumerate(lignes):
        variables.append(ligne.strip())

    return variables

class Chanson:
    def __init__(soi, titre, artistes, album, dur, lienPoc, uri):
        soi.Titre = titre
        soi.ArtistePrincipal = artistes[0]['name']
        if len(artistes) > 1:
            soi.ArtistesSecondaires = []
            for Monsieur in artistes[1:]:
                soi.ArtistesSecondaires.append(Monsieur['name'])
        soi.album = album
        soi.Duree = dur
        soi.Pochette = lienPoc
        soi.lien = uri
        soi.NomVideo = ""
        soi.LienVideo = ""
        soi.telechargee = False #Todo : le vérifier.

    def searchYt(soi):
        print(soi.Titre)
        soi.liensValables = []
        results = YoutubeSearch(soi.Titre+' - '+soi.ArtistePrincipal+' '+soi.ArtistesSecondaires, max_results=5).to_dict()
        for chanson in results:
            chanson = (chanson['title'], chanson['duration'], chanson['url_suffix'][:20])
            delta=duration_comparison(soi, chanson)
            if delta!=None and name_comparison(soi, chanson):
                soi.liensValables.append([chanson[0], chanson[2], round(delta/1000,3)])
        soi.BestBanger = []
        soi.otherBangers =[[]]
    

    def changerYt(soi):
        pass

    def comparerYt(soi):
        pass

    def forcerYt(soi):
        pass

    def chargerFichier(soi):
        pass

    def modifierFichier(soi):
        pass

    def Telecharger(soi):
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            #'preferredquality': '192',
        }],
        'outtmpl': path.join("downloads", '%(title)s.%(ext)s'),
        'restrictfilenames': False,
        'noplaylist': True}
        #! C'est de la merde ce qui est ici !
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for ProcessedBanger in ydl_opts:# in lien_downloads:
                ydl.download(['http://youtube.com'+ProcessedBanger['lienVideo']])
                urllib.request.urlretrieve(ProcessedBanger['lienImage'], "Pochette.jpg")
                try:
                    audio = MP4("downloads/"+ProcessedBanger['nomVideo']+'.m4a')
                    audio["\xa9nam"]=ProcessedBanger['nomChanson']
                    audio["\xa9ART"]=ProcessedBanger['artistePrincipal']
                    with open("Pochette.jpg", 'rb') as pochette:
                        audio['covr']=[MP4Cover(pochette.read(), imageformat=MP4Cover.FORMAT_JPEG)]
                    audio.save()
                except Exception as e:
                    print(f"Une erreur lors de l'édition de {ProcessedBanger['nomVideo']}: {e}")
                    #ecrire_fichier(".", "Reports", f"\nUne erreur lors de l'édition de {ProcessedBanger['nomChanson']} - {ProcessedBanger['ArtistePrincipal']}, cause : {e}")
                remove('Pochette.jpg')
                rename(f"downloads/{ProcessedBanger['nomVideo']}.m4a", "downloads/"+ProcessedBanger['nomChanson']+' - '+ProcessedBanger['artistePrincipal']+".m4a")

def GetBest(Banger):
    conserve=[]
    try :
        results = YoutubeSearch(Banger[0]+' - '+Banger[1], max_results=5).to_dict()
        for chanson in results:
            chanson = (chanson['title'], chanson['duration'], chanson['url_suffix'][:20])
            delta=duration_comparison(Banger, chanson)
            if delta!=None and name_comparison(Banger, chanson):
                conserve.append([chanson[0], chanson[2], round(delta/1000,3)])
        deltamin=5
        mChanson=0
        for i in range(len(conserve)):
            if conserve[i][2]<deltamin:
                deltamin=conserve[i][2]
                mChanson=i
        if len(conserve)==0: 
            return None
        return conserve[mChanson]
    except Exception as e:
        print(f"Une erreur est survenue avec la recherche de {Banger}: {e}")
        #ecrire_fichier(".", "Reports", f"\nErreur avec {Banger[0]} - {Banger[1]}, cause : {e}")
        return "Merde"

def name_comparison(rech, prop):
    if (rech[1].lower() in prop[0].lower() or rech[0].lower() in prop[0].lower()):
        return True
    else :
        return False

def duration_comparison(rech, prop):
    duration = prop[1].split(":")
    duration_ms = int(duration[0]) * 60000 + int(duration[1]) * 1000
    delta=abs(duration_ms-rech[2])
    if delta<5000 :
        return delta
    else :
        return None
    
def Lister_Chansons_Playlist():
    try:
        Key = lire_fichier("PrivateKey")
        client_id,client_secret,redirect_uri = Key[0],Key[1],Key[2]
    except:
        client_id,client_secret = "",""
        while len(client_id) != 32:
            client_id = input("Insérer votre \"Client ID\" (vous le trouverez à l'adresse https://developer.spotify.com/) : ")
        while len(client_secret) != 32:
            client_secret = input("Insérer votre \"Client secret\" (vous le trouverez à l'adresse https://developer.spotify.com/) : ")
        redirect_uri = input("Insérer votre \"Redirect URIs\" : ")
        from os import rename, path
        if path.exists("PrivateKey"):
            try :
                rename("PrivateKey", "PrivateKey.bak")
            except:
                print("Erreur lors de la création du fichier \"PrivateKey\".")
                return
        #ecrire_fichier(".", "PrivateKey", f"{client_id}\n{client_secret}\n{redirect_uri}\n{logo}")
    sp = Spotify_magic(auth_manager=SpotifyOAuth(client_id,client_secret,redirect_uri,scope="user-library-read"))
    url = "empty"
    while len(url) != 22:
        url = input("Veuillez entrer la fin de l'URL de la playlist Spotify : ")
    uri = 'spotify:playlist:'+url
    liste_des_titres = []
    decalage = 0
    api_call = {'items' : []}
    while len(api_call['items']) == 100 or decalage == 0:
        api_call = sp.playlist_tracks(uri, limit=100, offset=decalage)
        for element in api_call['items']:
            liste_des_titres.append([element["track"]["name"],element["track"]["artists"][0]["name"],element["track"]["duration_ms"],element['track']['album']['images'][0]['url']]) #["artists"][0,1,2,...]["name"] # Je ne prend que le premier artiste.
        decalage += 100
    return liste_des_titres