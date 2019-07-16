import csv
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
## Fix Pandas errors and future-proofing
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Clear any plot that was registered
plt.clf()
# Specify the style of the plot
plt.style.use("ggplot")

#Assign variables
date = ""
data = {}
timewait = []
time = []
wait = []

#Import csv with pandas
csv_file = pd.read_csv("./Space Mountain.csv")

#Get information
for index, row in csv_file.iterrows():
    if row["Wait"] not in ("Closed", "Down"):
        if row["Date"] not in date:
            timewait = [time] + [wait]
            data[row["Date"]] = timewait
            time = []
            wait = []
            timewait = []
        date = row["Date"]
        time.append(datetime.strptime(row["Time"], "%I.%M%p"))
        wait.append(row["Wait"])

# Create a plot for each day
for dat in data:
    plt.plot(data[dat][0], data[dat][1], linestyle="solid", marker="", label=dat)

plt.tight_layout(pad=2)
plt.title("Splash Mountain")
plt.xlabel("Time")
plt.ylabel("Wait (minutes)")
plt.margins(0.05)
plt.legend()
plt.show()