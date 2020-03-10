How to use:

Choose and run batch files located in folder */run_scripts*. On Linux you might want to use directly corresponding *main.py* files located in */src* subdirectories.

**Dataset analyzer**

- simply drop valid dataset onto the script or batch file
- wait for it to finish work
- follow instructions, path to save files is starting at working directory

**Dataset generator**

- there are some optional arguments:
    - *--base_dir* : sets path to starting directory for saving files, end with '\'
    - *--start_at*: set subdirectory for saving files
- execute script
- follow instructions in console

**Solution generator**

- there are some optional arguments:
    - *--base_dir* : sets path to starting directory for saving files, end with '\'
    - *--start_at*: set subdirectory for saving files
- simply drop valid dataset onto the script or batch file
- wait for it to finish work
- follow instructions in console

**File comparator**

- there are some optional arguments:
    - *--base_dir* : sets path to starting directory for saving file differences, end with '\'
    - *--start_at*: set subdirectory for saving differences
- drop two files onto the script or batch file
- wait for it to finish work
- a preview of found differences will appear
- follow instructions in console
