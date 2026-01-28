import argparse
from pathlib import Path
import json
import subprocess

# CONTANTS

CONFIG_FILE = "file_manager_config.json"


parser = argparse.ArgumentParser(prog="file_manager",
                                    description="A simple manager to create and manage python files easily.")

# ====== Creating subparsers for different commands ======
subparsers = parser.add_subparsers(dest="command", required=True, help="Commands to use")


# ++++ Subparser for configuration ++++
config_parser = subparsers.add_parser("config", help="Configure the file manager")

# arguments used by the config command
config_parser.add_argument("--relative-path", "-rp", type=str, help="Use a relative path to be the default for creating the files", default=None)

config_parser.add_argument("--absolute-path", "-ap", nargs="?", type=str, help="Use an absolute path to be the default for creating the files", const= Path.home().as_uri())

config_parser.add_argument("--for-scripts", "-fs", action="store_true",default=False, help="Configure the file manager to create files for scripts. Tells the file manager the" \
" path saved is to create scripts")

config_parser.add_argument("--for-projects", "-fp", action="store_true", default=False, help="Configure the file manager to create files for projects. Tells the file manager the" \
" path saved is to create projects")


# ++++ Subparser for creating a script ++++
create_script_parser = subparsers.add_parser("create-script", help="Create a new python script file on the area designated for scripts")

# arguments used by the create-script command
create_script_parser.add_argument("script_name", type=str, help="Name of the script to be created")


# ++++ Subparser for creating a project ++++
create_project_parser = subparsers.add_parser("create-project", help="Create a new python project folder on the area designated for projects")

# arguments used by the create-project command
create_project_parser.add_argument("project_name", type=str, help="Name of the project to be created")



args = parser.parse_args()

# ========== Section responsible for configuration ===========
if args.command == "config":
    print("\n\n" + args + "\n\n") # Line used for debugging purposes

    # the following line ensure the user specifies only one of the two options
    if ((args.for_scripts == False) and (args.for_projects == False)) or ((args.for_scripts == True) and (args.for_projects == True)):
        print("\nYou need to specify if the path is for scripts or for projects. Use --for-scripts OR --for-projects\n")
        exit(1)
    else:
        # configuring for scripts
        if args.for_scripts == True:
            # this if normalize the user entry for relative paths ensuring the first character is a "/" and making it able to be concatenated
            if args.relative_path is not None:
                if args.relative_path[0] != "/":
                    args.relative_path = "/" + args.relative_path
                
                # with the normalized relative path we can create the full path by concatenating with the current working directory
                full_path = Path.cwd().as_uri() + args.relative_path
                resolved_path = Path.from_uri(full_path)
            else: 
                resolved_path = Path(args.absolute_path)

            # checking if the path created is a valid directory
            if not resolved_path.is_dir():
                print("The relative path you provided does not exist. Please create the directory first.")
                exit(1)
            else:
                # the following structure is used to ensure that if the config file does not exist it is created with an empty dictionary
                try: 
                    with open(CONFIG_FILE, "r") as config_file:
                        existing_config = json.load(config_file)
                except FileNotFoundError:
                    with open(CONFIG_FILE, "w") as config_file:
                        json.dump({}, config_file)
                finally:
                    with open(CONFIG_FILE, "r") as config_file:
                        existing_config = json.load(config_file)

                    existing_config["path for scripts"] = resolved_path.as_uri()
                    with open(CONFIG_FILE, "w") as config_file:
                        json.dump(existing_config, config_file)   
        # configuring for projects            
        else:
            if args.relative_path is not None:
                if args.relative_path[0] != "/":
                    args.relative_path = "/" + args.relative_path
                
                full_path = Path.cwd().as_uri() + args.relative_path
                resolved_path = Path.from_uri(full_path)
            else: 
                resolved_path = Path(args.absolute_path)

            # checking if the path created is a valid directory
            if not resolved_path.is_dir():
                print("The relative path you provided does not exist. Please create the directory first.")
                exit(1)
            else:
                # the following structure is used to ensure that if the config file does not exist it is created with an empty dictionary
                try: 
                    with open(CONFIG_FILE, "r") as config_file:
                        existing_config = json.load(config_file)
                except FileNotFoundError:
                    with open(CONFIG_FILE, "w") as config_file:
                        json.dump({}, config_file)
                finally:
                    with open(CONFIG_FILE, "r") as config_file:
                        existing_config = json.load(config_file)
                    
                    existing_config["path for projects"] = resolved_path.as_uri()
                    with open(CONFIG_FILE, "w") as config_file:
                        json.dump(existing_config, config_file)

# ========== Section responsible for creating scripts and projects ===========
    
if args.command == "create-script":
    print(f"Creating script: {args.script_name}")
    try:
        with open(CONFIG_FILE, "r") as config_file:
            existing_config = json.load(config_file)
    except FileNotFoundError:
        print("You need to configure the file manager before creating scripts or projects. Use the config command.")
        exit(1)
    
    path_to_use = Path.from_uri(existing_config["path for scripts"])
    if path_to_use.is_dir() == False:
        print("The path configured for scripts is not a valid directory. Please check your configuration.")
        exit(1)
    
    path_to_use = path_to_use / f"{args.script_name}.py"
    with open(path_to_use, "w") as script_file:
        script_file.write(f"# Script: {args.script_name}\n\n")
        script_file.write("def main():\n")
        script_file.write("    pass\n\n")
        script_file.write("if __name__ == '__main__':\n")
        script_file.write("    main()\n")
    
    command = ["code", str(path_to_use)]
    try:
        answer = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while opening the script in VS Code:")
        print(e.stderr)
        exit(1)
    


if args.command == "create-project":
    print(f"Creating project: {args.project_name}")
    try:
        with open(CONFIG_FILE, "r") as config_file:
            existing_config = json.load(config_file)
    except FileNotFoundError:
        print("You need to configure the file manager before creating scripts or projects. Use the config command.")
        exit(1)

    path_to_use = Path.from_uri(existing_config["path for projects"])
    path_to_use = path_to_use / f"{args.project_name}"
    path_to_use.mkdir(parents=True, exist_ok=True)
    
    path_to_main = path_to_use / "main.py"
    with open(path_to_main, "w") as main_file:
        main_file.write(f"# Project: {args.project_name}\n\n")
        main_file.write("def main():\n")
        main_file.write("    pass\n\n")
        main_file.write("if __name__ == '__main__':\n")
        main_file.write("    main()\n")
    
    path_to_README = path_to_use / "README.md"
    with open(path_to_README, "w") as readme:
        readme.write(f"# {args.project_name}\n\n")

    command = ["git", "init"]
    try:
        answer = subprocess.run(command, cwd=path_to_use, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while initializing the git repository:")
        print(e.stderr)
        exit(1)
    
    command = ["git", "branch", "-M", "main"]
    try:
        answer = subprocess.run(command, cwd=path_to_use, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while renaming the default branch to main:")
        print(e.stderr)
        exit(1)

    command = ["code", str(path_to_use)]
    try:
        answer = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while opening the project in VS Code:")
        print(e.stderr)
        exit(1)
    
