import csv
import os

d = open("temp.csv", "r")
reader = csv.reader(d)
attraction={}
for row in reader:
    attraction[row[0]] = row[1]
d.close()

list_at = ["Astro Orbiter",
            "The Barnstormer",
            "Big Thunder Mountain Railroad",
            "Buzz Lightyears Space Ranger Spin",
            "Country Bear Jamboree",
            "Dumbo the Flying Elephant",
            "Enchanted Tales with Belle",
            "The Hall of Presidents",
            "Haunted Mansion",
            "its a small world",
            "Jungle Cruise",
            "Liberty Square Riverboat",
            "Mad Tea Party",
            "The Magic Carpets of Aladdin",
            "The Many Adventures of Winnie the Pooh",
            "Meet Ariel at Her Grotto",
            "Meet Cinderella and Elena at Princess Fairytale Hall",
            "Meet Daring Disney Pals as Circus Stars at Petes Silly Side Show",
            "Meet Dashing Disney Pals as Circus Stars at Petes Silly Side Show",
            "Meet Mickey Mouse & Minnie Mouse at Town Square Theater",
            "Meet Rapunzel and Tiana at Princess Fairytale Hall",
            "Meet Tinker Bell at Town Square Theater",
            "Mickeys PhilharMagic",
            "Monsters Inc. Laugh Floor",
            "Peter Pans Flight",
            "Pirates of the Caribbean",
            "Prince Charming Regal Carrousel",
            "Seven Dwarfs Mine Train",
            "Space Mountain",
            "Splash Mountain",
            "Swiss Family Treehouse",
            "Tom Sawyer Island",
            "Tomorrowland Speedway",
            "Tomorrowland Transit Authority PeopleMover",
            "Under the Sea  Journey of The Little Mermaid",
            "Walt Disneys Carousel of Progress",
            "Walt Disneys Enchanted Tiki Room"]

z = open("location.csv", "r")
readerr = csv.reader(z)
location={}
for row in readerr:
    park = row[0]
    date = row[1]
    time = row[2]

if not os.path.exists('data'):
    os.makedirs("data")
i = -1
#f = open(, "a")
try:
    for a in list_at:
        i += 1
        wait = attraction[list_at[i]]
        file_name = "data/{}/{}.csv".format(park, list_at[i])
        h = open(file_name, "a")
        h.write(date + "," + time + "," + wait + "\n")
        h.close()
        #print(list_at[i] + " - " + wait)
except:
    print("lol")