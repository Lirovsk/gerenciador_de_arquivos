import argparse
from request_processor import config_manager, open_manager, search_manager, create_manager

parser = argparse.ArgumentParser(prog='file_manager',
                                  description='A simple file manager that allows you to perform basic file operations.',
                                  epilog='In case of any issues, please contact me at https://github.com/Lirovsk',
                                  usage='%(prog)s [options]')

parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')

subparsers = parser.add_subparsers(dest='command', help='available commands', required=True,
                      )

config_parser = subparsers.add_parser('config', help='Configure paths and settings for different areas')

sub_subparser1 = config_parser.add_subparsers(dest='config_action', help='actions to configure different areas')
# project area
set_projects_path = sub_subparser1.add_parser('set-project-path', help='Set the path for projects')
set_projects_path.add_argument('value', help='The path value to set for projects')
set_projects_path.add_argument('--absolute-path', '-ap', action='store_true', help='Indicates that the provided path is an absolute path', dest='absolute_path')
set_projects_path.add_argument('--relative-path', '-rp', action='store_false', help='Indicates that the provided path is a relative path', dest='absolute_path')

set_project_extension = sub_subparser1.add_parser('set-project-extension', help='Set the default file extension for projects')
set_project_extension.add_argument('value', help='The file extension to set for projects (e.g., .py, .js)')

set_project_open = sub_subparser1.add_parser('set-project-open', help='Configure whether to open and/or configure some areas of a project')
set_project_open.add_argument('config_to_set', help='The specific configuration to set for opening projects (e.g., git, open_files,open_git)')
set_project_open.add_argument('value', help='The value to set for the specified configuration (e.g., true, false, .py)')

# scripts area
set_scripts_path = sub_subparser1.add_parser('set-script-path', help='Set the path for scripts')
set_scripts_path.add_argument('value', help='The path value to set for scripts')
set_scripts_path.add_argument('--absolute-path', '-ap', action='store_true', help='Indicates that the provided path is an absolute path', dest='absolute_path')
set_scripts_path.add_argument('--relative-path', '-rp', action='store_false', help='Indicates that the provided path is a relative path', dest='absolute_path')

set_scripts_open = sub_subparser1.add_parser('set-script-open', help='Configure whether to open scripts')
set_scripts_open.add_argument('config_to_set', help='The specific configuration to set for opening scripts (e.g., open_files)')
set_scripts_open.add_argument('value', help='The value to set for the specified configuration (e.g., true, false)')

set_script_extension = sub_subparser1.add_parser('set-script-extension', help='Set the default file extension for scripts')
set_script_extension.add_argument('value', help='The file extension to set for scripts (e.g., .py, .js)')

# open configurations
open_parser = subparsers.add_parser('open', help='Open files or directories based on the configured paths')
open_parser.add_argument('open_area', help='The area to open (e.g., project, script)')
open_parser.add_argument('file_to_open', help='Specific files to open within the area (optional)')

# create command
create_parser = subparsers.add_parser('create', help='Create new files or directories based on the configured paths')
create_parser.add_argument('create_area', help='The area to create in (e.g., project, script)')
create_parser.add_argument('name', help='The name of the file or directory to create')
create_parser.add_argument('--extension', '-e', nargs='?', default='default', help='The file extension to use when creating a file (optional, default is "default" which uses the configured extension for the area)', dest='extension_to_use'  )

# search command
search_parser = subparsers.add_parser('search', help='Search for files or directories based on the configured paths')
search_parser.add_argument('search_area', help='The area to search in (e.g., project, script)')
search_parser.add_argument('search_name', nargs='?', default=None, help='The search query to find specific files or directories (e.g., filename or part of it)')
search_parser.add_argument('--all', '-a', action='store_true', help='Search for all files and directories in the specified area', dest='search_all')

args = parser.parse_args()


if args.command == 'config':
    config_manager.save_config(args)
if args.command == 'create':
    create_manager.create(args)
if args.command == 'open':
    open_manager.open(args)
if args.command == 'search':
    search_manager.search(args)