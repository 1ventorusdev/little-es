import os
import datetime
import socket
import platform
import shutil
import ctypes
import getpass
import subprocess

class DataBase:
    def __init__(self):
        self.version = "beta 0.10.5"
        self.output = ""
        self.CommandHelp = {
            "shutdown": """command : shutdown
shutdown system
usage:
    shutdown -n         : for shutdown system now
    shutdown -t [time]  : for shutdown system with time delay, time in second
    """,
            "cd": """command : cd
if without argument print path, else go to argument path
usage:
    cd        : print path
    cd..      : go to parent path  
    cd/       : go to tree of drive
    dc [path] : go to path relative or complet
    """,
            "dir": """command : dir
command to print file and folder in path  with style
usage:
    dir [path]: print file and directory in path selected or this path if without argument
    """,
            "ls": """command : ls
command to print file and folder in path
usage:
    ls [path]: print file and directory in path selected or this path if without argument
    """,
            "quit": """command : quit
command to exit system
usage:
    shutdown
    """,
            "help": """command : help
print cli help command
usage:
    shutdown
    """,
            "$": """command : $
save preloaded data in var
usage:
    $[d]|[t]|[p]|[v]|[username]|[hostname]|[ip]|[mac]
    
    d         : date
    t         : time
    p         : path
    v         : version of OS
    username  : name of user loged
    hostname  : name of PC
    ip        : IP address
    mac       : MAC address
    """,
            "!": """command : !
save text in variable
usage:
    ![text] = [varname]
    """,
            "?": """command : ?
print data in variable
usage:
    ? [$var]|[!text]
    """,
            "clear": """command : clear
reset screen
usage:      
    clear
    """,
            "cls": """command : cls
reset screen
usage:   
    cls     
    """
        }

        self.filetype = {
            "python file": [".py", ".pyc"],
            "c file": [".c", ".cpp", ".c#", ".h"],  # Ajout de .cpp et .h
            "JS file": [".js"],
            "HTML file": [".html", ".htm"],
            "CSS file": [".css"],
            "temp file": [".tmp", ".temp"],
            "config file": [".conf", ".config", ".cfg"],
            "log file": [".log"],
            "version file": [".ver"],
            "SQL file":[".sql"],
            "text file": ["txt"],
            "game data file": [".gdta"],
            "vodka file": [".vod"],
            "error file": [".err", ".error"],
            "assembly file": [".asm"]
            }
        
    data = {
        "$d": str(datetime.date.today()),
        "$t": str(datetime.datetime.now().time()),
        "$p": os.getcwd(),
        "$username": os.getlogin(),
        "$hostname": socket.gethostname(),
        "$v": platform.system() + " " + platform.version(),
        "$ip": "0.0.0.0", # replace by method for obtain ip
        "$mac": "ffff.ffff.ffff.ffff" # replace by method for obtain mac address
        }

    tmp = {}

    auth = "user"
    execute = True

    AdminCommands = ["cd "]

    help = {
            "shutdown": "shutdown system",
            "cd": "if without argument print path, else go to argument path",
            "dir": "command to print file and folder in path  with style",
            "ls": "command to print file and folder in path",
            "quit": "command to exit system",
            "help": "print cli help command",
            "$": "save preloaded data in var",
            "!": "save text in variable",
            "?": "print data in variable",
            "clear": "reset screen",
            "cls": "reset screen"
        }

    shutdownCommand = ["shutdown", "stop"]

    system = platform.system()
    if system == "Windows":
        clear = "cls"
        shutdown = "shutdown -p"
        disc = ["a:", "b:", "c:", "d:", "e:", "f:", "g:", "h:", "i:", "j:", "k:", "l:", "m:", "n:", "o:", "p:", "q:", "r:", "s:", "t:", "u:", "v:", "w:", "x:", "y:", "z:"]
    elif system == "Linux":
        clear = "clear"
        shutdown = "shutdown -h"
        disc = []
        for file in os.listdir(f"/media/{os.getlogin()}"):
            d = os.path.join(f"/media/{os.getlogin()}", file)
            if os.path.isdir(d):
                disc.append(file)

    def entry(self):
        cd = os.getcwd()
        if platform.system() == "Linux":
            if cd.startswith(f"/home/{os.getlogin()}"):
                cd = cd.replace(f"/home/{os.getlogin()}", "~")
            endcommand = "\033[33m$"
        elif platform.system() == "Windows":
            endcommand = "\033[36m>"
        else:
            endcommand = "\033[33m$\033[36m>>>"
        cd = cd.replace("\\", "/")
        cd = cd.replace("//", "/")
        return (
            f"\033[1m\033[36m┌─[\033[34mCLI {self.version}\033[36m]─[\033[31m{cd}\033[36m]\n"
            f"\033[1m\033[36m└───(\033[32m{os.getlogin()}\033[34m\033[31m@\033[31m{socket.gethostname()}\033[36m){endcommand}\033[0m "
        )

    def cliversion(self):
        return self.version
    
    # set the data to print after
    def setOutput(self, output):
        self.output = output

    def addOutput(self, *output):
        output = ' '.join(map(str, output))
        self.output += output

    # print data saved
    def printOutput(self):
        print(self.output)


    # for return the help of command
    def commandhelp(self, command):
        return self.CommandHelp[command]
    
    def isExecutable(self, filename, ext):
        if ext == ".exe":
            return "app file"

        if platform.system() == "Linux":
            if os.access(filename, os.X_OK):
                return "app file"
        return None

    def whatfiletype(self, filename):
        _, ext = os.path.splitext(filename)
        executable = self.isExecutable(filename, ext)
        if executable:
            return executable

        for filetype, exts in self.filetype.items():
            if ext in exts:
                return filetype
            
        typefile = ext.upper() + " file"
        typefile = typefile.replace(".", "")
        return typefile

    def banner(self, *args, top="_", side="|"):
        combined_texts = [arg for arg in args]
    
        # Determine the maximum length of the banner
        max_length = max(len(line) for line in combined_texts) + 4  # Adding padding
        
        # Create the border
        bordertop = " " + top * (max_length) + "\n"
        borderbottom = side + top * (max_length) + side + "\n"
        
        # Print the banner
        self.addOutput(bordertop)
        self.addOutput(side + "{:^{width}}".format(" ", width=max_length) + side + "\n")
        for line in combined_texts:
            formatted_line = side + "{:^{width}}".format(line, width=max_length) + side + "\n"
            self.addOutput(formatted_line)
        self.addOutput(borderbottom)

