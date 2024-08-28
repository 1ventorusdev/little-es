import re
import json
import csv
import os
import random

class TestError(Exception):
    pass

class Gopen:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

    def open(self, mode="r"):
        if mode == "r":
            # Vérifier si le fichier existe avant de l'ouvrir en mode lecture
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    for line in file:
                        match = re.match(r'^\s*([^:]+)\s*:\s*(.*)\s*$', line)
                        if match:
                            key = match.group(1).strip()
                            value = match.group(2).strip()
                            self.data[key] = value
            else:
                raise FileNotFoundError(f"Le fichier {self.filename} n'existe pas.")
        elif mode == "a":
            try:
                with open(self.filename, 'r') as file:
                    for line in file:
                        match = re.match(r'^\s*([^:]+)\s*:\s*(.*)\s*$', line)
                        if match:
                            key = match.group(1).strip()
                            value = match.group(2).strip()
                            self.data[key] = value
            except FileNotFoundError:
                pass
        elif mode == "m":
            try:
                with open(self.filename, 'r') as file:
                    for line in file:
                        match = re.match(r'^\s*([^:]+)\s*:\s*(.*)\s*$', line)
                        if match:
                            key = match.group(1).strip()
                            value = match.group(2).strip()
                            self.data[key] = value
            except FileNotFoundError:
                self.data = {}
        elif mode == "c+":
            # Créer tous les dossiers nécessaires s'ils n'existent pas
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            # Ouvrir en mode création ou modification
            with open(self.filename, 'a+') as file:
                file.seek(0)
                for line in file:
                    match = re.match(r'^\s*([^:]+)\s*:\s*(.*)\s*$', line)
                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip()
                        self.data[key] = value
        else:
            raise ValueError("Mode non pris en charge")

    def save(self):
        # Vérifier si le fichier existe avant de le sauvegarder
        if os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                for key, value in self.data.items():
                    file.write(f"{key} : {value}\n")
        else:
            raise FileNotFoundError(f"Le fichier {self.filename} n'existe pas.")

    def createfilebydico(self, variables):
        for key, value in variables.items():
            if key in self.data:
                try:
                    existing_value = int(self.data[key])
                    new_value = int(value)
                    self.data[key] = existing_value + new_value
                except ValueError:
                    self.data[key] = value
            else:
                self.data[key] = value

    def createdicobyfile(self):
        dico = {}
        with open(self.filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                dico[key] = value
        return dico

    def delete(self, key):
        if key in self.data:
            del self.data[key]
        else:
            print(f"La variable '{key}' n'existe pas.")

    def variable_exists(self, key):
        return key in self.data

    def export_data(self, filename, format="json"):
        if format == "json":
            with open(filename, 'w') as file:
                json.dump(self.data, file, indent=4)
        elif format == "csv":
            with open(filename, 'w') as file:
                writer = csv.writer(file)
                for key, value in self.data.items():
                    writer.writerow([key, value])
        else:
            print("Format non pris en charge.")

    def import_data(self, filename, format="json"):
        if format == "json":
            with open(filename, 'r') as file:
                self.data = json.load(file)
        elif format == "csv":
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                self.data = {rows[0]: rows[1] for rows in reader}
        else:
            print("Format non pris en charge.")

    def import_item(self, other_inventory, keys=None):
        # Importer des données d'un autre inventaire
        if keys is None:
            keys = other_inventory.data.keys()
        for key in keys:
            self.data[key] = other_inventory.data[key]

    def export_item(self, other_inventory, keys=None):
        # Exporter des données vers un autre inventaire
        if keys is None:
            keys = self.data.keys()
        for key in keys:
            other_inventory.data[key] = self.data[key]

    def move_item(self, item_key, quantity, other_inventory):
        # Déplacer un certain nombre d'éléments d'un inventaire à un autre
        if item_key in self.data:
            self.data[item_key] -= quantity
            if self.data[item_key] <= 0:
                del self.data[item_key]
            if item_key in other_inventory.data:
                other_inventory.data[item_key] += quantity
            else:
                other_inventory.data[item_key] = quantity

    def check_data_integrity(self):
        for key, value in self.data.items():
            if not value.strip().startswith(":"):
                if ":" not in value:
                    print(f"Erreur: La variable '{key}' ne contient pas de valeur.")
                else:
                    print(f"Erreur: La variable '{key}' contient un ':' inattendu.")
                return False
        print("Intégrité des données vérifiée avec succès.")
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save()

    def __getitem__(self, key):
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value

    
class Pnj:
    def __init__(self, name):
        self.name = name

    def create_pnj(self, locatdir, years_old, type="pnj", story="none"):
        story_location = os.path.join(locatdir, self.name, self.name+"-story.txt")
        if story == "none":
            pass
        else:
            with open(story_location, "w+") as story_info:
                story_info.write(story)

        with Gopen(os.path.join(locatdir, self.name, self.name+"-info.gdta")) as dta:
            dta.open("c+")
            dta["name"] = self.name
            dta["years_old"] = years_old
            dta["type"] = type
            dta["story_location"] = story_location

    def modify_pnj(self, locatdir, years_old, type="pnj", story="none"):
        if os.path.exists(os.path.join(locatdir, self.name)):
            story_location = os.path.join(locatdir, self.name, self.name+"-story.txt")
            if story == "none":
                pass
            else:
                with open(story_location, "w+") as story_info:
                    story_info.write(story)
            
            with Gopen(os.path.join(locatdir, self.name, self.name+"-info.gdta")) as dta:
                dta.open("m")
                dta["name"] = self.name
                dta["years_old"] = years_old
                dta["type"] = type
                dta["story_location"] = story_location
        else:
            print(f"il semble que votre pnj nommé {self.name} ne se trouve pas au bonne endroit")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class Player:
    def __init__(self, name):
        self.name = name

    def create_player(self, locatdir, type, breed, health, defense, dgt, inventory="yes", story="none"):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        inventory_location = os.path.join(player_location, "inventory.gdta")
        story_location = os.path.join(player_location, "story.txt")

        with Gopen(data_location) as dta:
            dta.open("c+")
            dta["name"] = self.name
            dta["type"] = type
            dta["class"] = breed
            dta["hp"] = health
            dta["Defense"] = defense
            dta["DGT"] =  dgt
            dta["story"] = story_location

        if inventory == "yes":
            with Gopen(inventory_location) as dta:
                dta.open("c+")

        elif inventory == "no":
            pass

        else:
            print("erreur")

        if story == "none":
            pass
        else:
            with open(story_location, "w+") as story_dta:
                story_dta.write(story)

    def use_health(self, locatdir):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("a")
            return int(dta["hp"])

    def use_defense(self, locatdir):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("a")
            return int(dta["Defense"])

    def use_dgt(self, locatdir):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("a")
            return int(dta["DGT"])

    def use_breed(self, locatdir):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("a")
            return dta["class"]

    def use_type(self, locatdir):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("a")
            return dta["type"]

    def modify_health(self, locatdir,  health):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("m")
            dta["hp"] = health

    def modify_defense(self, locatdir, defense):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("m")
            dta["defense"] = defense

    def modify_dgt(self, locatdir, dgt):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("m")
            dta["DGT"] = dgt

    def modify_breed(self, locatdir, breed):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("m")
            dta["class"] = breed

    def modify_type(self, locatdir, type):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "player_data.gdta")
        with Gopen(data_location) as dta:
            dta.open("m")
            dta["type"] = type

    def __enter__(self):
        return self
    
    def __getitem__(self, key):
        return self.data.get(key)
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

