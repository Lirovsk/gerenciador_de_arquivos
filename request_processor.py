from logging import config
from pathlib import Path
import json
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
    CONFIG_FILE = "file_manager_config.json"

    @log_execution
    @staticmethod
    def retrive_config():
        
        with open(config_manager.CONFIG_FILE, 'r') as file:
            config = json.load(file)
        return config
    
    @staticmethod
    def save_config(args: dict):
        config = args.config_to_set
        if config == 'path':
            if args.relative_path and args.absolute_path:
                print("You cannot use both --relative-path and --absolute-path at the same time. Please choose one of them.")
                return
            config_manager.save_path(args.config_area, args.config_to_set, args.path_value, args.relative_path, args.absolute_path)
        
    @staticmethod
    def save_path(config_area, config_to_set, path_value, relative_path, absolute_path):
        if relative_path:
            if path_value[0] != '/':
                path_value = '/' + path_value
                print(path_value)
                full_path = Path.cwd().as_uri() + path_value
                path_check = Path.from_uri(full_path)
        elif absolute_path:
            full_path = Path.from_uri(path_value)
            print(full_path)
    
        if not path_check.is_dir():
            print("The path you entered is not a valid directory. Please enter a valid directory.")
            return
        else: 
            config = config_manager.retrive_config()
            with open(config_manager.CONFIG_FILE, 'r') as file:
                config = json.load(file)
            if config_area not in config:
                config[config_area] = {}
            config[config_area][config_to_set] = full_path
            if config_area == 'for-projects':
                config[config_area]['git'] = True
                config[config_area]['open_folder']= True
            else:
                config[config_area]['open_files'] = True

            with open(config_manager.CONFIG_FILE, 'w') as file:
                json.dump(config, file, indent=4)
            print(f"Path for {config_area} saved successfully: {full_path}")
                
    
