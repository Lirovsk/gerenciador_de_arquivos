from logging import config
from pathlib import Path, WindowsPath
import json
import os
import subprocess
from functools import wraps
import shutil

CONFIG_FILE = "file_manager_config.json"
DATA_FILE = "file_manager_data.json"

def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try: 
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
        
        except FileNotFoundError:
            print("\nConfig file not found. Creating a new one...\n")
            with open(CONFIG_FILE, 'w') as file:
                json.dump({}, file)
        return func(*args, **kwargs)
    return wrapper

class config_manager:
    
    
    @staticmethod
    def save_config(args: dict):
        match args.config_action:
            case "set-path":
                config_manager.set_path(args)
            
            case "set-project-open":
                config_manager.set_project_open(args)
            
            case "set-project-extension":
                config_manager.set_project_extension(args)
            
            case "set-script-open":
                config_manager.set_script_open(args)
            
            case "set-script-extension":
                config_manager.set_script_extension(args)
            
    
    @staticmethod
    def set_path(args: dict):
        path_value = args.value
        absolute_path = args.absolute_path
        
        path_uri, path_object = AsideTasks.normalize_path(path_value=path_value, absolute_path=absolute_path)
        
        
        if not path_object.exists():
            TEXT= f"The provided path '{path_uri}' does not exist. \n \nDo you want to create it? (yes/no): "
            answer = input(TEXT)
            match answer.lower():
                case "yes" | "y":
                    path_object.mkdir(parents=True)
                
                case "no" | "n":
                    print("Path creation cancelled. Please provide a valid path.")
                    return
                
                case _:
                    print("Invalid answer, please answer with 'yes' or 'no'.")
                    return
            
        AsideTasks.set_config(config_name='path', config_value=path_uri, ident_value=4)
        
    
    @staticmethod
    def set_project_open(args: dict):
        if args.config_to_set == 'files':
            config_to_set = 'open_files'
        else:
            config_to_set = 'open_git'
        
        value_to_set = args.value_to_set
        
        AsideTasks.set_nested_config(area_name='project', config_name=config_to_set, config_value=value_to_set)
            

    @staticmethod
    def set_project_extension(args: dict):
        extension_value = AsideTasks.normalize_extension(extension=args.value)
        
        AsideTasks.set_nested_config(area_name='project', config_name='default_extension', config_value=extension_value)


    @staticmethod
    def set_script_open(args:dict):
        config_to_set = 'open_files'
        value_to_set = args.value_to_set
        
        AsideTasks.set_nested_config(area_name='script', config_name=config_to_set, config_value=value_to_set)
        
        
    @staticmethod
    def set_script_extension(args:dict):
        extension_value = AsideTasks.normalize_extension(extension=args.value)
        
        AsideTasks.set_nested_config(area_name='script', config_name='default_extension', config_value=extension_value)


