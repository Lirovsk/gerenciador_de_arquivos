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
                
            case _:
                print("Invalid open area.")
        pass
    
    @staticmethod
    def open_project(project_name: str):
        pass  
    
    @staticmethod
    def open_script(script_name: str):
        pass

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
                pass
            
            case 'script':
                pass
    
    
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
                search_manager.search_project(args.search_name, args.search_all)
            
            case 'script':
                search_manager.search_script(args.search_name, args.search_all)
            
            case _:
                print("Invalid search area.")
    
    @staticmethod
    def search_project(search_name: str, search_all: bool):
        pass
    
    @staticmethod
    def search_script(search_name: str, search_all: bool):
        pass           

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
        pass
        
    
    @staticmethod
    def delete_script(script: str, force_delete: bool):
        pass


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
