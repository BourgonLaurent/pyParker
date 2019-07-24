#!/usr/bin/python3
intro = """
              ______               _                
              | ___ \             | |               
 _ __   _   _ | |_/ /  __ _  _ __ | | __  ___  _ __ 
| '_ \ | | | ||  __/  / _` || '__|| |/ / / _ \| '__|
| |_) || |_| || |    | (_| || |   |   < |  __/| |   
| .__/  \__, |\_|     \__,_||_|   |_|\_\ \___||_|   
| |      __/ |   © Laurent Bourgon for pyParker, parkerGrapher
|_|     |___/    © Scott Caratozzolo for MouseTools module
                 v2.0.2
 
 - All data is taken directly from Disney's Internal API
    by using the MouseTools module.
"""
# Repo: https://github.com/BourgonLaurent/pyParker

from MouseToolsbyScottCaratozzolo.attractions import Attraction
from MouseToolsbyScottCaratozzolo.parks import Park, MK_ID, EPCOT_ID, HS_ID, AK_ID, DLP_ID, CA_ID
from MouseToolsbyScottCaratozzolo.destinations import Destination, WDW_ID, DL_ID
from configparser import ConfigParser
from datetime import datetime
import time, os, csv, sys, json

## List of errors
errors = {
    "E001":"[!] ERROR 0-01: Your pyParker.ini file is incorrect, please delete it and try again."}

path = os.path.realpath(__file__).replace(os.path.basename(__file__), "")

## Utilities
def makeDir(directory):
    if os.path.isdir(directory):
        pass
    else:
        os.mkdir(directory)

def makeFile(fp):
    if os.path.isfile(fp):
        pass
    else:
        open(fp, 'w').close()

## Configurator
def iniConfig():
    global path
    
    if not os.path.isfile(path + "pyParker.ini"):
        print(intro)
        print("[*] This is the first time that you run this program, you will go through the configurator first.\n\n")
        
        datapath = input("- Where do you want the files stored?\n\tBy leaving this empty, you will be using the default location\n\t[Default is ./data/, AKA it will create a folder \"data\" in your current directory]: ")
        if datapath == "":
            datapath = "./data"

        print("\nHere's a list of Resorts, select those that you want to log [Y]es/[N]o/[A]dvanced:")
        
        worlds = {}  # All the parks in that world
        parks = {}  # Selected parks in a world
        configParks = {}  # Final with all the parks

        # Ask for each park and store the answer in a dictionnary
        worlds["waltdisneyworld"] = input("- Walt Disney World, Orlando (Florida) [Y]es/[N]o/[A]dvanced: ")  # Walt Disney World
        if worlds["waltdisneyworld"] in ("Y", "y", "Yes", "yes", "1"):
            configParks["magicKingdom"] = "true"
            configParks["epcot"] = "true"
            configParks["hollywoodStudios"] = "true"
            configParks["animalKingdom"] = "true"
        elif worlds["waltdisneyworld"] in ("A", "a", "Advanced", "advanced"):  # Advanced mode
            print("\nEntering Advanced configuration mode for Walt Disney World, Orlando (Florida)")
            parks["magicKingdom"] = input("\t- Magic Kingdom [Y]es/[N]o: ")
            parks["epcot"] = input("\t- Epcot [Y]es/[N]o: ")
            parks["hollywoodStudios"] = input("\t- Hollywood Studios [Y]es/[N]o: ")
            parks["animalKingdom"] = input("\t- Animal Kingdom [Y]es/[N]o: ")
            for park in parks:
                if parks[park] in ("Y", "y", "Yes", "yes", "1"):
                    configParks[park] = "true"
                else:
                    configParks[park] = "false"
        else:
            configParks["magicKingdom"] = "false"
            configParks["epcot"] = "false"
            configParks["hollywoodStudios"] = "false"
            configParks["animalKingdom"] = "false"

        worlds["disneyland"] = input("- Disneyland, Anaheim (California) [Y]es/[N]o/[A]dvanced: ")  # Disneyland
        if worlds["disneyland"] in ("Y", "y", "Yes", "yes", "1"):
            configParks["disneyland"] = "true"
            configParks["californiaAdventure"] = "true"
        elif worlds["disneyland"] in ("A", "a", "Advanced", "advanced"):  # Advanced mode
            print("\nEntering Advanced configuration mode for Disneyland, Anaheim (California)")
            parks["disneyland"] = input("\t- Disneyland Park [Y]es/[N]o: ")
            parks["californiaAdventure"] = input("\t- California Adventure [Y]es/[N]o: ")
            for park in parks:
                if parks[park] in ("Y", "y", "Yes", "yes", "1"):
                    configParks[park] = "true"
                else:
                    configParks[park] = "false"
        else:
            configParks["disneyland"] = "false"
            configParks["californiaAdventure"] = "false"

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
        
        config = ConfigParser()
        config["Paths"] = {"datapath": datapath}
        config["Parks"] = {"magicKingdom": configParks["magicKingdom"],
                           "epcot": configParks["epcot"],
                           "hollywoodStudios": configParks["hollywoodStudios"],
                           "animalKingdom": configParks["animalKingdom"],
                           "disneyland": configParks["disneyland"],
                           "californiaAdventure": configParks["californiaAdventure"]}
        config["Options"] = {"timeout": timeout}
        with open(path + "pyParker.ini", "w") as configfile:
            config.write(configfile)

