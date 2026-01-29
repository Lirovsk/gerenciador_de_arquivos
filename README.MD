# The main idea
This project was born due a lazynes of mine: I love startin a new project, but I hate losing time creating all the files and directories need to star programing. So I thought it would be a great idea to automate the hole process of creting the archives needed by saving predefined directories and then just tell the script what path to choose and the name of the program. 

Of course I want to create a robust solution, by robust I mean a program that can create not just a folder but also create a virtual enviroment, installing libraries and more.  

## Working principle
Although I'm already planning to change the way the program is constructed, for formal reasons I'll explain how it works because this project is also a portfolio. This program saves two diferent paths, one is to save scripts, the other is to save entire projects. 

The program currently have to main commands, one to save the paths and other to create the projects.

By having the paths pre saved, the program can create scripts or projects faster than manualy creating it. 

### commands
The commands are very intuitive, which means the config command is responsible for configurate the paths, the create command is responsible for create the files and so. But there are also some flags that can be used with these commands and this section is all about explainnig them.

#### {config}
The config command is responsible for running settings and stablish some constansts (Ex. the predefined path to scripts). to help the use of this program, some flags are related to it. 

--for-script(-fs): This flag tells the program that the config command is now setting (or changing) the variable responsible to save the path tied to the scripts. This flag does not need a value. It's own behavior set itself to true when the flag is used.

--for-projects(-fp): The same as the '--for-script' flag, but for projects. this flags tells the program the variable being used is the one tied to the projects.

--relative-path(-rp): This flags tells the program you are about to use a relative path. The start point of the relative path will always be the current work directory. This flag receive a string as a path (the format is directory/subdirectory/project_folder).

--absolute-path(-ap): It works similar to the previous flag, but in this case you are using an absolute path to tell the program where your directory is saved. It also receive a string as the argument

### {create-script}
The creat-script command tells the program to create a script on the designated path and open it in VSCODE. This command receive a string as value, this string is the name of the script to be created.

The command receive the name of the argument, create the file on the designated path, write a basic template then open it (in this order) in VScode. Before creating the file, the program ensures the path exists and is well setted.

### {create-project}
It works similar to the 'create-script' command but instead of create the file on the designated path, it creates the directory of the project first then create the files for the project.

The command first create the directory for the hole project, create the files (it create the main.py and the README.md), create git repository, change the name of the branch to main (recomended by GitHub) then open the folder on VScode.