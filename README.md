# pyParker

`Python3`program that records wait times and extra information at Walt Disney World, FL. Created this program to plan a family trip at Walt Disney World.

## Requirements

- `Python3` (might work with `Python2`, but not tested and will not be supported)
  - [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) installed
  - `urllib3`, it is a default python module, but on some installations it isn't
- Internet connection
- Rights in the folder you're in (especially on Synology's DSM)

## Instructions

1. Download the latest version of `pyParker.py` in [Releases](https://github.com/BourgonLaurent/pyParker/releases)
    - It is recommended to put it it's own folder, because it will create automatically a folder `data` at the place where it executed
2. If you don't have `Python3` installed, [install it](https://www.python.org/downloads/)
3. If you don't have `BeautifulSoup4`, install it [manually](https://www.crummy.com/software/BeautifulSoup/) or with `pip` (`pip install beautifulsoup4`)
4. Open Terminal/CMD/Powershell, navigate to `pyParker.py`'s folder (using `cd`) and run the script by entering `python3 pyParker.py`.

## Using it

A folder `data` will be created, inside this folder there will be sub-folders for each park. Inside these folders you will find a file for each attraction and a [INFORMATION].csv file, this file contains *the date, the day of the week, the opening hours and Extra Magic Hours.* To interpret the data, you will have to use an external tool.

## TODO

(This list is made in chronological order, it may change)

- Create a repository that will have the waits I logged by commiting changes automatically.
- Transform all the web scraping in a module.
- Make a sudo-GUI to create a script for automation (currently the script needs to be modified manually to use on a Synology).
- Take data directly from Disney, this will provide accurate data at the time specified.
- Support Disneyland, CA and Universal Studios, FL (same website, same webscrape, just need to implement it)
- Support other parks (Six Flag and others).
- Script that will convert it in a graph instead of doing it manually.
- Implement a GUI to select parks and to create a graph.

## Credits

Data taken from [Laughing Place](http://laughingplace.com), there's a way to take them from Disney directly.

## Licensing

> _**This is free and unencumbered software released into the public domain.**_
>
> _**Anyone is free**_ to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.
>
> In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.
>
> THE SOFTWARE IS PROVIDED "AS IS", _**WITHOUT WARRANTY**_ OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
> For more information, please refer to <http://unlicense.org>
