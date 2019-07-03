from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import urllib.request
import datetime
import os

# Sources URL
mk = "https://www.laughingplace.com/w/p/magic-kingdom-current-wait-times/" # Magic Kingdom

# Accepted headers
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"

req = urllib.request.Request(mk,headers={"User-Agent": user_agent}) # setting headers to go incognito
uClient = uReq(req) # opening up connection
page_html = uClient.read() # grabbing page
uClient.close() # closing connection

page_soup = soup(page_html, "lxml") #html parsing

title = page_soup.h1.text.strip() #Title of the page
park = title.replace(" Current Wait Times", "") # Name of the park
#r_time = page_soup.findAll("div", {"class":"header"})[0].findAll("span", {"id":"f_lastcheck"})[0].text.strip() # Last refresh

r_datetime = page_soup.findAll("div", {"class":"header"})[0].text.strip()

date, time = r_datetime.split("\n")

date, ophour = date.split(": ")
date = date.replace("Operating Hours For ", "")
day, date = date.split(", ")

time = time.replace("Last Check at ", "")
time = time.replace(":", ".")

table = page_soup.table
containers = table.findAll("tr")
containers = list(dict.fromkeys(containers))


t_break = "\n"
w_break = "\n\n\n\n"

temp = "temp.csv"
filename = "{} - {} - {}.csv".format(date, park, time)
f = open(temp, "w+")

location = "location.csv"
z = open(location, "w+")

loc = "{},{},{}".format(park, date, time)
z.write(loc)
#headers = "Attraction, Time\n"
#f.write(headers) #CSV headers creation

mklist = []

for container in containers:
    entry = container.text.strip()
    #if "\n\n\n\n" in entry:
    #    c_entry = entry.replace("\n\n\n\n", ", ")
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
    #att, tim = entry.split(", ")
    mklist.append(c_entry)

mklist = list(dict.fromkeys(mklist)) #Remove duplicates

for i in mklist: #Write to file
    f.write(i + "\n")

"""
Exemple de ce que je veux
finalfinal = park + " - " + attraction (ex. Magic Kingdom - Astro Orbiter.csv)
Dans le csv:
date, time, wait
Jul 02, 5.02pm, 30 
"""
#print(mklist)

#import wdisorting
#import wdisorting