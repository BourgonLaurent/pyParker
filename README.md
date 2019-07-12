# pyParker

                  ______               _                
                  | ___ \             | |               
     _ __   _   _ | |_/ /  __ _  _ __ | | __  ___  _ __ 
    | '_ \ | | | ||  __/  / _` || '__|| |/ / / _ \| '__|
    | |_) || |_| || |    | (_| || |   |   < |  __/| |   
    | .__/  \__, |\_|     \__,_||_|   |_|\_\ \___||_|   
    | |      __/ |                                      
    |_|     |___/    

`Python3` program that records wait times and extra information at Walt Disney World, FL. Created this program to plan a family trip at Walt Disney World.

## Requirements

- `Python3` (might work with `Python2`, but not tested and will not be supported)
  - [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) installed (`pip install bs4`)
  - `urllib3`, it is a default python module, but on some installations it isn't (`pip install urllib3`)
  - `lxml`, use pip (`pip install lxml`)
- Internet connection
- Rights in the folder you're in (especially on Synology's DSM)

## Instructions

1. Download the latest version of `pyParker.py` in [Releases](https://github.com/BourgonLaurent/pyParker/releases)
    - It is recommended to put it it's own folder, because it will create automatically a folder `data` at the place where it executed if you use the default location
2. If you don't have `Python3` installed, [install it manually](https://www.python.org/downloads/) or use a package manager(recommended) (apt on Linux, homebrew on macOS, chocolatey on Windows, etc.)
3. Make sure you have the required `Python3` modules installed ([check Requirements](README.md#Requirements))
4. Open Terminal/CMD/Powershell, navigate to `pyParker.py`'s folder (using `cd`) and run the script by entering `python3 pyParker.py`.

## Using it

At the first run (or if the `config.ini` is deleted), the configurator will load. It will ask you were you want to store the files, which parks you want and if you want to use a sleep option for task scheduler that only support intervals of 10 minutes. Here is the default config (if you press `Enter` at each prompt)

| Prompt                                                                                                                | Default | What it does                                                   | Example                                                                                                                     |
|-----------------------------------------------------------------------------------------------------------------------|---------|----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Where do you want the files stored?*                                                                                  | ./data/ | A folder `data` will be created at the location of the script. | C:\pyParker\data will be created, where `pyParker.py` is in C:pyParker\                                                     |
| Here's a list of parks, select those that you want to log [Y]es/[N]o:                                                 | No      | The park won't be logged.                                      | If you skip Magic Kingdom by pressing `Enter` or some other than Y or Yes, Magic Kingdom will not be logged by the program. |
| You can specify a time in seconds to pause the script, useful if your task scheduler only has intervals of 10 minutes | 0       | The program will not be put in sleep, it will be instant.      | When you run the program, it will directly fetch the wait times, as fast as possible.                                       |


\*_You can specify the data folder easily by drag-and-dropping the folder in your shell interface._

Inside the folder specified (or the default one) there will be sub-folders for each park. Inside these folders you will find a file for each attraction and an [INFORMATION].csv file, this file contains *the date, the day of the week, the opening hours and Extra Magic Hours.* To interpret the data, you will have to use an external tool.

To have it log wait times automatically, you will have to schedule a task using Windows Task Scheduler, cron, Synology's Task Scheduler, etc. This gives more flexibility to the user and reduces the number of errors/memory leak of the program.

If you have a server that is headless (does not have a GUI) and that you can't run this program through command-line or SSH, you will have to execute it on your computer and then transfer the `pyParker.py` and `config.ini` file on your server. Remember to use the right paths that are corresponding to your NAS/Server and not your computer.

For Synology's DSM users, if you use relative paths (AKA the default) in the config file, you will have some problems, please specify a whole path (ex: `/volume1/Documents/pyParker/data/`)

To use the configurator again, you just have to delete the `config.ini` file.

## TODO

(This list is made in chronological order of happening, it may change)

- Create a repository that will have the waits I logged by commiting changes automatically.
- Transform all the web scraping in a module.
- ~~Make a TUI to create a script for automation (currently the script needs to be modified manually to use on a Synology).~~ *Fixed by making a `config.ini` file that the program reads and creates at first run*
- Take data directly from Disney, this will provide accurate data at the time specified.
- Support Disneyland, CA and Universal Studios, FL (same website, same webscrape, just need to implement it)
- Support other parks (Six Flag and others).
- Script that will convert it in a graph instead of doing it manually.
- Implement a GUI to select parks and to create a graph.

## Credits

Data taken from [Laughing Place](http://laughingplace.com), there's a way to take them from Disney directly, it will come one day.

## Licensing

> _**This is free and unencumbered software released into the public domain.**_
>
> _**Anyone is free**_ to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.
>
> In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.
>
> THE SOFTWARE IS PROVIDED "AS IS", _**WITHOUT WARRANTY**_ OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
> For more information, please refer to <http://unlicense.org>
