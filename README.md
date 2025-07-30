# On Windows

Everything here assumes you are working inside a Powershell terminal. Right click the Start Icon and choose Terminal.

WARNING: At some point I intend to reword this to expect the user to be using the Git Bash terminal, but I have not confirmed that everything here (especially the uv install) will work in Git Bash. Git Bash (to me), is a far superior terminal for normal unix stuff as it adds numerous Unix commands that are super useful.

For Git Bash training/info, see this repo: https://github.com/cwkingjr/unix-command-intro-for-windows-folks.

Note, you can cd up one dir with `cd ..`, up two with `cd ../..`, or down more than one with e.g., `cd dir_one/dir_two`.

### Install Git

https://www.youtube.com/watch?v=iYkLrXobBbA

Verify git is with:

```
git version
```

### Install uv

Run this command:

`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Verify uv is installed with:

```
uv --version
```

### Create `dev` folder and change directory into it

Run these commands:

Check that you are in your home directory. Response to `pwd` (present working directory) should be "PS C:\Users\chuck>" but with your user name.

```
pwd
```

Make the directory.

```
mkdir dev
```

List the directory.

```
ls
```

Change directory into your new dev directory.

```
cd dev
```

### Clone repository into `dev` directory

In `dev` directory (check with `pwd`), run these commands:

- Clone the marimotest repo from github into your local dev directory, cd into the marimotest directory (that the clone makes), and preview the directory using `ls`.

```
git clone https://github.com/cwkingjr/marimotest.git
ls
cd marimotest
ls
```

### Sync dependencies using uv

Inside the marimotest directory, run `uv sync` to pull down all the python dependencies for Marimo and the sim_analysis.py Marimo Notebook. This will take a while the first time so don't be worried, just let it run and watch the status bars as it pulls down Python packages.

```
uv sync
```

### Run via uv run in Marimo edit mode

Marimo offers edit and run modes. Run is for finished projects and edit is for working with projects, changing files, etc. I would recommend using run mode, except that I am having problems with the data view right side panel showing up in run mode, so you may have to use edit mode to be able to see that (at least until I figure out what the problem is).

From inside the marimotest dir, run:

```
uv run marimo edit ./sim_analysis.py -- --infile ./fake-data-5000-rows.csv
```

To explain the above, I will break down some parts. We're using uv to manage Python, dependencies, and virtual environments here. Instead of worrying about learning all about Python installation and packaging and setting up virtual environments, uv will use the info in the local repo's files to download and install the version of python needed, all python dependency packages needed by this project, installed within a virtual environment inside this project (under the dir .venv) so these dependencies don't interfere with any other project's dependency needs/versions. Because of that, we launch projects using uv also, but using a different subcommand (run instead of sync).

Here is what the parts do of that long command line invocation do:

`uv run marimo` launches marimo using the local python virtual environment.

`marimo run ./sim_analysis.py` uses the marimo `run` subcommand to run the `./sim_analysis.py` Python file.

`--` tells `uv run` that any arguments after this are not for `uv run` and need to get passed on to `marimo run` for processing.

`--infile ./fake-data-5000-rows.csv` becomes an argument passed into the Python environment that is running the mytest.py file, where I use code to find out what the file path passed in was and display that in the left sidebar and use that path to load the CSV data.

### Run via uv run in Marimo `run` or `edit` mode

In the marimotest directory, run the project in either `run` or `edit` mode. I'd recommend trying both to see what is there.

Run (`marimo run`)

```
uv run marimo run ./sim_analysis.py -- --infile ./fake-data-5000-rows.csv
uv run marimo run ./sim_analysis.py -- --infile ./prod_data.csv
uv run marimo run ./review_any_csv.py -- --infile ./fake-data-5000-rows.csv
```

Edit (`marimo edit`)

```
uv run marimo edit ./sim_analysis.py -- --infile ./fake-data-5000-rows.csv
```

This will open you web browser to a local file and start showing the data. Meanwhile, the Terminal will be blocked. When you are ready to stop using the app, go to the terminal and hit Control-C to kill the uv marimo process. Then just close your browser tab.

Let me know if any of these instructions don't make sense or are wrong.

## Getting Repo Updates

Developers will push changes to a feature branch within the GitHub repository, review the code, and merge good code into the main branch, which is what you got when you ran the git clone command. Once you have run the git clone command, you will have the current code at that time, but will have to pull down any updates.

To get project code updates from the main branch, run this command from within the marimotest directory.

```
git pull
```

To make things easy on yourself and save a bunch of typing, see the alias command info in the unix repo mentioned above.

## Using the Fake Data Generator

The fake data generator takes one argument, which is the number of rows you want to generate. Below, it's passed 100000, and the output from stdout is redirected into a file for use later.

```
uv run ./generate_fake_data.py 100000 > fake-data-100000-rows.csv
```

If you do not pass it an argument, it will generate 1 row and display that vertically just to show you the format of generated data for each column. So, with no argument, just let it stream to stdout.

```
uv run ./generate_fake_data.py
```
