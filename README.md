> Warning: At the time of writing, pgcontest website appears to have an expired certificate. Follow the links to pgcontest on your own risk or wait for them to fix it.

# What is this?

You might stumble upon this repository if you were browsing solutions to previous competitions on [pgcontest from VSB](https://pgcontest.vsb.cz/contest/) or their GitLab.

This repository features helper programs that analyzed input datasets and helped me to build my solution in the [key-value storage](https://pgcontest.vsb.cz/contest/task/3) task.

# How do I use it?
The scripts are written in Python and work on both Windows and Linux. On Windows you can use batch scripts in the [run](/run) directory to run them with ease. On Linux you can start your selected script from a command line:

```
python -m src.{subdirectory}.main {arguments}
```

The [src](/src) folder contains multiple programs. The text below describes them in more detail.

## Dataset analyzer
### Purpose
- Produces graphs and statistics from the input dataset.

### Usage
- Simply drop valid dataset onto the script or pass its path as a argument from command line.
- Wait for it to finish work.
- Follow instructions.
- If you don't want to perform all the measurements, you can comment lines 10-17 in [main.py](/src/dataset_analyzer/main.py) and choose statistics you actually want to compute.

## Dataset generator
### Purpose
- Produces example datasets of a user-specified length.
- It was used for testing slow solutions and in combination with [solution generator](/src/solution_generator) it was used to check for correctness of a solution before uploading it to the competition server.

### Usage
- Optional arguments:
    - *--base_dir* : path to output folder, end with '\\'
    - *--start_at*: name of a subdirectory of a output folder
- Execute the [script](/src/dataset_generator/main.py).
- Follow instructions.
- The dataset should now be ready in the output directory you specified in the arguments.

## Solution generator
### Purpose
Produces solution files for a given dataset. However implemented algorithm is too slow and wasn't competitively viable. It was used only for testing purposes.

### Usage
- Optional arguments:
    - *--base_dir* : path to output folder, end with '\\'
    - *--start_at*: name of a subdirectory of a output folder
- Simply drop valid dataset onto the script or pass its path as a argument from command line.
- Wait for it to finish work.
- Follow instructions.
- The dataset should now be ready in the output directory you specified in the arguments.

## File comparator
### Purpose
Compares lines of two files and searches for differences. It was used for detecting mistakes in solution files.

### Usage
- Optional arguments:
    - *--base_dir* : path to output folder, end with '\\'
    - *--start_at*: name of a subdirectory of a output folder
- Drop two files onto the script or pass their paths as arguments from command line.
- Wait for it to finish work.
- A preview of found differences will appear.
- Follow instructions.
- If you saved the differences file, you can find in the output directory you specified in the arguments.

## File slicer
### Purpose
Creates smaller files from large datasets.

### Usage
- Optional arguments:
    - *--base_dir* : path to output folder, end with '\\'
    - *--start_at*: name of a subdirectory of a output folder
- Drop a file onto the script or pass its path as a argument from command line.
- Enter number of lines a copy should have.
- New dataset will be saved to the output directory you specified in the arguments.