class open_manager:
    
    @staticmethod
    def open(args: dict):
        """
        Opens a file or project based on the specified area.
        Args:
            args (dict): A dictionary containing:
                - open_area (str): The type of area to open. Can be 'project' or 'script'.
                - file_to_open (str): The path or identifier of the file/project to open.
        Raises:
            Prints an error message if open_area is not 'project' or 'script'.
        Returns:
            None
        """
        
        match args.open_area:
            case 'project':
                open_manager.open_project(args.file_to_open)
                
            case 'script':
                open_manager.open_script(args.file_to_open)

    
    @staticmethod
    def open_project(project_name: str):
        results = open_manager.search_for_file(file_area="projects", file_name=project_name)
        
        match len(results):
            case 0:
                print(f"No project found with the name '{project_name}'.")
                return
            
            case 1:
                project_path, _, _ = results[0]
                subprocess.run(["code", str(project_path)], shell=True)
                return
            
            case _:
                for i in range(len(results)):
                    project_path, direction, file_name = results[i]
                    print(f"{direction}/{file_name} [{i+1}]")
                    
                choice = input("which directory to open? (Enter the number corresponding to the directory): ")
                
                try:
                    choice_index = int(choice) - 1
                    project_path, _, _ = results[choice_index]
                    subprocess.run(["code", str(project_path)], shell=True)
                except (ValueError, IndexError):
                    print("Invalid choice. Please enter a valid number corresponding to the directory.")
                    return
                
                    
    @staticmethod
    def open_script(script_name: str):
        results = open_manager.search_for_file(file_area="scripts", file_name=script_name)
        
        match len(results):
            case 0:
                print(f"No script found with the name '{script_name}'.")
                return
            
            case 1:
                script_path, _, _ = results[0]
                subprocess.run(["code", str(script_path)], shell=True)
                return
            
            case _:
                for i in range(len(results)):
                    script_path, direction, file_name = results[i]
                    print(f"{direction}/{file_name} [{i+1}]")
                    
                choice = input("which directory to open? (Enter the number corresponding to the directory): ")
                
                try:
                    choice_index = int(choice) - 1
                    script_path, _, _ = results[choice_index]
                    subprocess.run(["code", str(script_path)], shell=True)
                except (ValueError, IndexError):
                    print("Invalid choice. Please enter a valid number corresponding to the directory.")
                    return
    
    
    @staticmethod
    def search_for_file(file_area: str, file_name: str):
        config = AsideTasks.retrieve_config()
        path = Path.from_uri(config.get('path', None))
        
        if not path:
            print("Path is not configured. Please set the path before trying to open a file.")
            return
        
        directory_list = []
        
        for language_folder in path.iterdir():
            for area_folder in language_folder.iterdir():
                if area_folder.name == file_area:
                    for file in area_folder.iterdir():
                        if file_name in file.name:
                            tuple_to_return = (file, f"{language_folder.name}/{area_folder.name}", file.name)
                            directory_list.append(tuple_to_return)
        
        return directory_list
                            

class create_manager:
    
    @staticmethod
    def create(args: dict):
        """
        Manages the creation of new projects, scripts, or folders based on the specified area.
        """
        match args.create_area:
            case 'folder':
                create_manager.creator_of_folder(args)
            
            case 'project':
                create_manager.create_project(args)
            
            case 'script':
                create_manager.create_script(args)
    
    
    @staticmethod
    def creator_of_folder(args: dict):
        name = args.create_name
        
        result = AsideTasks.search_for_name_by_name(name)
        if result:
            create_manager.create_folder(name)
        
        else:
            create_manager.create_folder("others")
        
    
    @staticmethod
    def create_folder(name: str):
        configs = AsideTasks.retrieve_config()
        path = configs.get('path', None)
        if not path:
            print("Path is not configured. Please set the path before trying to create a folder.")
            return

        # Create the folder
        path_ = Path.from_uri(path)
        directory_list = AsideTasks.directory_definer(name=name, path=path_)
        
        for path in directory_list:
            path.mkdir(exist_ok=True, parents=True)
            
            
    @staticmethod
    def create_project(args: dict):
        name = args.create_name
        configs = AsideTasks.retrieve_config()
        path = configs.get('path', None)
        path = Path.from_uri(path)
        
        project_extension = args.file_extension if args.file_extension is not None else configs.get('project', {}).get('default_extension', ".py")
        project_extension = AsideTasks.normalize_extension(extension=project_extension)
        
        project_open_files = args.open_files if args.open_files is not None else configs.get('project', {}).get('open_files', True)
        project_open_git = args.open_git if args.open_git is not None else configs.get('project', {}).get('open_git', True)
        
        if not path:
            print("Path is not configured. Please set the path before trying to create a project.")
            return
        
        result = AsideTasks.search_for_extension(project_extension)
        
        if result:
            create_manager.create_folder(result)
            comment = AsideTasks.search_for_comment(result)
            
            main_path = path / result / "projects" / name / f"main{project_extension}"
            readme_path = path / result /"projects" / name / "README.md"
            folder_path = path / result / "projects" / name
            
            
            try:
                main_path.parent.mkdir(parents=True)
            except FileExistsError as e:
                print(f"the directory {name} already exists on the folder '{result}'. Please choose a different name or delete the existing directory.")
                return
            except Exception as e:
                print(f"An error occurred while creating the directory: {e}")
                return
            finally:
                main_path.touch()
                main_path.write_text(f"{comment} This is the main file for the {name} project.\n")
                readme_path.write_text(f"# {name}\n\nThis is the README file for the {name} project.\n\n#### Created by file_manager.\n")
                
            if project_open_git:
                            gitignore_path = folder_path / ".gitignore"
                            gitignore_path.touch()
                            gitignore_path.write_text("# Ignore Python bytecode files\n__pycache__/\n*.py[cod]\n\n# Ignore virtual environment directories\nenv/\nvenv/\n\n# Ignore log files\n*.log\n\n# Ignore OS-specific files\n.DS_Store\nThumbs.db\n")
                            subprocess.run(["git", "init"], cwd=folder_path, shell=True)
                            subprocess.run(["git", "branch", "-M", "main"], cwd=folder_path, shell=True)
            
            if project_open_files:
                subprocess.run(["code", str(folder_path)], shell=True)
        else:
            create_manager.create_folder("others")
            
            main_path = path / "others" / "projects" / name / f"main{project_extension}"
            readme_path = path / "others" / "projects" / name / "README.md"
            folder_path = path / "others" / "projects" / name
            try:
                main_path.parent.mkdir(parents=True)
            except FileExistsError as e:
                print(f"the directory {name} already exists on the folder 'others'. Please choose a different name or delete the existing directory.")
                return
            except Exception as e:
                print(f"An error occurred while creating the directory: {e}")
                return
            finally:
                main_path.touch()
                readme_path.write_text(f"# {name}\n\nThis is the README file for the {name} project.\n\n#### Created by file_manager.\n")
            
            if project_open_git:
                gitignore_path = folder_path / ".gitignore"
                gitignore_path.touch()
                subprocess.run(["git", "init"], cwd=folder_path, shell=True)
                subprocess.run(["git", "branch", "-M", "main"], cwd=folder_path, shell=True)

            if project_open_files:      
                subprocess.run(["code", str(folder_path)], shell=True)
            
        
    @staticmethod
    def create_script(args: dict):
        name = args.create_name
        configs = AsideTasks.retrieve_config()
        
        open_file = args.open_files if args.open_files is not None else configs.get('script', {}).get('open_files', True)
        extension = args.file_extension if args.file_extension is not None else configs.get('script', {}).get('default_extension', ".py")
        extension = AsideTasks.normalize_extension(extension=extension)
        
        result = AsideTasks.search_for_extension(extension)
        
        if result:
            create_manager.create_folder(result)
            script_path = Path.from_uri(configs.get('path')) / result / "scripts" / f"{name}{extension}"
            script_path.touch()
            script_path.write_text(f"{AsideTasks.search_for_comment(result)} This is the {name} script.\n")
        else:
            create_manager.create_folder("others")
            script_path = Path.from_uri(configs.get('path')) / "others" / "scripts" / f"{name}{extension}"
            script_path.touch()
        
        if open_file:
            subprocess.run(["code", str(script_path)], shell=True)


