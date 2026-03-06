from logging import config
from pathlib import Path, WindowsPath
import json
import os
import subprocess
from functools import wraps
import shutil

CONFIG_FILE = "file_manager_config.json"

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
    def set_config(config:dict):
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)
    
    @staticmethod
    def save_config(args: dict):
        """
        Save configuration settings based on the specified action.
        This function processes various configuration actions for project and script settings,
        including paths, extensions, and open status flags. It retrieves the current configuration,
        updates it with the provided values, and persists the changes.
        Args:
            args (dict): A dictionary containing configuration parameters with the following keys:
                - config_action (str): The action to perform. Supported values:
                    - 'set-project-path': Set the project directory path
                    - 'set-project-extension': Set the file extension filter for projects
                    - 'set-project-open': Set whether the project should be opened (boolean string)
                    - 'set-script-path': Set the script directory path
                    - 'set-script-open': Set whether the script should be opened (boolean string)
                    - 'set-script-extension': Set the file extension filter for scripts
                - value (str): The value to set for the configuration
                - config_to_set (str): The specific config key to update (used for open flags)
        Returns:
            None
        Raises:
            Prints "Invalid config action." message if an unsupported config_action is provided.
        Note:
            Boolean string values ('true'/'false') are converted to Python boolean types
            for open status configurations.
        """
        
        match args.config_action:
            case 'set-project-path':
                config_manager.save_project_config(args)    
                
            
            case 'set-project-extension':
                config = config_manager.retrieve_config()
                config = AsideTasks.create_config_if_none(config, 'project')
                config['project']['extension'] = args.value
                config_manager.set_config(config)
                    
                pass
            
            case 'set-project-open':
                config = config_manager.retrieve_config()
                config = AsideTasks.create_config_if_none(config, 'project')
                if args.value.lower() == 'true':
                    args.value = True
                else:
                    args.value = False
                config['project'][args.config_to_set] = args.value
                config_manager.set_config(config)
            
            case 'set-script-path':
                config_manager.save_script_config(args)
            
            case 'set-script-open':
                config = config_manager.retrieve_config()
                config = AsideTasks.create_config_if_none(config, 'script')
                if args.value.lower() == 'true':
                    args.value = True
                else:
                    args.value = False
                config['script'][args.config_to_set] = args.value
                config_manager.set_config(config)
            
            case 'set-script-extension':
                config = config_manager.retrieve_config()
                config = AsideTasks.create_config_if_none(config, 'script')
                config['script']['extension'] = args.value
                config_manager.set_config(config)
            
            case _:
                print("Invalid config action.")
        pass
    
    @staticmethod
    def save_project_config(args: dict):
        """
        Save and initialize project configuration settings.
        Saves the project path to the configuration manager and initializes default
        project settings if they are not already set (git support, open files tracking,
        and file extension filter).
        Args:
            args (dict): A dictionary containing:
                - value (str): The project path value to save
                - absolute_path (str): The absolute path of the project
        Returns:
            None
        Side Effects:
            - Saves the project path to the configuration manager
            - Initializes 'git', 'open_files', and 'extension' settings if not present
            - Updates the configuration manager with the modified config
        """
        
        config_manager.save_path('project', 'path', args.value, args.absolute_path)
                
        config = config_manager.retrieve_config()
                
        AsideTasks.set_if_none(config['project'], 'git', True)
        AsideTasks.set_if_none(config['project'], 'open_files', True)
        AsideTasks.set_if_none(config['project'], 'extension', '.py')                
        config_manager.set_config(config)
        
    @staticmethod
    def save_script_config(args: dict): 
        """
        Save the script configuration with the provided arguments.
        This function updates the script configuration by setting the script path,
        and ensures default values are set for 'open_files' and 'extension' options.
        Args:
            args (dict): A dictionary containing:
                - value (str): The script path value to be saved.
                - absolute_path (str): The absolute path of the script.
        Returns:
            None
        Side Effects:
            - Saves the script path to the configuration manager.
            - Retrieves the current configuration.
            - Sets 'open_files' to True if not already defined in script config.
            - Sets 'extension' to '.py' if not already defined in script config.
            - Updates the configuration manager with the modified config.
        """
         
        config_manager.save_path('script', 'path', args.value, args.absolute_path)
                
        config = config_manager.retrieve_config()
                
        AsideTasks.set_if_none(config['script'], 'open_files', True)
        AsideTasks.set_if_none(config['script'], 'extension', '.py')
                
        config_manager.set_config(config)
        
    

    @staticmethod
    def save_path(config_area: str, config_to_set: str, path_value: str, absolute_path: bool):
        
        full_path, path_check = AsideTasks.normalize_path(path_value, absolute_path)
        
        if not path_check.is_dir():
            raise ValueError("The path you entered is not a valid directory. Please enter a valid directory.")
        
        config = config_manager.retrieve_config()
        if config_area not in config:
            config[config_area] = {}
        
        config[config_area][config_to_set] = full_path
        
        config_manager.set_config(config)


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
        Create a new project or script based on the specified area.
        Args:
            args (dict): A dictionary containing the following keys:
                - create_area (str): The type of item to create. Must be 'project' or 'script'.
                - name (str): The name of the project or script to create.
                - extension_to_use (str): The file extension to use for the created item.
        Returns:
            None
        Raises:
            Prints an error message if create_area is not 'project' or 'script'.
        Examples:
            >>> create({'create_area': 'project', 'name': 'my_project', 'extension_to_use': '.py'})
            >>> create({'create_area': 'script', 'name': 'my_script', 'extension_to_use': '.py'})
        """
        
        match args.create_area:
            case 'project':
                create_manager.create_project(args.name, args.extension_to_use, args.open_file, args.open_git)
            case 'script':
                create_manager.create_script(args.name, args.extension_to_use)
            case _:
                print("Invalid create area.")
    
    @staticmethod
    def create_project(project_name: str, extension_to_use: str, to_open: str|bool, to_git: str|bool):
        """
        Create a new project directory with initial files and optional Git initialization.
        This function creates a project folder at the configured project path with:
        - A README.md file containing basic project information
        - A main file with the specified extension
        - Optional Git repository initialization
        - Optional opening of the project in VS Code
        Args:
            project_name (str): The name of the project to create. This will be used as the 
                               directory name and in the generated file headers.
            extension_to_use (str): The file extension for the main file. Use 'default' to 
                                   use the extension from the project configuration, or specify 
                                   a custom extension (e.g., '.py', '.js').
        Raises:
            ValueError: If the project path is not configured in the config manager.
        Notes:
            - The function behavior differs slightly between Windows and Unix-like systems 
              for the mkdir command (with/without shell=True flag).
            - Git initialization and VS Code opening are controlled by the project 
              configuration settings ('git' and 'open_files' keys).
            - Requires git and code (VS Code CLI) to be available in the system PATH 
              if those features are enabled.
        """
        
        config = config_manager.retrieve_config()
        project_config = config.get('project', {})
        project_path = project_config.get('path')
        project_path = Path.from_uri(project_path)
        project_extension = project_config.get('extension') if extension_to_use == 'default' else extension_to_use
        if not project_path:
            raise ValueError("Project path is not configured. Please set the project path before trying to create a project.")
        if os.name == 'nt': # Windows
            subprocess.run(['mkdir', str(project_name)], shell=True, cwd=project_path)
            with open(project_path / project_name / 'README.md', 'w') as file:
                file.write(f"# {project_name}\n\nProject created using the file manager.")
            
            with open(project_path / project_name / f'main{project_extension}', 'w') as file:
                file.write(f"# Main file for {project_name}\n\n# This is the main file for the project created using the file manager.")
                
            inside_project = project_path / project_name
            if to_git == 'default':
                if project_config.get('git', True):
                    subprocess.run(['git', 'init'], shell=True, cwd=inside_project)
                    subprocess.run(['git', 'branch', '-M', 'main'], shell=True, cwd=inside_project)
            else:
                if to_git:
                    subprocess.run(['git', 'init'], shell=True, cwd=inside_project)
                    subprocess.run(['git', 'branch', '-M', 'main'], shell=True, cwd=inside_project)
            
            if to_open == 'default':
                if project_config.get('open_files', True):
                    subprocess.run(['code', str(project_path / project_name)], shell=True)
            else:
                if to_open:
                    subprocess.run(['code', str(project_path / project_name)], shell=True)
        
        else:
            subprocess.run(['mkdir', project_name], shell=True, cwd=project_path)
            with open(project_path / project_name / 'README.md', 'w') as file:
                file.write(f"# {project_name}\n\nProject created using the file manager.")
            
            with open(project_path / project_name / f'main{project_extension}', 'w') as file:
                file.write(f"# Main file for {project_name}\n\n# This is the main file for the project created using the file manager.")
                
            inside_project = project_path / project_name

            if project_config.get('git', True):
                subprocess.run(['git', 'init'], shell=True, cwd=inside_project)
                subprocess.run(['git', 'branch', '-M', 'main'], shell=True, cwd=inside_project)
            
            if project_config.get('open_files', True):
                subprocess.run(['code', str(project_path / project_name)], shell=True)
    
    @staticmethod
    def create_script(script_name: str, extension_to_use: str):
        """
        Create a new script file with the specified name and extension.
        This function creates a script file in the configured script directory.
        The script file is initialized with a standard header comment. On non-Windows
        systems, it also creates a directory for the script. If configured, the created
        script file is automatically opened in the default code editor (VS Code).
        Args:
            script_name (str): The name of the script to create (without extension).
            extension_to_use (str): The file extension to use for the script.
                If set to 'default', uses the extension specified in the configuration.
                Otherwise, uses the provided extension string.
        Raises:
            ValueError: If the script path is not configured in the configuration file.
        Returns:
            None
        Note:
            - On Windows (os.name == 'nt'): Creates the script file directly.
            - On other systems: Creates a directory with the script name, then creates
              the script file inside it.
            - The script file is populated with a standard header comment.
            - If 'open_files' is enabled in the script configuration, the created
              file is automatically opened in VS Code.
        """
        
        config = config_manager.retrieve_config()
        script_config = config.get('script', {})
        script_path = script_config.get('path')
        script_path = Path.from_uri(script_path)
        script_extension = script_config.get('extension') if extension_to_use == 'default' else extension_to_use
        if not script_path:
            raise ValueError("Script path is not configured. Please set the script path before trying to create a script.")
        
        if os.name == 'nt': # Windows
            with open(script_path / f'{script_name}{script_extension}', 'w') as file:
                file.write(f"# Script file for {script_name}\n\n# This is the main file for the script created using the file manager.")
        else:
            subprocess.run(['mkdir', script_name], shell=True, cwd=script_path)
            with open(script_path / f'{script_name}{script_extension}', 'w') as file:
                file.write(f"# Script file for {script_name}\n\n# This is the main file for the script created using the file manager.")
                
        if script_config.get('open_files', True):
            subprocess.run(['code', str(script_path / f'{script_name}{script_extension}')], shell=True)

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
    def set_if_none(config_dict: dict, key: str, value: any):
        """
        Set a configuration value only if the key does not already exist in the dictionary.
        Args:
            config_dict (dict): The configuration dictionary to update.
            key (str): The key to check and potentially set.
            value (any): The value to assign if the key is not present.
        Returns:
            None
        Note:
            Prints the updated dictionary to stdout if a new key-value pair is added.
        """
        
        if key not in config_dict:
            config_dict[key] = value
            print(config_dict)
            
    @staticmethod
    def create_config_if_none(config:dict, config_area: str):
        def create_config_if_none(config: dict, config_area: str):
            """
            Ensure a configuration area exists in the config dictionary.
            Creates an empty dictionary for the specified config_area key if it does not
            already exist in the config dictionary.
            Args:
                config (dict): The configuration dictionary to modify.
                config_area (str): The key/section name to ensure exists in the config.
            Returns:
                dict: The modified config dictionary with the config_area initialized if needed.
            """
        
        if config_area not in config:
            config[config_area] = {}
        return config
    
    @staticmethod
    def normalize_path(path_value: str, absolute_path: bool):
        def normalize_path(path_value: str, absolute_path: bool) -> tuple[str, Path]:
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
                
                full_path = WindowsPath(path_value)
                path_check = full_path
                full_path = full_path.as_uri()
            print(full_path)
        else :
            if path_value[0] != '/':
                path_value = '/' + path_value
                print(path_value)
                full_path = Path.cwd().as_uri() + path_value
                path_check = Path.from_uri(full_path)
        return full_path, path_check
        