def readConfig():
    global path, errors
    config = ConfigParser()
    config.read(path + "pyParker.ini")
    # Check if the config file is correct
    if not {"Paths", "Options", "Parks"} <= config.keys():
        sys.exit(errors["E001"])

    configfile = dict()  # Create dictionnary for the config

    configfile["datapath"] = config["Paths"]["datapath"]
    configfile["magickingdom"] = config["Parks"].getboolean("magickingdom")
    configfile["epcot"] = config["Parks"].getboolean("epcot")
    configfile["hollywoodstudios"] = config["Parks"].getboolean("hollywoodstudios")
    configfile["animalkingdom"] = config["Parks"].getboolean("animalkingdom")
    configfile["disneyland"] = config["Parks"].getboolean("disneyland")
    configfile["californiaadventure"] = config["Parks"].getboolean("californiaadventure")

    configfile["timeout"] = int(config["Options"]["timeout"])

    return configfile

def verifData():
    global configfile, errors
    makeDir(configfile["datapath"])
    if configfile["magickingdom"]:
        makeDir(configfile["datapath"] + "/Magic Kingdom/")
        makeFile(configfile["datapath"] + "/Magic Kingdom/[INFORMATION].csv")
    if configfile["epcot"]:
        makeDir(configfile["datapath"] + "/Epcot/")
        makeFile(configfile["datapath"] + "/Epcot/[INFORMATION].csv")
    if configfile["hollywoodstudios"]:
        makeDir(configfile["datapath"] + "/Hollywood Studios/")
        makeFile(configfile["datapath"] + "/Hollywood Studios/[INFORMATION].csv")
    if configfile["animalkingdom"]:
        makeDir(configfile["datapath"] + "/Animal Kingdom/")
        makeFile(configfile["datapath"] + "/Animal Kingdom/[INFORMATION].csv")
    if configfile["disneyland"]:
        makeDir(configfile["datapath"] + "/Disneyland Park/")
        makeFile(configfile["datapath"] + "/Disneyland Park/[INFORMATION].csv")
    if configfile["californiaadventure"]:
        makeDir(configfile["datapath"] + "/California Adventure/")
        makeFile(configfile["datapath"] + "/California Adventure/[INFORMATION].csv")

## Check/Store/Write Wait Times and Info
def storeWaitTimes(park):
    writeParkInformation(park)  # Get park info and write the content in a csv
    ids = Park(park).getAttractionIDs()  # Get the IDs of the attractions for the park specified
    data = retrieveWaitTime(park, ids)  # Retrieve the wait times of the attractions
    writeWaitTime(park, data)

