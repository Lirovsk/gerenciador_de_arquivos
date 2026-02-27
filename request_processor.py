from logging import config
from pathlib import Path, WindowsPath
import json
import os
import subprocess
from functools import wraps

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
    def retrive_config():
        
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
        match args.config_action:
            case 'set-project-path':
                config_manager.save_project_config(args)    
                
            
            case 'set-project-extension':
                config = config_manager.retrive_config()
                config = AsideTasks.create_config_if_none(config, 'project')
                config['project']['extension'] = args.value
                config_manager.set_config(config)
                    
                pass
            
            case 'set-project-open':
                config = config_manager.retrive_config()
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
                config = config_manager.retrive_config()
                config = AsideTasks.create_config_if_none(config, 'script')
                if args.value.lower() == 'true':
                    args.value = True
                else:
                    args.value = False
                config['script'][args.config_to_set] = args.value
                config_manager.set_config(config)
            
            case 'set-script-extension':
                config = config_manager.retrive_config()
                config = AsideTasks.create_config_if_none(config, 'script')
                config['script']['extension'] = args.value
                config_manager.set_config(config)
            
            case _:
                print("Invalid config action.")
        pass
    
    @staticmethod
    def save_project_config(args: dict):
        config_manager.save_path('project', 'path', args.value, args.absolute_path)
                
        config = config_manager.retrive_config()
                
        AsideTasks.set_if_none(config['project'], 'git', True)
        AsideTasks.set_if_none(config['project'], 'open_files', True)
        AsideTasks.set_if_none(config['project'], 'extension', '.py')                
        config_manager.set_config(config)
        
    @staticmethod
    def save_script_config(args: dict):  
        config_manager.save_path('script', 'path', args.value, args.absolute_path)
                
        config = config_manager.retrive_config()
                
        AsideTasks.set_if_none(config['script'], 'open_files', True)
        AsideTasks.set_if_none(config['script'], 'extension', '.py')
                
        config_manager.set_config(config)
        
    

    @staticmethod
    def save_path(config_area: str, config_to_set: str, path_value: str, absolute_path: bool):
        
        full_path, path_check = AsideTasks.normalize_path(path_value, absolute_path)
        
        if not path_check.is_dir():
            raise ValueError("The path you entered is not a valid directory. Please enter a valid directory.")
        
        config = config_manager.retrive_config()
        if config_area not in config:
            config[config_area] = {}
        
        config[config_area][config_to_set] = full_path
        
        config_manager.set_config(config)


class open_manager:
    
    @staticmethod
    def open(args: dict):
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
        config = config_manager.retrive_config()
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
        config = config_manager.retrive_config()
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
        match args.create_area:
            case 'project':
                create_manager.create_project(args.name, args.extension_to_use)
            case 'script':
                create_manager.create_script(args.name, args.extension_to_use)
            case _:
                print("Invalid create area.")
    
    @staticmethod
    def create_project(project_name: str, extension_to_use: str):
        config = config_manager.retrive_config()
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
                
            insdide_project = project_path / project_name
            if project_config.get('git', True):
                subprocess.run(['git', 'init'], shell=True, cwd=insdide_project)
                subprocess.run(['git', 'branch', '-M', 'main'], shell=True, cwd=insdide_project)
            
            if project_config.get('open_files', True):
                subprocess.run(['code', str(project_path / project_name)], shell=True)
        
        else:
            subprocess.run(['mkdir', project_name], shell=True, cwd=project_path)
            with open(project_path / project_name / 'README.md', 'w') as file:
                file.write(f"# {project_name}\n\nProject created using the file manager.")
            
            with open(project_path / project_name / f'main{project_extension}', 'w') as file:
                file.write(f"# Main file for {project_name}\n\n# This is the main file for the project created using the file manager.")
                
            insdide_project = project_path / project_name

            if project_config.get('git', True):
                subprocess.run(['git', 'init'], shell=True, cwd=insdide_project)
                subprocess.run(['git', 'branch', '-M', 'main'], shell=True, cwd=insdide_project)
            
            if project_config.get('open_files', True):
                subprocess.run(['code', str(project_path / project_name)], shell=True)
    
    @staticmethod
    def create_script(script_name: str, extension_to_use: str):
        config = config_manager.retrive_config()
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
        match args.search_area:
            case 'project':
                search_manager.search_project(args.search_name, args.search_all)
            case 'script':
                search_manager.search_script(args.search_name, args.search_all)
            case _:
                print("Invalid search area.")
    
    @staticmethod
    def search_project(search_name: str, search_all: bool):
        config = config_manager.retrive_config()
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
        config = config_manager.retrive_config()
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
    
class AsideTasks:
    
    @staticmethod
    def set_if_none(config_dict: dict, key: str, value: any):
        if key not in config_dict:
            config_dict[key] = value
            print(config_dict)
            
    @staticmethod
    def create_config_if_none(config:dict, config_area: str):
        if config_area not in config:
            config[config_area] = {}
        return config
    
    @staticmethod
    def normalize_path(path_value: str, absolute_path: bool):
        
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
        
