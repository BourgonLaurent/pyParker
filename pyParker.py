#!/usr/bin/python3
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import urllib.request, time, os, csv, sys, configparser

def makeDir(directory):
    if os.path.isdir(directory):
        pass
    else:
        os.mkdir(directory)

def makeFile(file):
    if os.path.isfile(file):
        pass
    else:
        open(file, 'a').close()

def iniconfig():
    if os.path.isfile("config.ini"):
        pass
    else:
        print("[*] This is the first time that you run this program, you will go through the configurator first.\n\n")
        datapath = input("Where do you want the files stored?\n\tBy leaving this empty, you will be using the default location\n\t[Default is ./data/, AKA it will create a folder \"data\" in your current directory]: ")
        if datapath == "":
            datapath = "./data/"

        print("\nHere's a list of parks, select those that you want to log [Y]es/[N]o:")
        parks = {}
        # Ask for each park and store the answer in a dictionnary
        parks["magicKingdom"] = input("Magic Kingdom [Y]es/[N]o: ")
        parks["epcot"] = input("Epcot [Y]es/[N]o: ")
        parks["hollywoodStudios"] = input("Hollywood Studios [Y]es/[N]o: ")
        parks["animalKingdom"] = input("Animal Kingdom [Y]es/[N]o: ")
        configParks = {}
        # Convert the input of the user in a boolean for the config file
        for park in parks:
            if parks[park] in ("Y", "y", "Yes", "yes", "1"):
                configParks[park] = "true"
            else:
                configParks[park] = "false"

        timeout = input("\nYou can specify a time in seconds to pause the script, useful if your task scheduler only has intervals of 10 minutes\n\tBy leaving this empty, you will be using the default value\n\t[Default is 0s, AKA instant]: ")
        if timeout == "":
            timeout = 0
        else:
            timeout = int(timeout)
        
        config = configparser.ConfigParser()
        config["Paths"] = {"datapath": datapath}
        config["Parks"] = {"magicKingdom": configParks["magicKingdom"],
                           "epcot": configParks["epcot"],
                           "hollywoodStudios": configParks["hollywoodStudios"],
                           "animalKingdom": configParks["animalKingdom"]}
        config["Options"] = {"timeout": timeout}
        with open("config.ini", "w") as configfile:
            config.write(configfile)

def verifConfig():
    global datapath, magickingdom, epcot, hollywoodstudios, animalkingdom
    makeDir(datapath)
    if magickingdom:
        makeDir(datapath + "/Magic Kingdom/")
        makeFile(datapath + "/Magic Kingdom/[INFORMATION].csv")
    if epcot:
        makeDir(datapath + "/Epcot/")
        makeFile(datapath + "/Epcot/[INFORMATION].csv")
    if hollywoodstudios:
        makeDir(datapath + "/Hollywood Studios/")
        makeFile(datapath + "/Hollywood Studios/[INFORMATION].csv")
    if animalkingdom:
        makeDir(datapath + "/Animal Kingdom/")
        makeFile(datapath + "/Animal Kingdom/[INFORMATION].csv")

def readConfig():
    config = configparser.ConfigParser()
    config.read("config.ini")
    # Check if the config file is correct
    if "Paths" in config:
        pass
    else:
        sys.exit("[!] ERROR 0-01: Your config.ini file is incorrect, please delete it and try again.")
    if "Parks" in config:
        pass
    else:
        sys.exit("[!] ERROR 0-01: Your config.ini file is incorrect, please delete it and try again.")
    if "Options" in config:
        pass
    else:
        sys.exit("[!] ERROR 0-01: Your config.ini file is incorrect, please delete it and try again.")
    
    datapath = config["Paths"]["datapath"]
    magickingdom = config["Parks"].getboolean("magickingdom")
    epcot = config["Parks"].getboolean("epcot")
    hollywoodstudios = config["Parks"].getboolean("hollywoodstudios")
    animalkingdom = config["Parks"].getboolean("animalkingdom")
    timeout = int(config["Options"]["timeout"])

    return datapath, magickingdom, epcot, hollywoodstudios, animalkingdom, timeout
def retrieveHTML(selected_park):
    global mk, ep, hs, ak

    if selected_park not in (mk, ep, hs, ak):  # Check if park exists
        print("Invalid park selected")
        sys.exit()
    # else: #DEBUG
        # print(selected_park)
    # Specify User-Agent to prevent Error 403: Forbiden
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
    # Create url by using the park specified
    selected_url = "https://www.laughingplace.com/w/p/{}-current-wait-times/".format(selected_park)
    req = urllib.request.Request(selected_url, headers={"User-Agent": user_agent})  # setting headers to go incognito
    uClient = uReq(req)  # opening up connection
    page_html = uClient.read()  # grabbing page
    uClient.close()  # closing connection
    return page_html

