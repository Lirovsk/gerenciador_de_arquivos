# The main idea
This project was born due a lazynes of mine: I love startin a new project, but I hate losing time creating all the files and directories need to star programing. So I thought it would be a great idea to automate the hole process of creting the archives needed by saving predefined directories and then just tell the script what path to choose and the name of the program. 

Of course I want to create a robust solution, by robust I mean a program that can create not just a folder but also create a virtual enviroment, installing libraries and more.  

## Working principle
Although I'm already planning to change the way the program is constructed, for formal reasons I'll explain how it works because this project is also a portfolio. This program saves two diferent paths, one is to save scripts, the other is to save entire projects. 

The program currently have to main commands, one to save the paths and other to create the projects.

By having the paths pre saved, the program can create scripts or projects faster than manualy creating it. 

### commands
The commands are very intuitive, which means the config command is responsible for configurate the paths, the create command is responsible for create the files and so. But there are also some flags that can be used with these commands and this section is all about explainnig them.

#### config
The config command is responsible for running settings and stablish some constansts (Ex. the predefined path to scripts). to help the use of this program, some flags are related to it. 

--for-script(-fs): This flag tells the program that the config command is now setting (or changing) the variable responsible to save the path tied to the scripts. This flag does not need a value. It's own behavior set itself to true when the flag is used.

--for-projects(-fp) The same as the '--for-script' flag, but for projects. this flags tells the program the variable being used is the one tied to the projects.