class Inventory:
    def __init__(self, name):
        self.name = name

    def stock(self, locatdir, dico):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "inventory.gdta")
        with Gopen(data_location) as item:
            item.open("a")
            item.create_dico(dico)

    def use(self, locatdir, name_data):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "inventory.gdta")
        with Gopen(data_location) as item:
            item.open("r")
            return int(item[name_data])

    def modify(self, locatdir, name_data, value):
        player_location = os.path.join(locatdir, self.name)
        data_location = os.path.join(player_location, "inventory.gdta")
        with Gopen(data_location) as item:
            item.open("m")
            item[name_data] = value

    def create_data_info(self, locatdir, name_data, type, durability, dgt="none", defense="none"):
        location = os.path.join(locatdir, type, name_data+".gdta")
        with Gopen(location) as dta:
            dta.open("c+")
            dta["name"] = name_data
            dta["type"] = type
            dta["durability"] = durability
            dta["DGT"] = dgt
            dta["Defense"] = defense

    def use_info_item(self, locatdir, type, name, info):
        location = os.path.join(locatdir, type, name+".gdta")
        with Gopen(location) as item:
            item.open("r")
            return item[info]

    def use_full_info_item(self, locatdir, type, name):
        location = os.path.join(locatdir, type, name+".gdta")
        full_info = {}
        with Gopen(location) as item:
            item.open("r")
            for key, value in item.data.items():
                # Exclure certaines valeurs précises du dictionnaire
                if value != "none":
                    full_info[key] = value
        return full_info

    def __enter__(self):
        return self
    
    def __getitem__(self, key):
        return self.data.get(key)
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass


class Sound:
    def __init__(self, music_path):
        self.music_path = music_path

    def play_music(self, loop=True):
        # Vérifier si le chemin spécifié est un fichier ou un dossier
        if os.path.isdir(self.music_path):
            # Si c'est un dossier, obtenir une liste des fichiers audio
            files = [f for f in os.listdir(self.music_path) if os.path.isfile(os.path.join(self.music_path, f))]
            # Sélectionner un fichier audio aléatoire dans le dossier
            music_file = os.path.join(self.music_path, random.choice(files))
        else:
            music_file = self.music_path

        # Sous Windows
        if os.name == 'nt':
            import winsound
            if loop:
                winsound.PlaySound(music_file, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            else:
                winsound.PlaySound(music_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
        # Sous Linux
        elif os.name == 'posix':
            if loop:
                os.system(f"mpg123 -q -loop 0 {music_file} &")
            else:
                os.system(f"mpg123 -q {music_file} &")

    def stop_music(self):
        # Sous Windows
        if os.name == 'nt':
            import winsound
            winsound.PlaySound(None, winsound.SND_FILENAME)
        # Sous Linux
        elif os.name == 'posix':
            os.system("killall -9 mpg123")

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass