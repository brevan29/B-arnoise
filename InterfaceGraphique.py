from Main2 import*
from tkinter import*
import tkinter.ttk as ttk

class fenetre(Tk): 
    def __init__(self):
        Tk.__init__(self) 
        self.title("b-arnoise en fonction")
        self.menuBar()
        self.geometry('520x300')
        self.resizable(1,0)
        self.client_id,self.client_secret,self.redirect_uri = "", "", ""

    def menuBar(self):
        menu_bar = Menu(self)

        menu_bar.add_command(label="Importer une playlist", command=self.importPlaylist)
        menu_bar.add_command(label="Sauvegarder le travail", command=self.sauver)
        menu_bar.add_command(label="Tout télécharger", command=self.toutTélécharger)
        menu_bar.add_command(label="Rentrer les clés", command=self.setPrivateKey)
        menu_bar.add_command(label="Quitter", command=self.quit)
        self.config(menu=menu_bar)

    def importPlaylist(self):
        self.zoneImport = Frame(self)
        self.zoneImport.grid(row = 0, column = 0)
        self.Type = ttk.Combobox(self.zoneImport, values=["Artiste", "Album", "Playlist"], width=9)
        self.Type.grid(padx=10, pady=5, column=0, row=0)
        self.ecrireURI = ttk.Entry(self.zoneImport, width=28)
        self.ecrireURI.grid(padx=5, pady=5, column=1, row=0)
        self.jeValide = ttk.Button(self.zoneImport, text='Valider', command=self.valider)
        self.jeValide.grid(padx=10, pady=5, column=2, row=0)
        
    
    def valider(self):
        self.Type = self.Type.get()
        self.URI = self.ecrireURI.get()
        self.zoneImport.destroy()
        self.contenuPlaylist=self.chargerPlaylist()
        self.LancerTableauDesChansons()

    def chargerPlaylist(self):
        contenu=[]
        try :
            Key = lire_fichier("PrivateKey")            
            self.client_id,self.client_secret,self.redirect_uri = Key[0],Key[1],Key[2]
        except :
            self.setPrivateKey()
        sp = Spotify_magic(auth_manager=SpotifyOAuth(self.client_id,self.client_secret,self.redirect_uri,scope="user-library-read"))
        decalage = 0
        api_call = {'items' : []}
        if self.Type=="Playlist":
            while len(api_call['items']) == 100 or decalage == 0:
                api_call = sp.playlist_tracks(f"spotify:playlist:{self.URI}", limit=100, offset=decalage)
                for element in api_call['items']:
                    contenu.append(Chanson(element["track"]["name"], element["track"]["artists"], element["track"]["album"]['name'], element["track"]["duration_ms"], element['track']['album']['images'][0]['url'], element['track']['id']))
                decalage += 100
        return contenu
    
    def setPrivateKey(self):
        self.fenID = Tk()
        self.fenID.resizable(0,0)
        Label(self.fenID, text="Client ID").grid(row=0, column=0, padx=5, pady=2.5)
        Label(self.fenID, text="Client secret").grid(row=0, column=1, padx=5, pady=2.5)
        Label(self.fenID, text="Redirect URI").grid(row=0, column=2, padx=5, pady=2.5)

        self.Entrerclient_id = Entry(self.fenID, width=33, text=self.client_id)
        self.Entrerclient_secret = Entry(self.fenID, width=33, text=self.client_secret)
        self.Entrerredirect_uri = Entry(self.fenID, width=20, text=self.redirect_uri)
        self.jeValide2 = ttk.Button(self.fenID, text='Valider', command=self.valider2)

        self.Entrerclient_id.grid(row=1, column=0)
        self.Entrerclient_secret.grid(row=1, column=1)
        self.Entrerredirect_uri.grid(row=1, column=2)
        self.jeValide2.grid(row=1, column=3)

    def valider2(self):
        if len(self.Entrerclient_id.get()) != 32 or len(self.Entrerclient_secret.get()) != 32: #? Pas ce qu'on veut quoi
            self.Entrerclient_id.config(bg="#ff000096")
            self.Entrerclient_secret.config(bg="#ff000096")
        else :
            self.client_id = self.Entrerclient_id.get()
            self.client_secret = self.Entrerclient_secret.get()
            self.redirect_uri = self.Entrerredirect_uri.get()
            from os import rename, path
            if path.exists("PrivateKey"):
                try :
                    rename("PrivateKey", "PrivateKey.bak")
                except:
                    print("Erreur lors de la création du fichier \"PrivateKey\".")
                    return
            ecrire_fichier(".", "PrivateKey", f"{self.client_id}\n{self.client_secret}\n{self.redirect_uri}\n{logo}")
            self.fenID.destroy()
        
    def LancerTableauDesChansons(self):
        self.TableauChansons = ttk.Treeview(self, columns=("Titre","Artistes", "Album", 'Durée', "URI de Piste", "VidéoYT", "LienYT"), height=20, show='headings')
        self.geometry('1120x300')
        self.TableauChansons.column("Titre", width=200, anchor='center'); self.TableauChansons.heading("Titre", text="Titre")
        self.TableauChansons.column("Artistes", width=150, anchor='center'); self.TableauChansons.heading("Artistes", text="Artistes")
        self.TableauChansons.column("Album", width=150, anchor='center'); self.TableauChansons.heading("Album", text="Album")
        self.TableauChansons.column("Durée", width=70, anchor='center'); self.TableauChansons.heading("Durée", text="Durée")
        self.TableauChansons.column("URI de Piste", width=100, anchor='center'); self.TableauChansons.heading("URI de Piste", text="URI de Piste")
        self.TableauChansons.column("VidéoYT", width=300, anchor='center'); self.TableauChansons.heading("VidéoYT", text="Vidéo Youtube équivalente")
        self.TableauChansons.column("LienYT", width=150, anchor='center'); self.TableauChansons.heading("LienYT", text="Lien de la vidéo")
        self.TableauChansons.grid(row=1, column=0, columnspan=4, sticky='n', pady=5)
        self.ajouterPistes()

    def ajouterPistes(self):
        for chanson in self.contenuPlaylist:
            self.TableauChansons.insert(parent='', index=END, values=[chanson.Titre, chanson.ArtistePrincipal, chanson.album, chanson.Duree, chanson.lien, chanson.NomVideo, chanson.LienVideo])
        self.BoutonRechercheYt = ttk.Button(self, text='Chercher vidéos YT', command=self.chercherYT) #? Pourquoi que mainteant ? Parce que les actions ne peuvent se faire une fois qu'on a un visuel sur les chanons importées.
        self.BoutonModifierLien = ttk.Button(self, text='Modifier un lien YT', command=self.modifier)
        self.BoutonTéléchargerUn = ttk.Button(self, text='Télécharger une Chanson', command=self.telechargerUn)
        self.BoutonToutTélécharger = ttk.Button(self, text='Tout télécharger', command=self.toutTélécharger)
        self.BoutonRechercheYt.grid(row=0, column=0, padx=5, pady=2)
        self.BoutonModifierLien.grid(row=0, column=1, padx=5, pady=2)
        self.BoutonTéléchargerUn.grid(row=0, column=2, padx=5, pady=2)
        self.BoutonToutTélécharger.grid(row=0, column=3, padx=5, pady=2)

    def chercherYT(self): #? Chercher les equivalents YT de TOUTES les chansons.
        assert len(self.contenuPlaylist) == len(self.TableauChansons.get_children())
        ids = self.TableauChansons.get_children()
        for i in range(len(self.contenuPlaylist)):
            BoumBoumTypeMusic = self.contenuPlaylist[i]
            BoumBoumTypeMusic.searchYt()
            if BoumBoumTypeMusic.liensValables != [] and BoumBoumTypeMusic.Titre == self.TableauChansons.item(ids[i])['values'][0]:
                print(self.TableauChansons.item(ids[i]))
                NouvelleValeur = self.TableauChansons.item(ids[i])['values']
                NouvelleValeur[5], NouvelleValeur[6] = BoumBoumTypeMusic.BestBanger[0], BoumBoumTypeMusic.BestBanger[1]
                self.TableauChansons.item(ids[i], values=NouvelleValeur)
                print(self.TableauChansons.item(ids[i]))

    def sauver(self): #? Enregister lensemble des infos dans un fichier json pour pouvoir le rouvrir par la suite.
        # Todo Doit pouvoir contenir les toutes les infos de toutes les chansons et savoir si elles ont étées téléchargées.
        pass
    
    def modifier(self):
        global id, BangersThatNeedHelp, Brevassistance, Valeurs
        BangersThatNeedHelp = self.TableauChansons.selection()[0]
        id = int(BangersThatNeedHelp[1:])
        Valeurs = self.TableauChansons.item(BangersThatNeedHelp)['values']
        Brevassistance = Tk()
        ttk.Label(Brevassistance, text = str(Valeurs[0:3])+"; lien Youtube : ").grid()
        self.DolipraneLikeSolution = Entry(Brevassistance, width=15)
        self.DolipraneLikeSolution.insert(0, "/watch?v=")
        self.DolipraneLikeSolution.grid()
        ttk.Button(Brevassistance, text='Valider', command=self.Valider3).grid()

    def Valider3(self):
        self.DolipraneLikeSolution = self.DolipraneLikeSolution.get()
        Brevassistance.destroy() #Aïe, j'ai mal. J'ai beau être matinal, j'ai mal
        self.contenuPlaylist[id].LienVideo = self.DolipraneLikeSolution
        Valeurs[5],Valeurs[6] = "Tkt, Ajouté manuellement", self.DolipraneLikeSolution
        self.TableauChansons.item(BangersThatNeedHelp, values=Valeurs)

    def telechargerUn(self, chanson):
        chanson.Telecharger()

    def toutTélécharger(self):
        pass

fen = fenetre()
fen.mainloop()