from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import urllib.request
import datetime
import os
import csv
import sys

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

def verifConfig():
    makeDir("./data/")
    makeDir("./data/Magic Kingdom/")
    makeDir("./data/Epcot/")
    makeDir("./data/Disney's Hollywood Studios/")
    makeDir("./data/Disney's Animal Kingdom/")

    makeFile("./data/Magic Kingdom/[INFORMATION].csv")
    makeFile("./data/Epcot/[INFORMATION].csv")
    makeFile("./data/Disney's Hollywood Studios/[INFORMATION].csv")
    makeFile("./data/Disney's Animal Kingdom/[INFORMATION].csv")

def retrieveHTML(selected_park):
    global mk, ep, hs, ak

    if selected_park not in (mk, ep, hs, ak): #Check if park exists
        print("Invalid park selected")
        sys.exit()
    #else: #DEBUG
        #print(selected_park)
    # Specify User-Agent to prevent Error 403: Forbiden
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
    # Create url by using the park specified
    selected_url = "https://www.laughingplace.com/w/p/{}-current-wait-times/".format(selected_park)
    req = urllib.request.Request(selected_url,headers={"User-Agent": user_agent}) # setting headers to go incognito
    uClient = uReq(req) # opening up connection
    page_html = uClient.read() # grabbing page
    uClient.close() # closing connection
    return page_html


def webScrape(page_html):
    page_soup = soup(page_html, "lxml") #html parsing
    title = page_soup.h1.text.strip() #Title of the page
    park = title.replace(" Current Wait Times", "") # Name of the park
    r_datetime = page_soup.findAll("div", {"class":"header"})[0].text.strip() #Find the locations

    date, time = r_datetime.split("\n")
    date, ophour = date.split(": ")
    date = date.replace("Operating Hours For ", "")
    day, date = date.split(", ")
    time = time.replace("Last Check at ", "")
    time = time.replace(":", ".")

    table = page_soup.table
    containers = table.findAll("tr")
    containers = list(dict.fromkeys(containers))

    location={}
    location["park"]=park
    location["ophour"]=ophour
    location["date"]=date
    location["day"]=day
    location["time"]=time

    attlist = {}
    for container in containers:
        entry = container.text.strip()
        #Cleaning entries
        if "\n" in entry:
            c_entry = entry.replace("\n", ",", 1)
            c_entry = c_entry.replace('\n','')
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
        #Split entry to have 2 values
        att, time = c_entry.split(",")
        #Add to dictionnary
        attlist[att] = time
    return attlist, location


def writeCSV(attlist, location):
    filename_info = "data/{}/[INFORMATION].csv".format(location["park"])
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
        filename = "data/{}/{}.csv".format(location["park"], att)
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

verifConfig()
storeWaitTimes(mk)
storeWaitTimes(ep)
storeWaitTimes(hs)
storeWaitTimes(ak)