database = DataBase()

class Commands:
    class Var:
        def replace(command:str):
            if "$" in command:
                if command.startswith("?") or "=" in command:
                    pass
                else:
                    for key in database.tmp:
                        if key in command:
                            command = command.replace(key, database.tmp[key])

                    for key in database.data:
                        if key in command:
                            command = command.replace(key, database.data[key])
            return command

        def create(command:str, method):
            if method == "$":
                value, data_name = command.split("=")
                value = value.strip()  # Supprimer les espaces autour de value
                data_name = data_name.strip()
                data_name = "$" + data_name
                data_name = data_name.replace(" ", "")

                if value.lower() in database.data:
                    if data_name in database.tmp:
                        del database.tmp[data_name]
                    database.tmp[data_name] = database.data[value]
                    database.addOutput(f"Donnée '{data_name}' enregistrée avec la valeur '{database.data[value]}'.")
                else:
                    database.addOutput("Donnée $ inconnue")

            elif method == "!":
                value, data_name = command.split("=")
                data_name = "$" + data_name
                data_name = data_name.replace(" ", "")
                value = value.strip()  # Supprimer les espaces autour de value
                data_name = data_name.strip()  # Supprimer les espaces autour de data_name
                if data_name in database.tmp:
                    del database.tmp[data_name]
                database.tmp[data_name] = value
                database.addOutput(f"Donnée '{data_name}' enregistrée avec la valeur '{value}'.")

        def print(command:str):
            if "? " in command:
                variable = command.replace("? ", "")
            else:
                variable = command.replace("?", "")
            if variable.lower() in database.data:
                database.addOutput(database.data[variable.lower()])
            else:
                if not "$" in variable:
                    variable = "$" + variable
                if variable in database.tmp:
                    database.addOutput(database.tmp[variable])
                elif variable.startswith("$!"):
                    variable = variable.replace("$!", "")
                    database.addOutput(variable)
                else:
                    database.addOutput("valeur nom sauvegardé")

    class Dirs:
        def cdlast():
            try:
                parent_directory = os.path.normpath(os.path.join(os.getcwd(), ".."))
                os.chdir(parent_directory)
            except Exception as e:
                database.addOutput(f"Erreur lors du changement de répertoire : {e}")
        
        def cdroot():
            try:
                # Obtient la racine du disque
                root_directory = os.path.abspath(os.sep)
                os.chdir(root_directory)
            except Exception as e:
                database.addOutput(f"Erreur lors du changement de répertoire : {e}")

        def cdtopath(path):
            _, path = path.split(" ", 1)
            path = path.strip()
            try:
                if path.startswith("/") and os.path.exists(path.replace("/", "", 1)):
                    path = path.replace("/", "", 1)

                os.chdir(path)
            except FileNotFoundError:
                database.addOutput(f"Le répertoire '{path}' n'existe pas.")
            except Exception as e:
                database.addOutput(f"Erreur lors du changement de répertoire : {e}")

        def cddrive(path):
            if database.system == "Windows":
                os.chdir(path)
            elif database.system == "Linux":
                os.chdir(f"/media/{database.data["$username"]}/{path}")

        def cdUserfile():
            if database.system == "Windows":
                os.chdir(f"c:Users/{database.data["$username"]}")
            elif database.system == "Linux":
                os.chdir(f"/home/{database.data["$username"]}")

        def printcd():
            database.addOutput(os.getcwd())
        
        def printdir(cd):
            files = os.listdir(cd)
            database.addOutput("{:<60} {:<9}\n".format("filename", "type"))
            database.addOutput("-"*75 + "\n")
            for file in files:
                if cd:
                    path = os.path.join(cd, file)
                if file in database.disc:
                    typefile = "[drive]"
                    filename = f"/{file}"
                elif os.path.isdir(path):
                    typefile = "<directory>"
                    filename = f" /{file}"
                elif os.path.isfile(path):
                    typefile = database.whatfiletype(file)
                    filename = f"./{file}"
                else:
                    typefile = "unckown"
                    filename = f"{file}"
                database.addOutput(" {:<60}{:<7}\n".format(filename, typefile))

        def printdrive():
            database.addOutput(f"system count {len(database.disc)} drive connected\n")
            for drive in database.disc:
                database.addOutput(" -", drive, "\n")

        def ls(cd):
            output = ""
            files = os.listdir(cd)
            
            # Récupère la taille de l'écran (nombre de colonnes)
            columns = shutil.get_terminal_size().columns

            # Trouve la longueur maximale des noms de fichiers pour définir la largeur de la colonne
            max_len = max((len(file) + 10) for file in files)
            
            # Ajoute un espace entre les colonnes
            col_width = max_len
            
            # Calcule le nombre de colonnes qui peuvent tenir dans la largeur de l'écran
            num_cols = columns // col_width
            
            # Initialise la variable pour stocker les lignes
            lines = []
            
            # Boucle pour organiser les fichiers en lignes et colonnes
            line = ""
            for i, file in enumerate(files):
                if cd:
                    path = os.path.join(cd, file)
                if file in database.disc:
                    typefile = "[drive]"
                    filename = f"\033[32m{file}\033[0m"
                elif os.path.isdir(path):
                    typefile = "<directory>"
                    filename = f"\033[34m{file}\033[0m"
                elif os.path.isfile(path):
                    typefile = database.whatfiletype(file)
                    filename = f"\033[36m{file}\033[0m"
                else:
                    typefile = "unknown"
                    filename = f"\033[36m{file}\033[0m"
                
                # Ajoute le nom de fichier à la ligne en cours
                line += f"{filename.ljust(col_width)}"
                
                # Si la ligne est complète, ajoute-la à la liste des lignes et réinitialise la ligne
                if (i + 1) % num_cols == 0:
                    lines.append(line)
                    line = ""
            
            # Ajoute la dernière ligne si elle n'est pas vide
            if line:
                lines.append(line)
            
            # Joindre toutes les lignes avec des nouvelles lignes
            output = "\n".join(lines)
            
            # Ajoute la sortie au database
            database.addOutput(output)

    # add other class for catergory of command
    # add command in class
    # add command general (not add in under class)

    def Help():
        database.banner(f"CLI {database.cliversion()} command help", f"system adapted to {database.data["$v"]}")
        database.addOutput("{:<10}{:<60}\n".format("command", "info to this command"))
        database.addOutput("-"*30 + "\n")
        for command in database.help:
            database.addOutput("{:<10}{:<60}\n".format(command, database.help[command]))

    class System:
        def shutdown(command:str):
            command = command.split()
            if len(command) < 2:
                database.addOutput("please enter parameter of shutdown")
                return
            if command[1] == "-n":
                # method for shutdown system now
                os.system("shutdown /s /t 0")
            elif command[1] == "-t":
                timesleep = int(command[2])
                os.system(f"shutdown /s /t {timesleep}")
                # method to shutdown system in end of timesleep second
        
        # add command system


    class Admin:
        # command only admin user
        pass

    class User:
        # command alternative of admin command
        pass

