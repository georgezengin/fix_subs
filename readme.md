<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Project fix_subs</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> 
## Movie Collection Beautifier


</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Author](#authors)

## 🧐 About <a name = "about"></a>

A Python script to rename movie folders by extracting and formatting the name, year, and release description as:
`<name> (year) [release_description]`.

## Features

- Traverse through subfolders to process multi-level structures (in case of groupings by year, genre, etc)
- Option to remove release descriptions (leave only name and year)
- Demo mode to show actions without performing them.
- Logging support with 3 log levels.
- Silent mode to suppress console output.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

- Python 3.x

```
Python 3.x
```

### Installing

Clone the repository:

```bash
git clone https://github.com/georgezengin/fix_subs.git
cd fix_subs
```

## 🎈 Usage <a name="usage"></a>

Go to the folder where the movies folders are.
Run the app as in the example above, or use a cmd/ps1/sh file as in the ones in the repo (provided as samples) to perform other automated cleanup tasks at the same time of the renaming.

Use flag -h or --help to get a usage description of the parameters

```
$ python fix_year.py -h
usage: fix_year.py [-h] [--nodesc] [--demo] [--log] [--logfile LOGFILE] [--loglevel {DEBUG,INFO,ERROR}] [--silent] [--recurse] [folder_path]

Rename movie folders by extracting and formatting name, years and release description as <name> (year) [release_description].

positional arguments:
  folder_path           Path to the folder containing the directories to rename

options:
  -h, --help            show this help message and exit
  --nodesc, -S          Short name. Do not append movie release description after the year
  --demo, -D            Demo mode. Show actions without performing them
  --log, -L             Enable logging
  --logfile LOGFILE, -F LOGFILE
                        Log file name (self generated if not specified)
  --loglevel {DEBUG,INFO,ERROR}, -LL {DEBUG,INFO,ERROR}
                        Set logging level
  --silent, -H          Silent/hush mode: suppress console output of log information
  --recurse, -R         Recursive mode: traverses through subfolders
$
```
Usage samples
Given a folder with contents like this:
![image](https://github.com/user-attachments/assets/faae0f0d-3bde-43ab-8253-771a532ef5de)

```
python fix_year.py .
```
Run on the current folder, perform the changes, do not log, get console output with the changes performed
Use flag -D or --demo to run a demo mode without applying changes

```
python fix_year.py . --log --loglevel DEBUG --demo
```

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org/) - Language

## ✍️ Authors <a name = "authors"></a>

- [@georgezengin](https://github.com/georgezengin) - Idea & Initial work

See also the list of [contributors](https://github.com/georgezengin/The-Documentation-Compendium/contributors) who participated in this project.

