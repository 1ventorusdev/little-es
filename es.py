try:
    # import
    from system.plugins.python import gamedata #, psutil
    import os
    import sys
    import socket
    import hashlib
    import datetime
    import shutil
    import getpass
    import platform

    # give path of little es
    os_location = os.getcwd()

    # temp var, to modificate
    user_data = None
    username = None

    os_type = "under os"
    osmod = "server"
    isIndev = False
    discpath = "/mnt"

    with open(os.path.join(os_location, "system", "path", "discpath.config"), "r") as path:
        discpath = path.read()

    textvar = {
        "$usr" : "",
        "$date" : datetime.date.today().strftime("%d %m %Y"),
        "$lang" : "",
        "$accountType" : "",
        "$debugmode": "",
        "$devmode": "",
        "$autoAuth" : "",
        "$e": "",
        "$path": "",
        "$firstname": "",
        "$command": "",
        "$ipv4": socket.gethostbyname(socket.gethostname()),
        "$vername": "",
        "$ver": ""

    }

    systemText = {}

    with open(os.path.join(os_location, "system", "systemtype.typ"), 'r') as file:
            lines = file.readlines()
    for i in range(1, len(lines) - 1):
            ligne_actuelle = lines[i].strip()
            ligne_suivante = lines[i + 1].strip()
            ligne_precedente = lines[i - 1].strip()
            
            # Vérifier si la ligne actuelle est entourée de lines composées uniquement de tirets
            if all(char == '#' for char in ligne_precedente) and all(char == '#' for char in ligne_suivante):
                os_type = ligne_actuelle
            elif all(char == '-' for char in ligne_precedente) and all(char == '-' for char in ligne_suivante):
                osmod = ligne_actuelle

    with open(os.path.join(os_location, "system", "versionname.rst"), 'r') as file:
            lines = file.readlines()
    for i in range(1, len(lines) - 1):
            ligne_actuelle = lines[i].strip()
            ligne_suivante = lines[i + 1].strip()
            ligne_precedente = lines[i - 1].strip()
            
            # Vérifier si la ligne actuelle est entourée de lines composées uniquement de tirets
            if all(char == '=' for char in ligne_precedente) and all(char == '=' for char in ligne_suivante):
                versionname = textvar["$vername"] = ligne_actuelle

    # define variable associate with the os of pc
    system = platform.system()
    if system == "Windows":
        clear = "cls"
        shutdown = "shutdown -p"
        disc = ["a:", "b:", "c:", "d:", "e:", "f:", "g:", "h:", "i:", "j:", "k:", "l:", "m:", "n:", "o:", "p:", "q:", "r:", "s:", "t:", "u:", "v:", "w:", "x:", "y:", "z:"]
        drive, _ = os.path.splitdrive(os_location)
        pythonexc = "python"
    elif system == "Linux":
        clear = "clear"
        shutdown = "shutdown now"
        disc = []
        drive = ""
        for file in os.listdir(discpath):
            d = os.path.join(discpath, file)
            if os.path.isdir(d):
                disc.append(file)
        os_location_for_drive = os_location.replace(f"{discpath}/", "")
        for file in disc:
            if os_location_for_drive.startswith(file):
                drive = f"{discpath}/{file}"
                break
        pythonexc = "python3"
    systemdisc = ["sys:", "system:", "home:", "debug:", "data:", "boot:", "tmp:", "media:"]
    systemdisc2 = ["/system:", "/home:", "/debug:", "/data:", "/boot:", "/tmp:", "/media:"]
    disc += systemdisc
        

    if os.path.exists("devmode.devmode"):
        isIndev = True

    # all database and var of system
    class systemData:
        # database, contain all user data
        database = {}
        for name in os.listdir(os.path.join(os_location, "data")):
            userdir = os.path.join(os_location, "data", name)
            userdata = {}
            with gamedata.Gopen(os.path.join(userdir, "userdata.config")) as dta:
                dta.open()
                userdata["password"] = dta["password"]
                userdata["commonName"] = dta["commonName"]
                userdata["firstname"] = dta["firstname"]
                userdata["familyname"] = dta["familyname"]
                userdata["birthday"] = dta["birthday"]
            
            with gamedata.Gopen(os.path.join(userdir, "system.config")) as dta:
                dta.open()
                userdata["lang"] = dta["lang"]
                userdata["accountType"] = dta["accountType"]
                userdata["devmode"] = dta["devmode"]
                userdata["autoAuth"] = dta["autoAuth"]
                userdata["debugmode"] = dta["debugmode"]
            
            textvar["$usr"] = name
            database[name] = userdata

        # variable of system (add IP and MAC)
        data = {
        "$d": str(datetime.date.today()),
        "$t": str(datetime.datetime.now().time()),
        "$p": os.getcwd(),
        "$username": os.getlogin(),
        "$hostname": socket.gethostname(),
        "$v": platform.system() + " " + platform.version()}
        dta = ["$d", "$t", "$p", "$username", "$hostname", "$v"]
        tmp = {}

        shutdownCommand = ["shutdown", "stop"]
        with open(os.path.join(os_location, "system", "version.rst"), 'r') as file:
            lines = file.readlines()

        versionok = False
        notes_en_cours = False
        version_note = []
        version = ""

        for i in range(1, len(lines) - 1):
            ligne_actuelle = lines[i].strip()
            ligne_suivante = lines[i + 1].strip()
            ligne_precedente = lines[i - 1].strip()

            # Détection du début d'une section de notes de version
            if (all(char == '-' for char in ligne_precedente) and not ligne_actuelle.startswith('-') and all(char == '-' for char in ligne_suivante) and not versionok):
                version = ligne_actuelle  # Enregistre le nom de la version
                textvar["$ver"] = version
                version_note = []
                versionok = True
                notes_en_cours = True  # On commence à enregistrer les notes de cette version
                print("version")
            elif notes_en_cours:
                print("l actuel: ", ligne_actuelle)
                print("l precedente: ", ligne_precedente)
                print("verification: ", (ligne_actuelle == '-' * len(ligne_actuelle) and (ligne_precedente != version and lines[i - 2].strip() != version)))
                # Si on trouve une ligne de tirets et que la ligne précédente n'est pas le nom de version, on arrête l'enregistrement
                if ligne_actuelle == '-' * len(ligne_actuelle) and (ligne_precedente != version and lines[i - 2].strip() != version):
                    notes_en_cours = False
                    continue  # On passe à la prochaine itération sans ajouter cette ligne

                # Ignorer les lignes qui commencent par 'version note:' ou '============='
                if not ligne_actuelle.startswith('version note:') and not ligne_actuelle.startswith("=============") and not ligne_actuelle.startswith(str('-' * len(ligne_actuelle))):
                    # Ajoute la ligne brute sans strip() pour conserver les espaces, mais on retire les lignes vides inutiles   
                    version_note.append(lines[i])  # Ajout de la ligne brute pour conserver le format original

        # Réunir toutes les notes de version dans une chaîne unique, en les séparant par des sauts de ligne
        version_note = "".join(version_note)


    class FileType:
        def __init__(self):
            self.filetype = {
                "python file": [".py"],
                "c file": [".c", ".cpp", ".c#", ".h"],  # Ajout de .cpp et .h
                "JS file": [".js"],
                "HTML file": [".html", ".htm"],
                "CSS file": [".css"],
                "temp file": [".tmp", ".temp"],
                "config file": [".conf", ".config"],
                "log file": [".log"],
                "version file": [".ver"],
                "SQL file":[".sql"],
                "text file": ["txt"],
                "game data file": [".gdta"],
                "vodka file": [".vod"]
            }

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
                
    ft = FileType()


    # input apearence
    def entry():
        cd = os.getcwd()
        if cd.startswith(os_location):
            cd = cd.replace(os_location, "sys:/")
            cd = cd.replace("\\", "/")
            cd = cd.replace("//", "/")
            if cd.startswith("sys:/home"):
                cd = cd.replace("sys:/home", "sys:/home:/")
            if cd.startswith("sys:/system"):
                cd = cd.replace("sys:/system", "sys:/system:/")
            if cd.startswith("sys:/media"):
                cd = cd.replace("sys:/media", "sys:/media:/")
            if cd.startswith("sys:/data"):
                cd = cd.replace("sys:/data", "sys:/data:/")
            if cd.startswith("sys:/boot"):
                cd = cd.replace("sys:/boot", "sys:/boot:/")
            if cd.startswith("sys:/debug"):
                cd = cd.replace("sys:/debug/", "sys:/debug:/")
            if cd.startswith("sys:/tmp"):
                cd = cd.replace("sys:/tmp", "sys:/tmp:/")
        else:
            cd = os.getcwd()
        cd = cd.replace("\\", "/")
        cd = cd.replace("//", "/")
        entry = (
            f"\033[1m\033[36m┌─[\033[34mLittle es {systemData.version}\033[36m]─[\033[31m{cd}\033[36m]─(\033[32m~\033[36m)\n"
            f"\033[1m\033[36m└───(\033[32m{username}\033[34m\033[31m@\033[31m{socket.gethostname()}\033[36m)\033[33m$\033[36m>>>\033[0m "
        )
        return entry

    # security system
    class Security:
        # verify if username in database
        def verify_username(user):
            global user_data
            global username
            if user in systemData.database:
                user_data = systemData.database[user]
                username = user
                return "True"
            else: 
                return "\033[31mUser not found !\n\033[0m"
            
        #verify if password is correct 
        def verify_password(password):
                password = hashlib.sha256(password.encode()).hexdigest()
                if user_data["password"] == password:
                    return f" "
                else:
                    return "\033[31mPassword is incorrect !\n\033[0m"

    # function for boot system          
    class BootSystem:
        # for log before real boot
        def login():
            global username

            if os.path.exists(os.path.join(os_location, "tmp", "firstuser.temp")):
                with open(os.path.join(os_location, "tmp", "newusr.usr"), "w+"):
                    pass
                return

            if os.path.exists(os.path.join(os_location, "tmp", "user-log.temp")):
                with open(os.path.join(os_location, "tmp", "user-log.temp"), "r") as dta:
                    data = dta.read()

                if data in systemData.database and not os.path.exists(os.path.join(os_location, "tmp", "running.temp")):
                    username = textvar["$user"] = data
                    with gamedata.Gopen(os.path.join(os_location, "data", username, "system.config")) as dta:
                        dta.open("r")
                        isAutoAuth = dta["autoAuth"]

                    if isAutoAuth == "on":
                        return
                
            while True:
                print("enter username for log in or \"new\" for create new user")
                user = input("username : ")
                if user == "close" or user == "exit":
                    System.shutdownSystem()
                    quit()
                elif user == "new":
                    with open(os.path.join(os_location, "tmp", "newusr.usr"), "w+"):
                        pass
                    break
                isGoodUsername = Security.verify_username(user)
                if isGoodUsername == "True":
                    password = getpass.getpass("password : ")
                    isGoodPassword = Security.verify_password(password)
                    print(isGoodPassword)
                    if isGoodPassword == f" ":
                        textvar["$user"] = username
                        break

                else:
                    print(isGoodUsername)

        # new user system
        def nus():
            if not os.path.exists(os.path.join(os_location, "tmp", "newusr.usr")):
                return

            lang = "en"
            commonName = "user"
            password = hashlib.sha256("a".encode()).hexdigest()
            firstname = "user"
            familyname = "user"
            birthday = "01/01"
            accountType = "user"
            autoAuth = "off"
            devmode = "off"
            debugmode = "off"

            avaliablelang = os.listdir(os.path.join(os_location, "system", "lang"))
            notavaliableuser = os.listdir(os.path.join(os_location, "data"))

            while True:
                print("NUS 0.5 (New User System) started")
                print("please enter correct value in all input")
                print("during this process it's impossible to exit, please go to end of NUS")
                print("select language in this list")
                for language in avaliablelang:
                    print(f" - {language}")
            
                selectedlang = input(">>> ")

                if selectedlang in avaliablelang:
                    lang = selectedlang
                    break
                else:
                    print("please retry other choice")

            with open(os.path.join(os_location, "system", "lang", lang, "nusadminrequest.lang"), "r") as txt:
                adminrequesttext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "nusdevmoderequest.lang"), "r") as txt:
                devmoderequesttext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "nusdebugmoderequest.lang"), "r") as txt:
                debugmoderequesttext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "nusautoAuthrequest.lang"), "r") as txt:
                autoAuthrequesttext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "nusbirthdayrequest.lang"), "r") as txt:
                birthdayrequesttext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "nusfirstnamerequest.lang"), "r") as txt:
                firstnamerequesttext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "nusfamilynamerequest.lang"), "r") as txt:
                familynamerequesttext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "nuspasswordrequest.lang"), "r") as txt:
                passwordrequesttext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "nususernamerequest.lang"), "r") as txt:
                usernamerequesttext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "nususernameerror.lang"), "r") as txt:
                usernameerrortext = txt.read()
            with open(os.path.join(os_location, "system", "lang", lang, "autoAuthhelp.lang"), "r") as txt:
                autoAuthHelptext = txt.read()

            while True:
                print(usernamerequesttext)
                for username in notavaliableuser:
                    print(f" - {username}")
            
                selecteduser = input(">>> ")

                if not selecteduser in notavaliableuser:
                    commonName = username = selecteduser
                    break
                else:
                    print(usernameerrortext)

            print(passwordrequesttext)
            passwd = input(">>> ")
            password = hashlib.sha256(passwd.encode()).hexdigest()

            print(firstnamerequesttext)
            firstname = input(">>> ")

            print(familynamerequesttext)
            familyname = input(">>> ")

            print(birthdayrequesttext)
            birthday = input(">>> ")


            if not os.path.exists(os.path.join(os_location, "tmp", "firstuser.temp")):
                print(adminrequesttext)
                admininput = input(">>> ")

                if admininput == "on":
                    accountType = "administrator"
                else:
                    accountType = "user"
                
                print(debugmoderequesttext)
                debugmode = input(">>> ")
                if debugmode == "on":
                    pass
                else:
                    debugmode = "off"

                print(devmoderequesttext)
                devmode = input(">>> ")
                if devmode == "on":
                    pass
                else:
                    devmode == "off"
            
            else:
                accountType = "administrator"
                debugmode = "on"
                devmode = "on"

            print(autoAuthrequesttext)
            print("info autoAuth:")
            print(autoAuthHelptext)
            autoAuth = input(">>> ")
            if autoAuth == "on":
                pass
            else:
                autoAuth = "off"

            recaplist = {
                "$lang": lang,
                "$username": commonName,
                "$password": passwd,
                "$firstname": firstname,
                "$familyname": familyname,
                "$birthday": birthday,
                "$devmode": devmode,
                "$debugmode": debugmode,
                "$accountType": accountType,
                "$autoAuth": autoAuth
                }

            with open(os.path.join(os_location, "system", "lang", lang, "nusrecap.lang"), "r") as txt:
                recaptext = txt.read()

            if "$" in recaptext:
                for key in recaplist:
                    recaptext =  recaptext.replace(key, recaplist[key])

            print("\n")
            print(recaptext)
            
            os.mkdir(os.path.join(os_location, "data", commonName))
            os.mkdir(os.path.join(os_location, "home", commonName))
            os.mkdir(os.path.join(os_location, "home", commonName, "document"))
            os.mkdir(os.path.join(os_location, "home", commonName, "download"))
            os.mkdir(os.path.join(os_location, "home", commonName, "appdata"))
            

            with gamedata.Gopen(os.path.join(os_location, "data", commonName, "system.config")) as dta:
                dta.open("c+")
                dta["lang"] = lang
                dta["accountType"] = accountType
                dta["devmode"] = devmode
                dta["autoAuth"] = autoAuth
                dta["debugmode"] = debugmode

            with gamedata.Gopen(os.path.join(os_location, "data", commonName, "userdata.config")) as dta:
                dta.open("c+")
                dta["password"] = password
                dta["CommonName"] = commonName
                dta["firstname"] = firstname
                dta["familyname"] = familyname
                dta["birthday"] = birthday

            if os.path.exists(os.path.join(os_location, "tmp", "firstuser.temp")):
                os.remove(os.path.join(os_location, "tmp", "firstuser.temp"))
            os.remove(os.path.join(os_location, "tmp", "newusr.usr"))

            with open(os.path.join(os_location, "system", "lang", lang, "nusrestart.lang"), "r") as txt:
                restartText = txt.read()
                restartText = restartText.replace('\\033', '\033')
                restartText = restartText.replace('\\x1b', '\x1b')
            if "$" in restartText:
                for key in textvar:
                    if key in restartText:
                        restartText = restartText.replace(key, textvar[key])


            while True:
                print(restartText)
                restart = input(">>>")

                if restart == "restart":
                    os.execv(sys.executable, [pythonexc] + sys.argv)
                elif restart == "close" or restart == "exit":
                    System.shutdownSystem()
                    quit()
                else: 
                    with open(os.path.join(os_location, "system", "lang", lang, "unckowncommand.lang"), "r") as txt:
                        unckowncommand = txt.read()
                        unckowncommand = unckowncommand.replace('\\033', '\033')
                        unckowncommand = unckowncommand.replace('\\x1b', '\x1b')
                    if "$" in unckowncommand:
                        for key in textvar:
                            if key in unckowncommand:
                                if key == "$command":
                                    unckowncommand = unckowncommand.replace(key, restart)
                                else:
                                    unckowncommand = unckowncommand.replace(key, textvar[key])
                    print(unckowncommand)

        def systemfileverification():
            folders = ["home", "system", "data", "tmp", "debug", "boot", "media"]

            for folder in folders:
                folderpath = os.path.join(os_location, folder)

                if not os.path.exists(folderpath):
                    if folder in ["system", "boot"]:
                        print("system folder lost, please reinstall little es and retry")
                        quit()
                    os.mkdir(folderpath)

        # system on first launch on pc
        def systemConfiguration():
            pass

        #load user data
        def loadUserData(user):
            textvar["$usr"] = user
            textvar["$lang"] = systemData.database[user]["lang"]
            textvar["$firstname"] = systemData.database[user]["firstname"]
            textvar["$accountType"] = systemData.database[user]["accountType"]
        
        def viewsystemconf():
            """
            server_output = ""
            user_output = ""
            def get_cpu_info():
                cpu_cores = psutil.cpu_count(logical=False)  # Nombre de cœurs physiques
                cpu_model = os.popen("lscpu | grep 'Model name:' | awk -F: '{print $2}'").read().strip()
                return cpu_cores, cpu_model

            def get_memory_info():
                memory = psutil.virtual_memory()
                total_ram = memory.total / (1024 ** 3)  # Convert to GB
                available_ram = memory.available / (1024 ** 3)  # Convert to GBreturn total_ram, available_ram
            def get_network_interface():
                gateways = psutil.net_if_stats()
                if_addrs = psutil.net_if_addrs()

                interface = None
                for ifname, stats in gateways.items():
                    if stats.isup and ('eth'in ifname or'Ethernet'in ifname):
                        interface = ifname
                        break
                    if interface is None:
                        for ifname, stats in gateways.items():
                            if stats.isup and ('wlan'in ifname or'Wi-Fi'in ifname):
                                interface = ifname
                                break
                            return interface, if_addrs.get(interface, [])

            def get_network_info(interface):
                ipv4 = ipv6 = "N/A"
                for addr in interface:
                    if addr.family == socket.AF_INET:
                        ipv4 = addr.address
                    elif addr.family == socket.AF_INET6:
                        ipv6 = addr.address
                return ipv4, ipv6


            def get_network_speed():
                net_io = psutil.net_io_counters()
                sent = net_io.bytes_sent / (1024 ** 2)  # Convert to MB
                recv = net_io.bytes_recv / (1024 ** 2)  # Convert to MBreturn sent, recv

            def format_speed(speed):
                power = 2**10
                n = 0
                power_labels = {0: 'o/s', 1: 'Ko/s', 2: 'Mo/s', 3: 'Go/s', 4: 'To/s', 5: 'Po/s'}
                while speed > power:
                    speed /= power
                    n += 1
                return f"{speed:.2f} {power_labels[n]}"
            def get_users():
                ssh_users = os.popen("who | awk '{print $1}'").read().split()

            cpu_cores, cpu_model = get_cpu_info()
            total_ram, available_ram = get_memory_info()
            ssh_users, _ = get_users()
            interface_name, interface_info = get_network_interface()
            ipv4, ipv6 = get_network_info(interface_info)

            
            ipv4_str = f"  ipv4: {ipv4}"
            ipv6_str = f"  ipv6: {ipv6}"
            # Format the strings for alignment
            cpu_cores_str = f"  cores: {cpu_cores}"
            cpu_model_str = f"  model: {cpu_model}"
            ram_total_str = f"  total: {total_ram:.2f}Go"
            ram_available_str = f"  available: {available_ram:.2f}Go"
            send_str = f"send: {format_speed(sent)}"
            receive_str = f"recieve: {format_speed(recv)}"
            
            ssh_users_str = ' '.join(ssh_users)

            server_output += ("+---------------------------------------------+---------------------------------------+\n")
            server_output += ("|#hardware                                    |#network                               |\n")
            server_output += ("+--------------------+------------------------+---------------------------------------+\n")
            server_output += (f"|CPU:                |RAM:                    |{(interface_name + ":"):<39}|\n")
            server_output += (f"|{cpu_cores_str:<20}|{ram_total_str:<24}|{ipv4_str:<39}|\n")
            server_output += (f"|{cpu_model_str:<20}|{ram_available_str:<24}|{ipv6_str:<39}|\n")
            server_output += ("+--------------------+------------------------+---------------------------------------+\n")
            server_output += (f"|ssh user list       |{ssh_users_str:<64}|\n")
            server_output += ("+--------------------+----------------------------------------------------------------+\n")
            """

            with gamedata.Gopen(os.path.join(os_location, "boot", "langfile.config")) as dta:
                dta.open("r")
                listlanfile = dta.createdicobyfile()

            # Lecture des fichiers et traitement du texte
            for textType, file in listlanfile.items():
                with open(os.path.join(os_location, "system", "lang", systemData.database[username]["lang"], file), "r") as txt:
                    text = txt.read()
                    text = text.replace('\\033', '\033')
                    text = text.replace('\\x1b', '\x1b')
                    systemText[textType] = text

            # Remplacement des variables dans le texte
            for key1, text in systemText.items():
                if "$" in text:
                    for key2 in textvar:
                        if key2 in text:
                            text = text.replace(key2, textvar[key2])
                            systemText[key1] = text

            # Affichage du texte avec les couleurs (si supporté par le terminal)
            if osmod == "server":
                print(systemText["welcome"])

            with open(os.path.join(os_location, "tmp", "running.temp"), "w+"):
                pass

            if systemData.database[username]["autoAuth"] == "on":
                with open(os.path.join(os_location, "tmp", "user-log.temp"), "w+") as dta:
                    dta.write(username)


    # command and function of system
    class System:
        # shutdown system
        def shutdownSystem():
            if not systemData.database[username]["autoAuth"] == "on":
                if os.path.exists(os.path.join(os_location, "tmp", "user-log.temp")):
                    os.remove(os.path.join(os_location, "tmp", "user-log.temp"))
            
            if os.path.exists(os.path.join(os_location, "tmp", "running.temp")):
                os.remove(os.path.join(os_location, "tmp", "running.temp"))

    class Command:
        def dirs(cd):
            if cd:
                files = os.listdir(cd)

            else:
                files = os.listdir(os.getcwd())
            print("{:<60} {:<7}".format("filename", "type"))
            print("-"*68)
            for file in files:
                if cd:
                    path = os.path.join(cd, file)
                if os.path.isdir(path):
                    typefile = "<dir>"
                    filename = f"/{file}"
                elif file in disc:
                    typefile = "[drive]"
                    filename = f"/{file}"
                elif os.path.isfile(path):
                    typefile = ft.whatfiletype(file)
                    filename = f"./{file}"
                else:
                    typefile = "unckown"
                    filename = f"{file}"
                print(" {:<60} {:<7}".format(filename, typefile))

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
                if file in disc:
                    typefile = "[drive]"
                    filename = f"\033[32m{file}\033[0m"
                elif os.path.isdir(path):
                    typefile = "<directory>"
                    filename = f"\033[34m{file}\033[0m"
                elif os.path.isfile(path):
                    typefile = ft.whatfiletype(file)
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
            print("\n".join(lines))


    BootSystem.systemfileverification()
    BootSystem.login()
    if not os.path.exists(os.path.join(os_location, "tmp", "running.temp")):
        with open(os.path.join(os_location, "tmp", "running.temp"), "w+"):
            pass
    BootSystem.nus()
    BootSystem.loadUserData(username)
    BootSystem.viewsystemconf()

    while True:
        command = input(entry())

        # save dir before command result
        tmpdir = os.getcwd()

        # replace key by her value in the command
        if "$" in command:
            if command.startswith("?") or "=" in command:
                pass
            else:
                for key in systemData.tmp:
                    if key in command:
                        command = command.replace(key, systemData.tmp[key])

                for key in systemData.data:
                    if key in command:
                        command = command.replace(key, systemData.data[key])

        if (command.lower() == "close" or command.lower() == "exit") and os_type == "under os":
            System.shutdownSystem()
            quit()
        elif (command.lower() == "restart" or command.lower() == "reboot") and os_type == "under os":
            os.chdir(os_location)
            print(systemText["restart"])
            os.execv(sys.executable, [pythonexc] + sys.argv)

        elif command.lower() in systemData.shutdownCommand:
            print(systemText["shutdown"])
            System.shutdownSystem()
            os.system(shutdown)

        elif command == "unlog":
            print(systemText["unlog"])
            BootSystem.login()
            BootSystem.nus()
            BootSystem.viewsystemconf()

        elif command.lower() == "clear" or command.lower() == "cls":
            os.system(clear)

        elif command == "help":
            print(systemText["help"])

        # print data system, var created by user and text
        elif command.lower().startswith("$"):  
            value, data_name = command.split("=")
            value = value.strip()  # Supprimer les espaces autour de value
            data_name = data_name.strip()
            data_name = "$" + data_name
            data_name = data_name.replace(" ", "")

            if value.lower() in systemData.dta:
                if data_name in systemData.tmp:
                    del systemData.tmp[data_name]
                systemData.tmp[data_name] = systemData.data[value]
                print(f"Donnée '{data_name}' enregistrée avec la valeur '{systemData.data[value]}'.")
            else:
                print("Donnée $ inconnue")
        elif command.startswith("!"):
            variable = command.replace("!", "")
            value, data_name = variable.split("=")
            data_name = "$" + data_name
            data_name = data_name.replace(" ", "")
            value = value.strip()  # Supprimer les espaces autour de value
            data_name = data_name.strip()  # Supprimer les espaces autour de data_name
            if data_name in systemData.tmp:
                del systemData.tmp[data_name]
            systemData.tmp[data_name] = value
            print(f"Donnée '{data_name}' enregistrée avec la valeur '{value}'.")
        elif command.startswith("?"):
            if "? " in command:
                variable = command.replace("? ", "")
            else:
                variable = command.replace("?", "")
            if variable.lower() in systemData.dta:
                print(systemData.data[variable.lower()])
            else:
                if not "$" in variable:
                    variable = "$" + variable
                if variable in systemData.tmp:
                    print(systemData.tmp[variable])
                elif variable.startswith("$!"):
                    variable = variable.replace("$!", "")
                    print(variable)
                else:
                    print("valeur nom sauvegardé")

        # print path
        elif command == "cd":
            dir = os.getcwd()
            if dir.startswith(os_location):
                dir = dir.replace(os_location, "sys:/")
                dir = dir.replace("\\", "/")
                dir = dir.replace("//", "/")
                if dir.startswith("sys:/home/"):
                    dir = dir.replace("sys:/home/", "sys:/home:/")
                if dir.startswith("sys:/system/"):
                    dir = dir.replace("sys:/system/", "sys:/system:/")
                if dir.startswith("sys:/media/"):
                    dir = dir.replace("sys:/media/", "sys:/media:/")
                if dir.startswith("sys:/data/"):
                    dir = dir.replace("sys:/data/", "sys:/data:/")
                if dir.startswith("sys:/boot/"):
                    dir = dir.replace("sys:/boot/", "sys:/boot:/")
                if dir.startswith("sys:/debug/"):
                    dir = dir.replace("sys:/debug/", "sys:/debug:/")
                if dir.startswith("sys:/tmp/"):
                    dir = dir.replace("sys:/tmp/", "sys:/tmp:/")
            else:
                dir = os.getcwd()
            
            dir = dir.replace("\\", "/")
            dir = dir.replace("//", "/")
            print(dir)
        elif command == "disc":
            print("avaliable disc:")
            for file in disc:
                print(f" - {file}")
        elif command.startswith("dir"):
            command = command.split(" ")
            path = os.getcwd()
            if len(command) > 1:
                if command[1:] != " ":
                    path = ' '.join(command[1:])
            Command.dirs(path)

        elif command.startswith("ls") and command != "lsblk":
            command = command.split(" ")
            path = os.getcwd()
            if len(command) > 1:
                if command[1:] != " ":
                    path = ' '.join(command[1:])
            Command.ls(path)

        # change path
        elif command in disc or command in systemdisc2:
            if command == "sys:":
                os.chdir(os_location)
            elif command == "system:" or command == "/system:":
                os.chdir(os.path.join(os_location, "system"))
            elif command == "home:" or command == "/home:":
                os.chdir(os.path.join(os_location, "home"))
            elif command == "data:" or command == "/data:":
                os.chdir(os.path.join(os_location, "data"))
            elif command == "media:" or command == "/media:":
                os.chdir(os.path.join(os_location, "media"))
            elif command == "debug:" or command == "/debug:":
                os.chdir(os.path.join(os_location, "debug"))
            elif command == "boot:" or command == "/boot:":
                os.chdir(os.path.join(os_location, "boot"))
            elif command == "tmp:" or command == "/tmp:":
                os.chdir(os.path.join(os_location, "tmp"))
            else:
                if system == "Linux":
                    command = f"{discpath}/{command}"
                elif system == "Windows":
                    pass
                os.chdir(command)
        elif command == "cd..":
            try:
                parent_directory = os.path.normpath(os.path.join(os.getcwd(), ".."))
                os.chdir(parent_directory)
            except Exception as e:
                print(f"{e}")
        elif command == "cd/":
            try:
                # Obtient la racine du disque
                root_directory = os.path.abspath(os.sep)
                os.chdir(root_directory)
            except Exception as e:
                print(f"{e}")
        elif command.startswith("cd"):
            _, path = command.split(" ", 1)
            path = path.strip()
            try:
                if path.startswith("sys:/"):
                    path = path.replace("sys:", os_location)
                if "/system:" in path:
                    path = path.replace("/system:", "/system")
                if "/home:" in path:
                    path = path.replace("/home:", "/home")
                if "/media:" in path:
                    path = path.replace("/media:", "/media")
                if "/data:" in path:
                    path = path.replace("/data:", "/data")
                if "/boot:" in path:
                    path = path.replace("/boot:", "/boot")
                if "/debug:" in path:
                    path = path.replace("/debug:", "/debug")
                if "/tmp:" in path:
                    path = path.replace("/tmp:", "/tmp")
                

                os.chdir(path)
            except FileNotFoundError:
                with open(os.path.join(os_location, "system", "lang", systemData.database[username]["lang"], "nopath.lang"), "r") as txt:
                    text = txt.read()
                    text = text.replace('\\033', '\033')
                    text = text.replace('\\x1b', '\x1b')
                if "$" in text:
                    for key in textvar:
                        if key in text:
                            text = text.replace(key, path)
                print(text)
            except Exception as e:
                print(f"{e}")

        # app system access

        elif command == "version":
            print(f"version: {systemData.version} \nnote: \n{systemData.version_note}")

        else:
            os.system(command)


except Exception as e:
    try: 
        if os.path.exists(os.path.join(os_location, "system", "lang", systemData.database[username]["lang"], "error.lang")):
            errorpath = os.path.join(os_location, "system", "lang", systemData.database[username]["lang"], "error.lang")
    except:
        errorpath = os.path.join(os_location, "system", "lang", "en", "error.lang")

    with open(errorpath, "r") as txt:
        text = txt.read()
        text = text.replace('\\033', '\033')
        text = text.replace('\\x1b', '\x1b')
    if "$" in text:
        for key in textvar:
            if key in text:
                text = text.replace(key, str(e))
    # if error occured while system running
    print("\033[1m\033[31m", e, "\033[0m\n")
    System.shutdownSystem()
