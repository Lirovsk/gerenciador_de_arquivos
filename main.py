import argparse
from request_processor import config_manager, open_manager, search_manager, create_manager, delete_manager

parser = argparse.ArgumentParser(prog='file_manager',
                                  description='A simple file manager that allows you to perform basic file operations.',
                                  epilog='In case of any issues, please contact me at https://github.com/Lirovsk',
                                  usage='%(prog)s [options]')

parser.add_argument('--version', action='version', version='%(prog)s 2.2.3')

subparsers = parser.add_subparsers(dest='command', help='available commands', required=True)

config_parser = subparsers.add_parser('config', help='Configure paths and settings for different areas')

sub_subparser1 = config_parser.add_subparsers(dest='config_action', help='actions to configure different areas')

set_path = sub_subparser1.add_parser('set-path', help='Set the main directory used by the program')
set_path.add_argument('value', help='The path valeu to set')
set_path.add_argument('--absolute-path', '-ap', action='store_true', help='Indicates that the provided path is an absolute path', 
                      dest='absolute_path', default=True)
set_path.add_argument('--relative-path', '-rp', action='store_false', help='Indicates that the provided path is a relative path', dest='absolute_path')

# ==================== projects area ====================
set_projects_open = sub_subparser1.add_parser('set-project-open', help='Configure whether to open projects')
set_projects_open.add_argument(
    "config_to_set",
    help="The specific configuration to set for opening scripts (e.g., files, git)",
    choices=['files', 'git']
)
set_projects_open.add_argument(
    '--true', '-t', action='store_true', help="The value to set for the specified configuration (e.g., true, false)",
    dest='value_to_set'
)
set_projects_open.add_argument(
    '--false', '-f', action='store_false', help="The value to set for the specified configuration (e.g., true, false)",
    dest='value_to_set'
)

set_projects_extension = sub_subparser1.add_parser('set-project-extension', help='Config the default extension for projects')
set_projects_extension.add_argument(
    "value", help="The file extension to set for projects (e.g., .py, .js)"
)

# ==================== scripts area ====================
set_scripts_open = sub_subparser1.add_parser('set-script-open', help='Configure whether to open scripts')
set_scripts_open.add_argument('config_to_set', help='The specific configuration to set for opening scripts (e.g., files)',
                              choices=['files'])
set_scripts_open.add_argument(
    '--true', '-t', action='store_true', help="The value to set for the specified configuration (e.g., true, false)",
    dest='value_to_set'
)
set_scripts_open.add_argument(
    '--false', '-f', action='store_false', help="The value to set for the specified configuration (e.g., true, false)",
    dest='value_to_set'
)

set_script_extension = sub_subparser1.add_parser('set-script-extension', help='Set the default file extension for scripts')
set_script_extension.add_argument('value', help='The file extension to set for scripts (e.g., .py, .js)')

# ==================== open configurations ====================
open_parser = subparsers.add_parser('open', help='Open files or directories based on the configured paths')
open_parser.add_argument('open_area', help='The area to open (e.g., project, script)')
open_parser.add_argument('file_to_open', help='Specific files to open within the area (optional)')

# ==================== create command ====================
create_parser = subparsers.add_parser('create', help='Create new files or directories based on the configured paths')
create_parser.add_argument('create_area', help='The area to create in (e.g., project, script, folder)',
                           choices=['project', 'script', 'folder'])
create_parser.add_argument('create_name', help='The name of the file, directory, or folder to create')
create_parser.add_argument('--extension', '-e', help='The file extension to use when creating a file (optional)', 
                           dest='file_extension', default=None)
create_parser.add_argument('--open-git', '-og', action='store_true', help='Open the created project in Git (if applicable)',
                           dest='open_git', default=None)
create_parser.add_argument('--open-files', '-of', action='store_true', help='Open the created files (if applicable)',
                           dest='open_files', default=None)

# ==================== search command ====================
search_parser = subparsers.add_parser('search', help='Search for files or directories based on the configured paths')
search_parser.add_argument('search_area', help='The area to search in (e.g., project, script)')
search_parser.add_argument('search_name', nargs='?', default=None, help='The search query to find specific files or directories (e.g., filename or part of it)')
search_parser.add_argument('--all', '-a', action='store_true', help='Search for all files and directories in the specified area', dest='search_all')

delete_parser = subparsers.add_parser('delete', help='Delete files or directories based on the configured paths')
delete_parser.add_argument('delete_area', help='The area to delete from (e.g., project, script)')
delete_parser.add_argument('delete_name', help='The name of the file or directory to delete')
delete_parser.add_argument('--force', '-f', nargs='?', default=False, const=True, help='Force delete without confirmation (use with caution)', dest='force_delete')

args = parser.parse_args()


# ==================== Command Handling ====================
match args.command:
    case 'config':
        config_manager.save_config(args)

    case 'create':
        create_manager.create(args)

    case 'open':
        open_manager.open(args)

    case 'search':
        search_manager.search(args)

    case 'delete':
        delete_manager.delete(args)