def webScrape(page_html):
    page_soup = soup(page_html, "lxml")  # html parsing
    title = page_soup.h1.text.strip()  # Title of the page
    park = title.replace(" Current Wait Times", "")  # Name of the park
    if "Disney's " in park:
        park = park.replace("Disney's ", "")
    r_datetime = page_soup.findAll("div", {"class": "header"})[0].text.strip()  # Find the locations

    date, time = r_datetime.split("\n")
    date, ophour = date.split(": ")
    date = date.replace("Operating Hours For ", "")
    day, date = date.split(", ")
    time = time.replace("Last Check at ", "")
    time = time.replace(":", ".")

    table = page_soup.table
    containers = table.findAll("tr")
    containers = list(dict.fromkeys(containers))

    location = {}
    location["park"] = park
    location["ophour"] = ophour
    location["date"] = date
    location["day"] = day
    location["time"] = time

    attlist = {}
    for container in containers:
        c_entry = container.text.strip()
        #Cleaning entries
        if "\n" in c_entry:
            c_entry = c_entry.replace("\n", ",", 1)
            c_entry = c_entry.replace('\n','')
        else:
            continue
        if " minutes" in c_entry:
            c_entry = c_entry.replace(" minutes", "")
        if "“" in c_entry:
            c_entry = c_entry.replace("“", "")
        if "”" in c_entry:
            c_entry = c_entry.replace("”", "")
        if "’" in c_entry:
            c_entry = c_entry.replace("’", "")
        if "~" in c_entry:
            c_entry = c_entry.replace("~", "")
        if "Monsters, Inc. Laugh Floor" in c_entry:
            c_entry = c_entry.replace("Monsters, Inc. Laugh Floor", "Monsters Inc. Laugh Floor")
        if "*" in c_entry:
            c_entry = c_entry.replace("*", "")
        if "–" in c_entry:
            c_entry = c_entry.replace("–", "")
        if "!" in c_entry:
            c_entry = c_entry.replace("!", "")
        if ":" in c_entry:
            c_entry = c_entry.replace(":", "")
        if "™" in c_entry:
            c_entry = c_entry.replace("™", "")
        if u"\u2018" in c_entry:
            c_entry = c_entry.replace(u"\u2018", "")
        # Split entry to have 2 values
        att, time = c_entry.split(",")
        # Add to dictionnary
        attlist[att] = time
    return attlist, location

def writeCSV(attlist, location):
    global datapath
    filename_info = datapath + "/{}/[INFORMATION].csv".format(location["park"])
    writeinfo = location["date"] + "," + location["day"] + "," + location["ophour"] + "\n"

    #Check if we need to write to [INFORMATION].csv
    inf = open(filename_info, "r")
    infr = inf.read()
    headers = "Date,Day,Opening Hours\n"
    f = open(filename_info, "a")
    if headers not in infr:
        f.write(headers)
    if writeinfo not in infr:
        f.write(writeinfo)
    f.close()
    inf.close()
    for att in attlist:
        filename = datapath + "/{}/{}.csv".format(location["park"], att)
        wait = str(attlist[att])
        headers = "Date,Time,Wait\n"
        writedata = location["date"] + "," + location["time"] + "," + wait + "\n"
        #Write to data file if it doesn't exist
        if os.path.isfile(filename):
            data = open(filename, "r")
            datar = data.read()
            if writedata not in datar:
                h = open(filename, "a")
                h.write(writedata)
                h.close()
        else: #create file if it doesn't exist
            newentry = open(filename, "a")
            newentry.write(headers)
            newentry.write(writedata)
            newentry.close()

def storeWaitTimes(mainpark):
    page_html = retrieveHTML(mainpark) #Scrape Magic Kingdom
    attlist, location = webScrape(page_html) #Retrieve Attractions and Wait
    writeCSV(attlist, location) #Write to a CSV

mk = "magic-kingdom" #Source URL
ep = "Epcot"
hs = "Disneys-Hollywood-Studios"
ak = "Disneys-Animal-Kingdom"

iniconfig()
datapath, magickingdom, epcot, hollywoodstudios, animalkingdom, timeout = readConfig()
verifConfig()
time.sleep(timeout)
if magickingdom:
    storeWaitTimes(mk)
if epcot:
    storeWaitTimes(ep)
if hollywoodstudios:
    storeWaitTimes(hs)
if animalkingdom:
    storeWaitTimes(ak)