class search_manager:
    @staticmethod
    def search(args: dict):
        """
        Search for files or scripts based on the specified search area.
        Args:
            args (dict): A dictionary containing search parameters with the following keys:
                - search_area (str): The area to search in. Valid values are 'project' or 'script'.
                - search_name (str): The name or pattern to search for.
                - search_all (bool): Whether to search all occurrences or just the first match.
        Raises:
            Prints an error message if search_area is not 'project' or 'script'.
        """
        
        match args.search_area:
            case 'project':
                search_manager.search_project(args.search_name)
            
            case 'script':
                search_manager.search_script(args.search_name)
                
            case 'for_all':
                search_manager.search_all(search_area=None)
            
            case _:
                print("Invalid search area.")
    
    
    @staticmethod
    def search_all(search_area: str, search_name: str | None = None):
        config = AsideTasks.retrieve_config()
        path = Path.from_uri(config.get('path', None))
        
        if search_area is not None:
            for language_folder in path.iterdir():
                for area_folder in language_folder.iterdir():
                    if len(list(area_folder.iterdir())) != 0 and area_folder.name == search_area:
                        print(f"{language_folder.name}/{area_folder.name}/")
                        
                        for file in area_folder.iterdir():
                            if search_name is not None and search_name in file.name:
                                print(f"      {file.name}")
                            
                            if search_name is None:
                                print(f"      {file.name}")
                        
                        print("\n", end="")
            
        else: 
            for language_folder in path.iterdir():
                for area_folder in language_folder.iterdir():
                    if len(list(area_folder.iterdir())) != 0:
                        print(f"{language_folder.name}/{area_folder.name}/")
                        
                        for file in area_folder.iterdir():
                            if search_name is not None and search_name in file.name:
                                print(f"      {file.name}")
                            
                            if search_name is None:
                                print(f"      {file.name}")
                            
                        print("\n", end="")
        return 
                        
    
    @staticmethod
    def search_project(search_name: str | None):
        if search_name is None:
            search_manager.search_all(search_area='projects')
        
        else:
            search_manager.search_all(search_area='projects', search_name=search_name)
        
    
    @staticmethod
    def search_script(search_name: str | None):
        if search_name is None:
            search_manager.search_all(search_area='scripts')
        else:
            search_manager.search_all(search_area='scripts', search_name=search_name)          

