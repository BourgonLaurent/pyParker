# pyParker

                  ______               _                
                  | ___ \             | |               
     _ __   _   _ | |_/ /  __ _  _ __ | | __  ___  _ __ 
    | '_ \ | | | ||  __/  / _` || '__|| |/ / / _ \| '__|
    | |_) || |_| || |    | (_| || |   |   < |  __/| |   
    | .__/  \__, |\_|     \__,_||_|   |_|\_\ \___||_|   
    | |      __/ |   © Laurent Bourgon for pyParker, parkerGrapher
    |_|     |___/    © Scott Caratozzolo for MouseTools module

`Python3` program that records wait times and extra information at Walt Disney World, Orlando (Florida) and Disneyland, Anaheim (California).
Created this program to plan a family trip at Walt Disney World.

## Requirements

- `Python3` (might work with `Python2`, but not tested and will not be supported)
    - [`MouseTools` by Scott Caratozzolo](https://github.com/scaratozzolo/MouseTools), already included 1.2.0beta (as of 2019-07-22) with this program, it may be necessary to update it manually if Disney change their internal API
    - `requests`, sometimes included by default, sometimes not. If not, you can install it with pip `pip install requests`
- Internet connection
- Rights in the folder you're in (especially for users on Synology's DSM)

## Instructions

1. Download the latest version of `pyParker_vx.x.x.zip` in [Releases](https://github.com/BourgonLaurent/pyParker/releases)
2. Extract the content of `pyParker_vx.x.x.zip`
    - It is recommended to put all the files in it's own folder, because it will create automatically a folder `data` and a file `pyParker.ini` at the place where it is located if you use the default location
3. If you don't have `Python3` installed, [install it manually](https://www.python.org/downloads/) or use a package manager(recommended) (apt on Linux, [homebrew on macOS](https://brew.sh/), [chocolatey on Windows](https://chocolatey.org/), etc.)
4. Make sure you have the required `Python3` modules installed ([check Requirements](README.md#Requirements))
5. Open Terminal/CMD/Powershell, navigate to `pyParker.py`'s folder (using `cd`) and run the program by entering `python3 pyParker.py`.
    - `pyParker.py` will never change it's name (unless there's a rebranding), this is made so you can set a task scheduler and never worry about a filename change.

## Using it

At the first run (or if the `pyParker.ini` is deleted), the configurator will load. It will ask you were you want to store the files, which worlds (and parks if you select the advanced options) you want and if you want to use a sleep option for task scheduler that only support intervals of 10 minutes. Here is the default config (if you press `Enter` at each prompt)

| Prompt                                                                                                                | Default | What it does                                                   | Example                                                                                                                   |
|-----------------------------------------------------------------------------------------------------------------------|---------|----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Where do you want the files stored?*                                                                                  | ./data | A folder `data` will be created at the location of the script. | C:\pyParker\data will be created, if `pyParker.py` is in C:pyParker\                                                     |                                      | If you press `Enter` on `Walt Disney World, Orlando (Florida)`, the program will not store the wait times and information of Walt Disney World.|
| Here's a list of parks, select those that you want to log [Y]es/[N]o/[A]dvanced**:                                                 | No      | The world will not be logged.                                      | If you press `Enter` on `Walt Disney World, Orlando (Florida)`, the program will not store the wait times and information.|
| You can specify a time in seconds to pause the script, useful if your task scheduler only has intervals of 10 minutes | 0       | The program will not be put in sleep, it will be instant.      | When you run the program, it will directly fetch the wait times, as fast as possible.                                       |

\*_You can specify the data folder easily by drag-and-dropping the folder in your shell interface._

\**_You can select `A` and access advanced options to select a specific park (ex. you can log Magic Kingdom, but not Epcot)_

Inside the folder specified (or the default one) there will be sub-folders for each park. Inside these folders you will find a file for each attraction and an [INFORMATION].csv file, this file contains *the date, the day of the week, the opening hours and Extra Magic Hours.* To interpret the data in a graph or a table, you will have to use an external tool.

To have it log wait times automatically, you will have to schedule a task using Windows Task Scheduler, cron, Synology's Task Scheduler, etc. This choice was made to give more flexibility to the user and reduce the possible number of errors or memory leak of the program.

If you have a server that is headless (does not have a GUI) and that you can't run this program through command-line or SSH, you will have to execute it on your computer and then transfer the `pyParker.py` and `pyParker.ini` file on your server. Remember to use the right paths that are corresponding to your NAS/Server and not your computer.

For Synology's DSM users, if you use relative paths (AKA the default) in the config file, you will have some problems, please specify a whole path (ex: `/volume1/Documents/pyParker/data/`)

To use the configurator again, you just have to delete the `pyParker.ini` file.

## TODO

(This list is made in chronological order that it will be happening, it may change)

- Create a repository that will have the waits I logged by commiting changes automatically.
- ~~Transform all the web scraping in a module.~~ *There's no more web scraping, it may be done for other parks, we will see* 2019-07-22
- ~~Make a TUI to create a script for automation (currently the script needs to be modified manually to use on a Synology).~~ *Fixed by making a `pyParker.ini` file that the program reads and creates at first run* 2019-07-11
- ~~Take data directly from Disney, this will provide accurate data at the time specified.~~ *Fixed by using Scott Caratozzolo's MouseTools python module* 2019-07-22
- Support ~~Disneyland, CA~~*Fixed by using Scott Caratozzolo's MouseTools python module* and Universal Studios, FL (same website, same webscrape, just need to implement it)
- Support other parks (Six Flag and others).
- Script that will convert it in a graph instead of doing it manually.
- Implement a GUI to select parks and to create a graph.

## Credits

Data taken directly from Disney using their internal API. To save time and headaches, this program uses [Scott Caratozzolo's `MouseTools` python module](https://github.com/scaratozzolo/MouseTools).

## Licensing

> _**This is free and unencumbered software released into the public domain.**_
>
> _**Anyone is free**_ to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.
>
> In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.
>
> THE SOFTWARE IS PROVIDED "AS IS", _**WITHOUT WARRANTY**_ OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
> For more information, please refer to <http://unlicense.org>