class Security:
    def changeAuth():
        if database.system == "Windows":
            if ctypes.windll.shell32.IsUserAnAdmin():
                database.auth = "admin"
            else:
                database.execute = False

        elif database.system == "Linux":
            password = getpass.getpass("enter your password: ") 
            command = f"echo {password} | sudo -S -v"
            proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Send the password
            output, error = proc.communicate(input=f"{password}\n".encode())

            if proc.returncode == 0:
                database.auth = "admin"
            else:
                database.execute = False

def main():
    while True:
        command = input(database.entry())
        database.setOutput("")
        database.execute = True

        command = Commands.Var.replace(command)

        if command.startswith("sudo "):
            Security.changeAuth()
            command = command.replace("sudo ", "", 1)


        if command == "close":
            quit()

        if database.execute == False or (not command.startswith("sudo ") and database.auth != "admin" and command.startswith(adminCommand) for adminCommand in database.AdminCommands):
            database.addOutput(f"security system:{command} => premission denied")

        elif command.endswith("/?"):
            for com in database.CommandHelp:
                if command.startswith(com):
                    database.addOutput(database.commandhelp(command.replace(" /?", "")))
                    in_system = True
                    break
            if not in_system:
                database.addOutput(f"command {command} isn't in database, please verify with command help")

        elif command == "help":
            Commands.Help()
        
        elif command.startswith("$"):
            Commands.Var.create(command, "$")
        elif command.startswith("!"):
            command = command.replace("!", "", 1)
            Commands.Var.create(command, "!")
        elif command.startswith("?"):
            Commands.Var.print(command)
        
        elif command.startswith("cd"):
            if command == "cd":
                Commands.Dirs.printcd()
            elif command == "cd..":
                Commands.Dirs.cdlast()
            elif command == "cd/":
                Commands.Dirs.cdroot()
            else:
                if command.endswith(" ~") or command.endswith(" " + database.data["$username"]):
                    Commands.Dirs.cdUserfile()
                else:
                    Commands.Dirs.cdtopath(command)

        elif command in database.disc:
            Commands.Dirs.cddrive(command)

        elif command.startswith("dir"):
            command = command.split(" ")
            path = os.getcwd()
            if len(command) > 1:
                path = ' '.join(command[1:])
            Commands.Dirs.printdir(path)

        elif command.startswith("ls"):
            command = command.split(" ")
            path = os.getcwd()
            if len(command) > 1:
                path = ' '.join(command[1:])
            Commands.Dirs.ls(path)
        elif command == "disc" or command == "drive":
            Commands.Dirs.printdrive()

        elif command == "clear" or command == "cls":
            os.system(database.clear)

        # add traitment of command

        else:
            database.addOutput(f"command {command} isn't in database, please verify with command help")

        database.printOutput()
try:
    main()
except Exception as e:
    database.addOutput(e)
    database.printOutput()