class delete_manager:
    @staticmethod
    def delete(args: dict):
        """
        Delete a project or script based on the specified delete area.
        Args:
            args (dict): A dictionary containing deletion parameters with the following keys:
                - delete_area (str): The type of entity to delete ('project' or 'script').
                - delete_name (str): The name of the project or script to delete.
                - force_delete (bool): Whether to force deletion without confirmation.
        Raises:
            None: Prints an error message if delete_area is not 'project' or 'script'.
        Returns:
            None
        """
        
        match args.delete_area:
            case 'project':
                delete_manager.delete_project(args.delete_name, args.force_delete)
            
            case 'script':
                delete_manager.delete_script(args.delete_name, args.force_delete)
            
            case _:
                print("Invalid delete area.")
                
            
    @staticmethod
    def delete_project(project: str, force_delete: bool):
        results = open_manager.search_for_file(file_area="projects", file_name=project)
        
        match len(results):
            case 0:
                print(f"No project found with the name '{project}'.")
                return
            
            case 1:
                project_path, _, _ = results[0]
                if force_delete:
                    shutil.rmtree(project_path)
                    print(f"Project '{project}' has been deleted.")
                else:
                    confirmation = input(f"Are you sure you want to delete the project '{project}'? (yes/no): ")
                    if confirmation.lower() in ['yes', 'y']:
                        shutil.rmtree(project_path)
                        print(f"Project '{project}' has been deleted.")
                    else:
                        print("Deletion cancelled.")
                
            case _:
                for i in range(len(results)):
                    project_path, direction, file_name = results[i]
                    print(f"{direction}/{file_name} [{i+1}]")
                    
                choice = input("which directory to delete? (Enter the number corresponding to the directory): ")
                
                try:
                    choice_index = int(choice) - 1
                    project_path, _, name = results[choice_index]
                    if force_delete:
                        shutil.rmtree(project_path)
                        print(f"Project '{name}' has been deleted.")
                    else:
                        confirmation = input(f"Are you sure you want to delete the project '{name}'? (yes/no): ")
                        if confirmation.lower() in ['yes', 'y']:
                            shutil.rmtree(project_path)
                            print(f"Project '{name}' has been deleted.")
                        else:
                            print("Deletion cancelled.")
                except (ValueError, IndexError):
                    print("Invalid choice. Please enter a valid number corresponding to the directory.")
                    return
        
    
    @staticmethod
    def delete_script(script: str, force_delete: bool):
        results = open_manager.search_for_file(file_area="scripts", file_name=script)
        
        match len(results):
            case 0:
                print(f"No script found with the name '{script}'.")
                return
            
            case 1:
                script_path, _, _ = results[0]
                if force_delete:
                    script_path.unlink()
                    print(f"Script '{script}' has been deleted.")
                else:
                    confirmation = input(f"Are you sure you want to delete the script '{script}'? (yes/no): ")
                    if confirmation.lower() in ['yes', 'y']:
                        script_path.unlink()
                        print(f"Script '{script}' has been deleted.")
                    else:
                        print("Deletion cancelled.")
                
            case _:
                for i in range(len(results)):
                    script_path, direction, file_name = results[i]
                    print(f"{direction}/{file_name} [{i+1}]")
                    
                choice = input("which directory to delete? (Enter the number corresponding to the directory): ")
                
                try:
                    choice_index = int(choice) - 1
                    script_path, _, name = results[choice_index]
                    if force_delete:
                        script_path.unlink()
                        print(f"Script '{name}' has been deleted.")
                    else:
                        confirmation = input(f"Are you sure you want to delete the script '{name}'? (yes/no): ")
                        if confirmation.lower() in ['yes', 'y']:
                            script_path.unlink()
                            print(f"Script '{name}' has been deleted.")
                        else:
                            print("Deletion cancelled.")
                except (ValueError, IndexError):
                    print("Invalid choice. Please enter a valid number corresponding to the directory.")
                    return


