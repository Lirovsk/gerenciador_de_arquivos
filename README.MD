# The main idea
(Versão em português ao final desta página)

This project was born due a lazynes of mine: I love starting a new project, but I hate losing time creating all the files and directories need to star programing. So I thought it would be a great idea to automate the hole process of creting the archives needed by saving predefined directories and then just tell the script what path to choose and the name of the program. 

Of course I want to create a robust solution, by robust I mean a program that can create not just a folder but also create a virtual enviroment, installing libraries and more.  

## Working principle
Although I'm already planning to change the way the program is constructed, for formal reasons I'll explain how it works because this project is also a portfolio. 

This program saves two diferent paths, one is to save scripts, the other is to save entire projects. 

The program currently have three main commands:
- {config} to set all the configurantions;
- {create-project} to create the projects;
- {create-script} to create scripts. 

By having the paths pre saved, the program can create scripts or projects faster than manualy creating it. 

### Commands
The commands are very intuitive, which means the 'config' command is responsible for configurate the paths and so. But there are also some flags that can be used with these commands and this section is all about explainnig them.

#### {config}
The 'config' command is responsible for running settings and stablish some constansts (Ex. the predefined path to scripts). To help the use of this program, some flags are related to it. 

--for-scripts(-fs) 

This flag tells the program that the config command is now setting (or changing) the variable responsible to save the path tied to the scripts. This flag does not need a value. It's own behavior set itself to true when the flag is used.

--for-projects(-fp)

The same as the '--for-scripts' flag, but for projects. This flag tells the program the variable being used is the one tied to the projects.

--relative-path(-rp)

This flags tells the program you are about to use a relative path. The start point of the relative path will always be the current work directory. This flag receive a string as a path (the format is directory/subdirectory/project_folder).

--absolute-path(-ap)

It works similar to the previous flag, but in this case you are using an absolute path to tell the program where your directory will be saved. It also receive a string as the argument

#### {create-script}
The 'create-script' command tells the program to create a script on the designated path and open it in VScode. This command receive a string as value, this string is the name of the script to be created.

The command receive the name of the argument, create the file on the designated path, write a basic template then open it (in this order) in VScode. Before creating the file, the program ensures the path exists and is well setted.

#### {create-project}
It works similar to the 'create-script' command but instead of create the file on the designated path, it creates the directory of the project first then create the files for the project.

The command first create the directory for the hole project, create the files (it create the main.py and the README.md), create git repository, change the name of the branch to main (recomended by GitHub) then open the folder on VScode.

## Next objectives
The next steps for this project will be:

- Refactoring the code to avoid excessive use of if and else;
- Turning repeated part of the into functions to reduce the amount of written lines;
- Adding more flags to the 'create-script' and 'create-project' aiming to give more control about the creation process;
- Studying ways to tranform this code into an executable to be used anywhere in your PC/Mac/Linux;
  
# Ideia principal
Esse projeto nasceu por causa de uma preguiça minnha: Eu amo começar novos projetos, mas eu detesto perder meu tempo criando todos os arquivos e diretórios necessários para começar a programar. Então eu pensei que seria uma boa ideia automatizar esse processo inteiro de criar os arquivos necessários usando um diretórios predefinidos e só dizer ao programa o caminho a escolher e o nome do arquivo.

Claro que eu quero criar uma solução robusta, com robusta eu quero dizer um programa responsável por não só criar as pastas, mas os ambientes vistuais necessários, instalar bibliotecas e mais.

## Princípio de funcionamento 
Apesar de eu já estar planejando trocar a maneira que o programa é construido, por rasões formais eu vou explicar como funciona porque esse projeto é também um portifólio. 

Esse programa salva dois caminhos diferentes, um voltado para criar scripts e outro para criar projetos inteiros.

O programa atualmente tem três comandos principais:
- {config} para configurar todos os parâmetros;
- {create-project} para criar projetos;
- {create-script} para criar scripts.

Tendo os caminhos salvos, o programa pode criar scripts ou projetos mais rapidamente que criando eles manualmente.

### Comandos
Os comandos são bem intuitivos, o que significa que o comando 'config' é responsável por configurar os caminhos a serem salvos, e assim vai. Além disso algumas flags podem ser usadas com esses comandos e essa seção é todo sobre exlpicar elas.

#### {config}
O comando 'config' é responsável por rodar as configurações e definir algumas constantes (Ex. o caminho predefinido para scripts). Para ajudar o uso desse programa algumas flags são relacionadas a esse comando.

--for-sccripts(-fs)

Essa flag diz ao programa que o comando de configuração está configurando (ou trocando) a variável responsável por salvar o caminho atrelado aos scripts. Essa flag não precisa receber nenhum valor; O seu próprio comportamento se configura para verdadeiro quando essa flag é usada.

--for-projects(-fp)

A mesma forma que a flag '--for-scripts', mas para projetos. Essa flag conta para o programa que a variável sendo manipulada é a atrelada aos projetos.

--relative-path(-rp)

Essa flag conta ao programa que você está prestes a usar um caminho relativo. O ponto inicial do caminho relativo sempre será o seu diretório de trabalho atual. Essa flag recebe uma string como caminho (o formato é diretório/subdiretório/pasta_projeto).

--absolute-path(-ap)

Funciona de maneira similar a flag anterior, mas nesse caso você está usando um caminho absoluto para dizer ao programa onde o diretório será salvo. Também recebe uma string como argumento.

#### {create-script}
O comando 'create-script' diz ao programa para criar um script no caminha designado e abrir o script no VScode. Esse comando recebe uma string como valor, essa string é o nome do script a ser criado.

O comando recebe o nome do argumento, cria o arquivo no caminho designado, escreve um template básico e depois abre isso (nessa ordem) no VScode. Antes de criar o arquivo, o programa confirma que o acaminho existe e está bem configurado.

#### {create-project}
Funciona de maneira similar ao comando 'create-script' mas ao invés de criar o arquivo no caminho designado, o comando cria um diretório do projeto primeiro e depois cria os arquivos do projeto.

O comando primeiro cria o diretório de projeto inteiro, cria os arquivos (cria o arquivo main.py e README.md), cria um repositório git, troca o nome da branch para main (recomendado pelo GitHub) e depois abre a pasta no VScode.

## Próximos objetivos 
Os próximos passo para esse projeto serão: 

- Refatorar o código para evitar o uso excessivo de if e else;
- Transformar partes repetidas de código em funções para reduzir a quantidade de linhas escritas;
- Adicionar mais flags ao comando 'create-script' e 'create-project' mirando fornecer mais cobtrole sobre o processo de criação;
- Estudar maneiras de transformar esse código em executável para ser usado em qualquer lugar do seu PC/Mac/Linux
- 