def writeParkInformation(park):
    global configfile, folderSwitcher
    info = Park(id=park).getTodayParkHours()  # 0: Open 1: Close 2: EMH Start 3: EMH End
    info_transformed = list()
    info_transformed.append(info[0].strftime("%b %d"))  # Store Month Day
    info_transformed.append(info[0].strftime("%a"))  # Store day of the week
    info_transformed.append(info[0].strftime("%I:%M%p"))  # Store open
    info_transformed.append(info[1].strftime("%I:%M%p"))  # Store close
    if info[2]:
        info_transformed.append(info[2].strftime("%I:%M%p"))
    else:
        info_transformed.append("None")
    if info[3]:
        info_transformed.append(info[3].strftime("%I:%M%p"))
    else:
        info_transformed.append("None")

    # Prepare the info to write it
    info_transformed_ready = "{},{},{},{},{},{}\n".format(info_transformed[0], info_transformed[1], info_transformed[2], info_transformed[3], info_transformed[4], info_transformed[5])
    # Get filepath of information.csv
    info_fp = configfile["datapath"] + "/{}/[INFORMATION].csv".format(folderSwitcher.get(park))
    # Write to file
    with open(info_fp,"a") as info_file:
        headers = "Date,Day,Opening Hours,Closing Hours,Extra Magic Hours Start,Extra Magic Hours End\n"
        with open(info_fp, "r") as info_file_r:  # Check if it already exists
            info_file_rr = info_file_r.read()
            if headers not in info_file_rr:  # Check if the headers are there
                info_file.write(headers)
            if info_transformed_ready not in info_file_rr:
                info_file.write(info_transformed_ready)

def retrieveWaitTime(park, ids):
    data = {}
    for id in ids:
        att = Attraction(id)
        wait = att.getAttractionWaitTime()  # Get the current wait time
        if wait == None:  # Remove everything that doesn't have a wait time and skips does that don't have one
            continue
        
        name = att.getAttractionName()
        if "“" in name:  # Clean the names
            name = name.replace("“", "")
        if "”" in name:
            name = name.replace("”", "")
        if "’" in name:
            name = name.replace("’", "")
        if "~" in name:
            name = name.replace("~", "")
        if "Monsters, Inc. Laugh Floor" in name:
            name = name.replace("Monsters, Inc. Laugh Floor", "Monsters Inc. Laugh Floor")
        if "it\\'s a small world" in name:
            name = name.replace("it\\'s a small world", "its a small world")
        if "*" in name:
            name = name.replace("*", "")
        if "–" in name:
            name = name.replace("–", "")
        if "!" in name:
            name = name.replace("!", "")
        if ":" in name:
            name = name.replace(":", "")
        if "™" in name:
            name = name.replace("™", "")
        if u"\u2018" in name:
            name = name.replace(u"\u2018", "")
        if "\"" in name:
            name = name.replace("\"", "")
        if "\\'" in name:
            name = name.replace("\\'", "")
        
        time = datetime.now().strftime("%b %d,%I:%M%p")  # Get the current time
        data[name] = "{},{}\n".format(time, wait)  # Add the entry for the attraction
    return data

def writeWaitTime(park, data):
    global configfile, folderSwitcher
    for att in data:
        fp = configfile["datapath"] + "/{}/{}.csv".format(folderSwitcher.get(park), att)
        with open(fp, "a") as file_fp:
            headers = "Date,Time,Wait\n"
            with open(fp, "r") as file_r:
                if headers not in file_r.read():
                    file_fp.write(headers)

            file_fp.write(data[att])

folderSwitcher = {  # Have a case/switch conditional to remove the use of if/elif and be save memory
    MK_ID:"Magic Kingdom",
    EPCOT_ID:"Epcot",
    HS_ID:"Hollywood Studios",
    AK_ID:"Animal Kingdom",
    DLP_ID:"Disneyland Park",
    CA_ID:"California Adventure"}

iniConfig()  # Start the configurator
configfile = readConfig()  # Read the configfile and export the result (dictionnary)
verifData()  # Check if folders and datapath are correct and creates them if not
time.sleep(configfile["timeout"])  # Pause the program for the amount of seconds entered in the config file

## Check the parks selected and check/store/write the times
if configfile["magickingdom"]:
    storeWaitTimes(MK_ID)
if configfile["epcot"]:
    storeWaitTimes(EPCOT_ID)
if configfile["hollywoodstudios"]:
    storeWaitTimes(HS_ID)
if configfile["animalkingdom"]:
    storeWaitTimes(AK_ID)
if configfile["disneyland"]:
    storeWaitTimes(DLP_ID)
if configfile["californiaadventure"]:
    storeWaitTimes(CA_ID)