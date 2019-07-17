import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from datetime import datetime
from pandas.plotting import register_matplotlib_converters  # Fix Pandas errors and future-proofing
register_matplotlib_converters()  # See line5

plt.clf()  # Clear any plot that was registered during an error
# Specify the style of the plot
# plt.style.use("ggplot")
plt.rcdefaults()  # DEBUG removes any style used before


def getInfo(file, mode, analysis):
    if mode == "alltime":
        #Assign variables
        date = ""
        data = {}
        timewait = []
        time = []
        wait = []

        #Import csv with pandas
        csv_file = pd.read_csv(file)
        att = file.replace(".csv", "")
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
                time.append(mdates.date2num(datetime.strptime(row["Time"], "%I.%M%p")))
                wait.append(int(row["Wait"]))
        return data, att  # Sun,Mon => %a
    if mode == "latest_week":
        pass
    if mode in (sun, mon, tues, wed, thurs, fri, sat):
        pass
    else:
        return("Invalid parameter for mode/analysis, please check again")
        print(")Invalid parameter for mode/analysis, please check again")

def createPlot(data, att):
    # Create a plot for each day
    # fig, ax = plt.subplots()
    for dat in data:
        plt.plot_date(data[dat][0], data[dat][1], marker=">", linestyle="solid", label=dat)  #xdate=True
    """ 
    axes = plt.gca() # Get current axes
    axes.set_ylim([0,None]) # Wait times cannot be under 0 min.
    axe = plt.axes()
    """
    # plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%I.%M%p"))
    plt.tight_layout(pad=2)  # Fix layout
    plt.title(att)  # Add title
    plt.xlabel("Time")  # Add label for x axis
    plt.ylabel("Wait (minutes)")  # Add label for y axis
    # plt.margins(0.05)  # DEBUG Specify the margins of the file
    plt.legend(loc="upper left")
    fig = plt.gcf()
    fig.set_size_inches(15, 10, forward=True)
    plt.savefig("graph/{}.png".format(att))
    plt.show()  # DEBUG Show plot
    plt.clf()  # Resets the plot for a new attraction

def buildPlot(file, mode="alltime", analysis="all"):  # Analysis: all-show everything/average-make an average of mode/median-make a median
    data, att = getInfo(file, mode, analysis)
    createPlot(data, att)

buildPlot("Space Mountain.csv")