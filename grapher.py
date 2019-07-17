import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from datetime import datetime
from pandas.plotting import register_matplotlib_converters  # Fix Pandas errors and future-proofing
register_matplotlib_converters()  # See line5

plt.clf()  # Clear any plot that was registered during an error
# Specify the style of the plot
plt.style.use("classic")
plt.rcdefaults()  # DEBUG removes any style used before


def getInfo(cs_file, month="all", select="alltime", option="all", analysis="raw"):
    if select == "alltime":
        #Assign variables
        date = ""
        data = {}
        timewait = []
        time = []
        wait = []

        #Import csv with pandas
        csv_file = pd.read_csv(cs_file)
        att = cs_file.replace(".csv", "")
        #Get information
        for index, row in csv_file.iterrows():
            if row["Wait"] not in ("Closed", "Down", "Open"):
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
    if select == "latest_week":
        pass
    if select in (sun, mon, tues, wed, thurs, fri, sat):
        pass
    else:
        return("Invalid parameter for mode/analysis, please check again")
        print("Invalid parameter for mode/analysis, please check again")

def createPlot(data, att, debug=False):
    # Create a plot for each day
    ax = plt.gca()
    fig = plt.gcf()

    for dat in data:
        plt.plot_date(data[dat][0], data[dat][1], marker=">", linestyle="solid", label=dat, xdate=True)  #xdate=True
    """ 
    axes = ax # Get current axes
    axes.set_ylim([0,None]) # Wait times cannot be under 0 min.
    axe = plt.axes()
    """

    ## X
    # Label axis
    plt.xlabel("Time", fontsize=15, fontweight="bold")  # Add label for x axis
    fig.autofmt_xdate(rotation=15)  # Put a rotation on the dates to be more clear
    # Label data
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))  # Select the formatting for the minor tick dates
    ax.set_axisbelow(True)  # Always have axis/grids under the data
    # Minor Ticks
    ax.minorticks_on()  # Activate the minor ticks on both axis
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%M"))  # Select the formatting for the major tick dates
    # Ticks Formatter
    ax.tick_params(axis="x", which="both", width=3)  # Set the width between the ticks
    ax.tick_params(axis="x", which="major", length=15, labelsize=10, colors="k")
    ax.tick_params(axis="x", which="minor", length=3.5, labelsize=8, colors="r")
    # Tick Location
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_minor_locator(mdates.MinuteLocator((15, 30, 45)))
    plt.xlim((693596.3333333334, 693597))

    ## Y
    plt.ylabel("Wait (minutes)", fontsize=15, fontweight="bold")  # Add label for y axis
    # ax.yaxis.set_major_formatter(mdates.AutoDateFormatter(mdates.AutoDateLocator()))
    plt.ylim((0, None))
    plt.yticks(fontsize=18)
    # ax.yaxis.set_minor_locator(mdates.AutoDateLocator())

    ## General Graph
    # Layout
    # plt.tight_layout(pad=2)  # Fix layout
    plt.title(att, fontsize=20, fontweight="bold")  # Add title
    #plt.margins(0.05)  # DEBUG Specify the margins of the file
    plt.legend(loc="upper left") # Add a Legend and set it in the upper left corner
    # Grid
    plt.grid(b=True, which="major", axis="both", linestyle="-", linewidth="1", color="k", alpha=0.9)  # Modify the grid format for the major ticks
    plt.grid(b=True, which="minor", linestyle="--", linewidth="0.5", color="r", alpha=0.75)  # Modify the grid format for the minor ticks

    ## Exporter
    # Save to a file
    fig.set_size_inches(15, 10, forward=True)  # Set size of the image
    export_png = "graph/{}.png".format(att)
    plt.savefig(export_png, format="png")  # Save image in a folder
    # DEBUG
    if debug == True:
        plt.show()  # DEBUG Show plot
    ## Clear
    plt.clf()  # Resets the plot for a new attraction

def buildPlot(cs_file, month="all", select="alltime", option="all", analysis="raw", debug=False):  # File: File to build Plot from                                  # Option: What to show (all, magic_hour)
    data, att = getInfo(cs_file, month=month, select=select,                                       # Month: Which month of the year(jan, feb...)                    # Analysis: How to interpret the data (raw, avg, med)
                        option=option, analysis=analysis)                                           # Select: What Data to choose(alltime, latest_week, last_week, mon/tues...)                                      
    
    createPlot(data, att, debug=debug)

buildPlot("Space Mountain.csv")
buildPlot("The Twilight Zone Tower of Terror.csv")
buildPlot("Lightning McQueens Racing Academy.csv")