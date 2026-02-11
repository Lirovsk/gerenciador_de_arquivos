import argparse

parser = argparse.ArgumentParser(prog='file_manager',
                                  description='A simple file manager that allows you to perform basic file operations.',
                                  epilog='In case of any issues, please contact me at https://github.com/Lirovsk',
                                  usage='%(prog)s [options]')

parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')

subparsers = parser.add_subparsers(dest='command', help='available commands', required=True,
                      )

# ++++ Subparser for configuration ++++
config = subparsers.add_parser('config', help='Configure the file manager')
two_subparse_config = config.add_subparsers(dest='config_area', help='which area to configure', required=True) #cria subparser para escolher entre configurar para scripts ou projetos

for_scripts = two_subparse_config.add_parser('for-scripts', help='Configure the file manager for scripts')
scripts_subparsers = for_scripts.add_subparsers(dest='scripts_config', help='what to configure for scripts', required=True) #cria subparser para escolher o que configurar para scripts, como o path

scripts_path = scripts_subparsers.add_parser('path', help='Configure path for scripts') # essa linha cria o chamado "path" dentro do "for-scripts", ou seja, o comando completo seria "config for-scripts path"
scripts_path.add_argument('path_value', help='The path to be the default for creating the files') # esse argumento é obrigatório, ou seja, o comando completo seria "config for-scripts path <path_value>", onde <path_value> é o valor do caminho que o usuário quer configurar
scripts_path.add_argument('--relative-path', '-rp', action='store_true', help='Use a relative path to be the default for creating the files', default=None)
scripts_path.add_argument('--absolute-path', '-ap', action='store_true', help='Use an absolute path to be the default for creating the files', default=None)

scripts_open_config = scripts_subparsers.add_parser('open-config', help='Configure how the files should be opened') # essa linha cria o chamado "open-config" dentro do "for-scripts", ou seja, o comando completo seria "config for-scripts open-config"
scripts_open_config.add_argument('--open', '-o', action='store_true', help='Open the files after creating them', default=True, dest='open_files') # esse argumento é opcional, ou seja, o comando completo seria "config for-scripts open-config --open" para abrir os arquivos após criá-los, ou "config for-scripts open-config" para não abrir os arquivos após criá-los (o padrão é abrir os arquivos)
scripts_open_config.add_argument('--no-open', '-no', action='store_false', help='Do not open the files after creating them', default=True, dest='open_files') # esse argumento é opcional, ou seja, o comando completo seria "config for-scripts open-config --no-open" para não abrir os arquivos após criá-los, ou "config for-scripts open-config" para abrir os arquivos após criá-los (o padrão é abrir os arquivos)

for_projects = two_subparse_config.add_parser('for-projects', help='Configure the file manager for projects')
projects_subparsers = for_projects.add_subparsers(dest='projects_config', help='what to configure for projects', required=True)

projects_path = projects_subparsers.add_parser('path', help='Configure path for projects')
projects_path.add_argument('path_value', help='The path to be the default for creating the files')
projects_path.add_argument('--relative-path', '-rp', action='store_true', help='Use a relative path to be the default for creating the files', default=None)
projects_path.add_argument('--absolute-path', '-ap', action='store_true', help='Use an absolute path to be the default for creating the files', default=None)

projects_open_config = projects_subparsers.add_parser('open-config', help='Configure how the files should be opened')
projects_open_config.add_argument('open_config', help='Configure how the files should be opened', choices=['open_folder', 'git'], default=None) # armazena o valor do argumento em "open_config", que pode ser "open_folder" ou "git"
projects_open_config.add_argument('--open', '-o', action='store_true', help='Open the files after creating them', default=True, dest='open_files')
projects_open_config.add_argument('--no-open', '-no', action='store_false', help='Do not open the files after creating them', default=True, dest='open_files')



# ++++ Subparser for creating files ++++
create = subparsers.add_parser('create', help='Create a new file')
two_subparse_create = create.add_subparsers(dest='create_area', help='which area to create the file in', required=True)

create_script = two_subparse_create.add_parser('script', help='Create a new script')
create_script.add_argument('script_name', help='The name of the script to be created')
create_script.add_argument('--no-open', '-no', action='store_false', help='Do not open the script after creating it', default=None, dest='open_script')

create_project = two_subparse_create.add_parser('project', help='Create a new project')
create_project.add_argument('project_name', help='The name of the project to be created')
create_project.add_argument('--no-open', '-no', action='store_false', help='Do not open the project after creating it', default=None, dest='open_project')
create_project.add_argument('--no-open-git', '-nogit', action='store_false', help='Do not initialize a git repository in the project after creating it', default=None, dest='init_git')


# suparse to open files
open_file = subparsers.add_parser('open', help='Open a file')
two_subparse_open = open_file.add_subparsers(dest='open_area', help='which area to open the file in', required=True)

open_script = two_subparse_open.add_parser('script', help='Open a script')
open_script.add_argument('script_name', help='The name of the script to be opened')

open_project = two_subparse_open.add_parser('project', help='Open a project')
open_project.add_argument('project_name', help='The name of the project to be opened')

args = parser.parse_args("open project nome1".split())

print(args)

