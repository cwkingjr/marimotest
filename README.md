# On Windows

Everything here assumes you are working inside a Powershell terminal. Right click the Start Icon and choose Terminal.

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
cd marimotest
ls
```

### Sync dependencies using uv

Inside the marimotest directory, run `uv sync` to pull down all the python dependencies for Marimo and the mytest.py Marimo Notebook. This will take a while the first time so don't be worried, just let it run and watch the status bars as it pulls down Python packages.

```
uv sync
```

### Run via uv run in Marimo edit mode

Marimo offers edit and run modes. Run is for finished projects and edit is for working with projects, changing files, etc. I would recommend using run mode, except that I am having problems with the data view right side panel showing up in run mode, so you may have to use edit mode to be able to see that (at least until I figure out what the problem is).

From inside the marimotest dir, run:

```
uv run marimo edit ./mytest.py -- --infile fake-data-3000-rows.csv
```

To explain the above, I will break down some parts. We're using uv to manage Python, dependencies, and virtual environments here. Instead of worrying about learning all about Python installation and packaging and setting up virtual environments, uv will use the info in the local repo's files to download and install the version of python needed, all python dependency packages needed by this project, installed within a virtual environment inside this project (under the dir .venv) so these dependencies don't interfere with any other project's dependency needs/versions. Because of that, we launch projects using uv also, but using a different subcommand (run instead of sync).

Here is what the parts do of that long command line invocation do:

`uv run marimo` launches marimo using the local python virtual environment.

`marimo run ./mytest.py` uses the marimo `run` subcommand to run the `./mytest.py` Python file.

`--` tells `uv run` that any arguments after this are not for `uv run` and need to get passed on to `marimo run` for processing.

`--infile fake-data-3000-rows.csv` becomes an argument passed into the Python environment that is running the mytest.py file, where I use code to find out what the file path passed in was and display that in the left sidebar and use that path to load the CSV data.

### Run via uv run in Marimo run mode

In the marimotest directory, run the project in either run or edit mode. I'd recommend trying both to see what is there.

Run

```
uv run marimo run ./mytest.py -- --infile fake-data-3000-rows.csv
```

Edit

```
uv run marimo edit ./mytest.py -- --infile fake-data-3000-rows.csv
```

This will open you web browser to a local file and start showing the data. Meanwhile, the Terminal will be blocked. When you are ready to stop using the app, go to the terminal and hit Control-C to kill the uv marimo process. Then just close your browser tab.

Let me know if any of these instructions don't make sense or are wrong.
