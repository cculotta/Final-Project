
# COMP 170 SU25 Final Project

<mark>Note that `Birthday` and `Person` are not in final version yet, as they are part of an ongoing homework assignment. Final versions of these two classes will be posted here on July 23.</mark>

## Scope
Build an application to manage contact information about your friends. The application should provide a menu with the following functions.
```text
1 - Create new friend record
2 - Search for a friend
3 - Run reports
4 - Exit
```

### Options for menu 1
You can create a new record for a single person, by manually entering their information in the application. Or, you may load data for multiple friends from a [csv file](https://en.wikipedia.org/wiki/Comma-separated_values).

### Options for menu 2
If a friend is found, the user should have the option to edit the friend's record or delete it. Deletion should be a 2-step process.

### Options for menu 3
The application should offer the following reports
```text
3.1 - List of friends alphabetically
3.2 - List of friends by upcoming birthdays
3.3 - Mailing labels for friends
3.9 - Return to the previous menu
```

## Requirements

* Code must be based on classes `Person` and `Birthday`.
* Code must be modular (multiple cooperating `.py` files)
* You may import modules you develop or improve (for example `import Person`). For any other imports you must first obtain instructor's permission.
* Use of some basic text decoration would be nice: bold fonts, colored fonts etc. (You may need to learn how to use ANSI codes for such decorations.)
* When you turn on the application, the records of the friends must be loaded from a file called `friends_database.csv`.
* The records of the friends must be saved in a file called `friends_database.csv` every time you exit the application.
* Duplicate entries are allowed -- for example you may have two records for the same friend. Not a good idea, but managing duplicates adds complexity to the project that is best to avoid.
* <mark>Expect these requirements to change overtime, as we discuss the project in class.</mark>