class AsideTasks:

    @log_execution
    @staticmethod
    def retrieve_config():

        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
        return config

    @log_execution
    @staticmethod
    def set_nested_config(area_name:str, config_name:str, config_value:any):
        config = AsideTasks.retrieve_config()
        if area_name not in config:
            config[area_name] = {}
            config[area_name][config_name] = config_value
        else:
            config[area_name][config_name] = config_value

        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)


    @log_execution
    @staticmethod
    def set_config(config_name: str, config_value: any, ident_value: int):
        config = AsideTasks.retrieve_config()
        config[config_name] = config_value
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=ident_value)
            

    @staticmethod
    def normalize_path(path_value: str, absolute_path: bool):

        """
        Normalize a file path to a standardized URI format with validation.
        This function converts a given path string into a normalized URI representation
        and returns both the URI and a Path object for further validation or processing.
        Args:
            path_value (str): The path to normalize. Can be either an absolute path
                (with drive letter on Windows) or a relative path.
                absolute_path (bool): If True, treats path_value as an absolute path.
                If False, treats it as a relative path and prepends the current
                working directory.
        Returns:
            tuple[str, Path]: A tuple containing:
                - full_path (str): The normalized path as a URI string.
                - path_check (Path): A Path object representing the full path
                    for validation purposes.
        Raises:
            ValueError: On Windows systems, if absolute_path is True and the
                path_value does not include a drive letter (e.g., 'C:').
        Note:
            - On Windows, absolute paths must include a drive letter.
            - On non-Windows systems, relative paths are automatically prefixed
                with '/' if not already present.
            - The function uses the current working directory as the base for
                relative paths.
        """

        if absolute_path:
            if os.name == 'nt': # Windows
                if path_value[1] != ':':
                    raise ValueError("On Windows, an absolute path must include a drive letter (e.g., C:). Please provide a valid absolute path.")

                path_objet = Path(path_value)
                path_check = path_objet
                full_path = path_objet.as_uri()
        else :
            if path_value[0] != '/':
                path_value = '/' + path_value
                print(path_value)
                full_path = Path.cwd().as_uri() + path_value
                path_check = Path.from_uri(full_path)
        return full_path, path_check
    
    
    @staticmethod
    def directory_definer(name: str, path: Path):
        projects_path = path / name / "projects"
        scripts_path = path / name / "scripts" 
        
        return [projects_path, scripts_path]

    @staticmethod
    def search_for_extension(extension):
        with open(DATA_FILE, 'r') as data_file:
            """Returns the programming language associated with a given file extension from a JSON data file."""
            data = json.load(data_file)
            languages = data.get('languages', {})
            result = next((lang for lang in languages if languages[lang] == extension), None)
            return result

    @staticmethod
    def search_for_name(name):
        with open(DATA_FILE, 'r') as data_file:
            """Returns the file extension associated with a given programming language name from a JSON data file."""
            data = json.load(data_file)
            languages = data.get('languages', {})
            result = languages.get(name, None)
            return result

    @staticmethod
    def search_for_name_by_name(name):
        with open(DATA_FILE, 'r') as data_file:
            """Returns the programming language name associated with a given programming language name from a JSON data file."""
            data = json.load(data_file)
            languages = data.get('languages', {})
            result = next((lang for lang in languages if lang.lower() == name.lower()), None)
            return result
        
    @staticmethod
    def search_for_comment(language_name: str):
        with open(DATA_FILE, 'r') as data_file:
            """Returns the comment syntax associated with a given programming language name from a JSON data file."""
            data = json.load(data_file)
            languages = data.get('comments', {})
            result = languages.get(language_name, None)
            return str(result)

    @staticmethod
    def normalize_extension(extension):
        """
        Normalize a file extension to ensure it starts with a dot.
        Args:
            extension (str): The file extension to normalize.
        Returns:
            str: The normalized file extension, starting with a dot.
        Note:
            - If the input extension already starts with a dot, it is returned unchanged.
            - If the input extension does not start with a dot, a dot is prepended.
        """
        if not extension.startswith('.'):
            return '.' + extension
        return extension
