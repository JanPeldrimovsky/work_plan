# Work plan
Simple application for planning a workday

Plans are created in a plain text file with format:
```
yyyy-MM-dd.txt
```

Files can be placed in subfolders.

Plan file format:
```
hh:mm - activity
```

For example:
```
07:30 - plan the day
07:40 - review last day's work
08:00 - solve task #35
08:30 - pause
08:35 - solve task #35
09:00 - stop
```

At the time of the planned item, a pop-up window shows planned activity accompanied by gong sound.
If the plan file is not defined, activity has no defined end or activity is longer than one hour, pop-up window describing problem shows accompanied by an annoying beeping sound.

Usage:
```
python parse_plan.py --plan_folder "path\to\plan\folder"
```

On Windows I have created a batch file, that runs after computer starts and since I don't want to see command line window I use *pythonw* instead of *python*:
```
pythonw path/to/parse_plan.py --plan_folder "path/to/plan/folder"
```

