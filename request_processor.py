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

    @log_execution
    @staticmethod
    def retrieve_config():
        
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
        return config
    
    @log_execution
    @staticmethod
    def set_nested_config(area_name:str, config_name:str, config_value:any):
        config = config_manager.retrieve_config()
        if area_name not in config:
            config[area_name] = {}
        config[area_name][config_name] = config_value
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)
    
    @log_execution
    @staticmethod
    def set_config(config_name:str, config_value:any, ident_value:int):
        config = config_manager.retrieve_config()
        config[config_name] = config_value
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=ident_value)
    
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
            
        config_manager.set_config(config_name='path', config_value=path_uri, ident_value=4)
        
    
    @staticmethod
    def set_project_open(args: dict):
        if args.config_to_set == 'files':
            config_to_set = 'open_files'
        else:
            config_to_set = 'open_git'
        
        value_to_set = args.value_to_set
        
        config_manager.set_nested_config(area_name='project', config_name=config_to_set, config_value=value_to_set)
            

    @staticmethod
    def set_project_extension(args: dict):
        extension_value = AsideTasks.normalize_extension(extension=args.value)
        
        config_manager.set_nested_config(area_name='project', config_name='default_extension', config_value=extension_value)


    @staticmethod
    def set_script_open(args:dict):
        config_to_set = 'open_files'
        value_to_set = args.value_to_set
        
        config_manager.set_nested_config(area_name='script', config_name=config_to_set, config_value=value_to_set)
        
        
    @staticmethod
    def set_script_extension(args:dict):
        extension_value = AsideTasks.normalize_extension(extension=args.value)
        
        config_manager.set_nested_config(area_name='script', config_name='default_extension', config_value=extension_value)
        

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
        """
        Opens a project in Visual Studio Code.
        Retrieves the configured project path from the config manager, constructs the full path
        to the specified project, and opens it in VS Code. Handles both directories and files.
        Args:
            project_name (str): The name of the project to open.
        Raises:
            ValueError: If the project path is not configured in the config file.
            ValueError: If the specified project does not exist in the configured project path.
        Returns:
            None
        """
        
        config = config_manager.retrieve_config()
        project_config = config.get('project', {})
        project_path = project_config.get('path')
        if not project_path:
            raise ValueError("Project path is not configured. Please set the project path before trying to open a project.")
        
        full_path = Path.from_uri(project_path) / project_name
        if not full_path.exists():
            raise ValueError(f"The specified project '{project_name}' does not exist in the configured project path.")
        
        if full_path.is_dir():
            subprocess.run(['code', full_path], shell=True)
        else:
            subprocess.run(['code', '', full_path], shell=True)  
    
    @staticmethod
    def open_script(script_name: str):
        """
        Opens a script file or directory in Visual Studio Code.
        Retrieves the configured script path from the configuration manager,
        constructs the full path to the specified script, validates its existence,
        and opens it in VS Code. Directories are opened directly, while files are
        opened in a new VS Code window.
        Args:
            script_name (str): The name of the script file or directory to open.
        Raises:
            ValueError: If the script path is not configured in the config file.
            ValueError: If the specified script does not exist in the configured path.
        Returns:
            None
        """
        
        config = config_manager.retrieve_config()
        script_config = config.get('script', {})
        script_path = script_config.get('path')
        if not script_path:
            raise ValueError("Script path is not configured. Please set the script path before trying to open a script.")
        
        full_path = Path.from_uri(script_path) / script_name
        if not full_path.exists():
            raise ValueError(f"The specified script '{script_name}' does not exist in the configured script path.")
        
        if full_path.is_dir():
            subprocess.run(['code', full_path], shell=True)
        else:
            subprocess.run(['code', '', full_path], shell=True)

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
        configs = config_manager.retrieve_config()
        path = configs.get('path', None)
        if not path:
            print("Path is not configured. Please set the path before trying to create a folder.")
            return

        # Create the folder
        path_usable = Path.from_uri(path)
        folder_path = path_usable / name
        projects_path = folder_path / "projects"
        scripts_path = folder_path / "scripts"
        
        folder_path.mkdir(parents=False, exist_ok=True)
        projects_path.mkdir(parents=False, exist_ok=True)
        scripts_path.mkdir(parents=False, exist_ok=True)
        

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
        """
        Search for projects or items in the configured project directory.
        Args:
            search_name (str): The name or partial name of the project/item to search for.
                              Ignored if search_all is True.
            search_all (bool): If True, displays all items in the project directory.
                              If False, searches for items matching search_name.
        Raises:
            ValueError: If the project path is not configured in the config file.
            ValueError: If the configured project path does not exist.
        Returns:
            None: Prints the names of found items to stdout.
        Note:
            - When search_all is True, all items in the project directory are listed.
            - When search_all is False, only items containing search_name are listed.
            - If no items match the search criteria, a message is printed to inform the user.
        """
        
        config = config_manager.retrieve_config()
        project_config = config.get('project', {})
        project_path = project_config.get('path')
        if not project_path:
            raise ValueError("Project path is not configured. Please set the project path before trying to search for a project.")
        
        full_path = Path.from_uri(project_path)
        if not full_path.exists():
            raise ValueError("The configured project path does not exist. Please check the project path configuration.")
        
        if search_all:
            items = list(full_path.iterdir())
            for item in items:
                item_tuple = item.parts
                print(item_tuple[-1])
                            
        else:
            found_items = [item for item in list(full_path.iterdir()) if search_name in item.name]
            for items in found_items:
                item_tuple = items.parts
                print(item_tuple[-1])
                
            if found_items == []:
                print(f"No items found matching '{search_name}' in the configured project path.")
    
    @staticmethod
    def search_script(search_name: str, search_all: bool):
        """
        Search for scripts in the configured script directory.
        This function searches for script files in the path specified in the configuration.
        It can either list all scripts or search for scripts matching a specific name.
        Args:
            search_name (str): The name or partial name of the script to search for.
                              Ignored if search_all is True.
            search_all (bool): If True, lists all scripts in the configured directory.
                              If False, searches for scripts matching search_name.
        Raises:
            ValueError: If the script path is not configured in the configuration file.
            ValueError: If the configured script path does not exist.
        Returns:
            None: Prints the names of found scripts to the console.
        Note:
            - If search_all is False and no items are found matching search_name,
              a message is printed to inform the user.
            - Only the last part of the file path (filename) is printed.
        """
        
        config = config_manager.retrieve_config()
        script_config = config.get('script', {})
        script_path = script_config.get('path')
        if not script_path:
            raise ValueError("Script path is not configured. Please set the script path before trying to search for a script.")
        
        full_path = Path.from_uri(script_path)
        if not full_path.exists():
            raise ValueError("The configured script path does not exist. Please check the script path configuration.")
        
        if search_all:
            items = list(full_path.iterdir())
            for item in items:
                item_tuple = item.parts
                print(item_tuple[-1])
                
        else:
            found_items = [item for item in list(full_path.iterdir()) if search_name in item.name]
            for items in found_items:
                item_tuple = items.parts
                print(item_tuple[-1])
                
            if found_items == []:
                print(f"No items found matching '{search_name}' in the configured script path.")           

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
        
        if args.delete_area == 'project':
            delete_manager.delete_project(args.delete_name, args.force_delete)
        elif args.delete_area == 'script':
            delete_manager.delete_script(args.delete_name, args.force_delete)
        else:
            print("Invalid delete area.")
            
    @staticmethod
    def delete_project(project: str, force_delete: bool):
        """
        Delete a project directory from the configured project path.
        Args:
            project (str): The name of the project to delete.
            force_delete (bool): If True, delete the project without confirmation.
                                If False, prompt the user for confirmation before deletion.
        Raises:
            ValueError: If the project path is not configured in the config file.
            ValueError: If the specified project does not exist in the configured project path.
        Returns:
            None
        Notes:
            - If force_delete is False, the user will be prompted to confirm the deletion.
            - User can confirm with 'yes' or 'y' (case-insensitive).
            - This action cannot be undone as the entire project directory will be removed.
            - Prints a success message upon successful deletion.
            - Prints a cancellation message if the user declines the confirmation prompt.
        """
        
        config = config_manager.retrieve_config()
        project_config = config.get('project', {})
        project_path = project_config.get('path')
        if not project_path:
            raise ValueError("Project path is not configured. Please set the project path before trying to delete a project.")
        full_path = Path.from_uri(project_path) / project
        if not full_path.exists():
            raise ValueError(f"The specified project '{project}' does not exist in the configured project path.")
        
        if force_delete:
            shutil.rmtree(full_path)
        else:
                confirmation = input(f"Are you sure you want to delete the project '{project}'? This action cannot be undone. (yes/no): ")
                if confirmation.lower() in ['yes', 'y']:
                    shutil.rmtree(full_path)
                    print (f"Project '{project}' has been deleted.")
                else:
                    print("Project deletion cancelled.")
        
    
    @staticmethod
    def delete_script(script: str, force_delete: bool):
        """
        Delete a script from the configured script path.
        Args:
            script (str): The name of the script to delete.
            force_delete (bool): If True, delete the script without confirmation.
                                If False, prompt the user for confirmation before deletion.
        Raises:
            ValueError: If the script path is not configured or if the specified script does not exist.
        Returns:
            None
        Prints a confirmation message after successful deletion, or a cancellation message if the user declines.
        """
        
        config = config_manager.retrieve_config()
        script_config = config.get('script', {}) 
        script_path = script_config.get('path')
        if not script_path:
            raise ValueError("Script path is not configured. Please set the script path before trying to delete a script.")
        
        full_path = Path.from_uri(script_path) / script
        if not full_path.exists():
            raise ValueError(f"The specified script '{script}' does not exist in the configured script path.")
        
        if force_delete:
            full_path.unlink()
        else:
            confirmation = input(f"Are you sure you want to delete the script '{script}'? This action cannot be undone. (yes/no): ")
            if confirmation.lower() in ['yes', 'y']:
                full_path.unlink()
                print (f"Script '{script}' has been deleted.")
            else:
                print("Script deletion cancelled.")


class AsideTasks:

    

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
