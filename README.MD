# File Manager CLI

- **Version:** 2.2.3
- **Author:** [João Vítor Lira (Lirovsk)](https://github.com/Lirovsk)
- **Purpose:** create, open, search, and delete project folders and script files from the terminal.

---

## English

### Overview

`file_manager` is a small command-line utility for speeding up repetitive project and script setup.

It stores default locations and behaviors in a JSON config file, then uses those settings to:

- create project folders with starter files
- create standalone scripts with a configurable extension
- open projects and scripts in VS Code
- search configured directories by name
- delete projects and scripts

This repository is designed around a simple CLI entry point and a single request-processing module, making it easy to extend with new templates or workflows later.

### Features

- Separate configuration for `project` and `script` areas
- Support for default extensions such as `.py`, `.js`, `.ts`, or any other custom extension
- Optional project git initialization
- Optional automatic opening in VS Code after creation
- Search by partial name or list all items in a configured area
- Interactive or forced deletion
- Automatic creation of `file_manager_config.json` if it does not exist yet

### Requirements

- Python 3.10 or newer
- VS Code CLI available in `PATH` as `code` if you want to use the open features
- Git available in `PATH` if you enable git initialization for projects

### Repository Structure

- `main.py`: CLI parser and command dispatch
- `request_processor.py`: configuration, create, open, search, and delete logic
- `file_manager_config.json`: persisted user configuration
- `requirements.txt`: dependency file for the project environment
- `documents/`: auxiliary project material

### How It Works

The CLI is organized into five top-level commands:

- `config`
- `create`
- `open`
- `search`
- `delete`

Configuration values are stored in `file_manager_config.json` as file URIs. A typical config looks like this:

```json
{
	"script": {
		"path": "file:///C:/Users/Arauj/Documents/VScode/python/Scripts",
		"open_files": true,
		"extension": ".py"
	},
	"project": {
		"path": "file:///C:/Users/Arauj/Documents/VScode/python/projetos",
		"git": false,
		"open_files": true,
		"extension": ".py"
	}
}
```

### Installation

1. Clone or download this repository.
2. Open a terminal in the project root.
3. Run commands with:

```bash
python main.py <command> [options]
```

You can also check the installed version with:

```bash
python main.py --version
```

### First-Time Setup

Set the base folders where projects and scripts will be managed.

Absolute paths:

```bash
python main.py config set-project-path "C:/path/to/projects" --absolute-path
python main.py config set-script-path "C:/path/to/scripts" --absolute-path
```

Relative paths:

```bash
python main.py config set-project-path projects --relative-path
python main.py config set-script-path scripts --relative-path
```

Then configure the default extensions and behavior flags you want to use.

```bash
python main.py config set-project-extension .py
python main.py config set-script-extension .py
python main.py config set-project-open git true
python main.py config set-project-open open_files true
python main.py config set-script-open open_files true
```

### Command Reference

#### `config`

Updates the saved configuration.

Available actions:

- `set-project-path`
- `set-project-extension`
- `set-project-open`
- `set-script-path`
- `set-script-open`
- `set-script-extension`

Examples:

```bash
python main.py config set-project-path "C:/workspace/projects" --absolute-path
python main.py config set-project-extension .js
python main.py config set-project-open git false
python main.py config set-project-open open_files true
python main.py config set-script-path "C:/workspace/scripts" --absolute-path
python main.py config set-script-extension .py
python main.py config set-script-open open_files false
```

Notes:

- path values must point to existing directories
- boolean flags are expected as `true` or `false`
- missing `project` or `script` sections are created automatically when needed

#### `create`

Creates either a project folder or a script file.

Project creation:

- creates a folder named after the project
- creates `README.md`
- creates `main<extension>`
- optionally initializes git
- optionally opens the folder in VS Code

Script creation:

- creates `<name><extension>` in the configured script directory
- optionally opens the file in VS Code

Examples:

```bash
python main.py create project my_project
python main.py create project my_project --extension .js
python main.py create project my_project --no-open --open-git
python main.py create script my_script
python main.py create script my_script --extension .ts
python main.py create script my_script --no-open
```

Notes:

- when `--extension` is omitted, the configured default extension is used
- when `--open` or `--no-open` is omitted, the saved `open_files` setting is used
- for projects, when `--open-git` or `--no-git` is omitted, the saved `git` setting is used

#### `open`

Opens an existing project directory or script file in VS Code.

Examples:

```bash
python main.py open project my_project
python main.py open script my_script.py
```

Notes:

- the target must exist inside the configured base directory
- for scripts, you should pass the exact file name, including the extension

#### `search`

Lists items in the configured directory or filters them by partial name.

Examples:

```bash
python main.py search project api
python main.py search script test
python main.py search project --all
python main.py search script --all
```

Notes:

- search uses a simple substring match
- if nothing is found, the command prints a message instead of failing

#### `delete`

Deletes a project folder or script file.

Examples:

```bash
python main.py delete project my_project
python main.py delete project my_project --force
python main.py delete script my_script.py
python main.py delete script my_script.py --force
```

Notes:

- without `--force`, the command asks for confirmation
- deleting a project removes the entire project directory recursively
- deleting a script removes a single file

### Generated Files

When you create a project, the tool currently generates:

```text
my_project/
├── README.md
└── main.py
```

If the configured extension is different, the main file follows that extension, for example `main.js` or `main.ts`.

When you create a script, the tool generates a single file such as:

```text
my_script.py
```

### Error Handling

The CLI raises explicit errors when:

- a configured path is missing
- a configured path does not exist
- an item to open or delete does not exist
- an absolute Windows path is missing a drive letter

If `file_manager_config.json` is missing, it is automatically created before configuration is read or written.

### Limitations

- paths must already exist before they can be saved in the configuration
- opening files depends on the `code` command being available in the system
- git initialization depends on `git` being installed and available in `PATH`
- search is case-sensitive because it uses direct substring comparison
- the tool currently creates only a minimal starter structure

### Roadmap Ideas

- project templates for multiple stacks
- virtual environment creation
- automatic dependency installation
- richer search filters
- safer validation and clearer CLI help text

---

## Português

### Visão Geral

`file_manager` é uma pequena ferramenta de linha de comando para acelerar tarefas repetitivas de criação de projetos e scripts.

Ela salva locais e comportamentos padrão em um arquivo JSON de configuração e depois usa essas definições para:

- criar pastas de projeto com arquivos iniciais
- criar scripts avulsos com extensão configurável
- abrir projetos e scripts no VS Code
- buscar nomes dentro dos diretórios configurados
- excluir projetos e scripts

Este repositório foi organizado em torno de um ponto de entrada simples da CLI e de um único módulo de processamento de requisições, o que facilita extensões futuras com novos templates ou fluxos de trabalho.

### Recursos

- Configuração separada para as áreas `project` e `script`
- Suporte a extensões padrão como `.py`, `.js`, `.ts` ou qualquer outra extensão personalizada
- Inicialização opcional de git para projetos
- Abertura automática opcional no VS Code após a criação
- Busca por nome parcial ou listagem completa dos itens em uma área configurada
- Exclusão interativa ou forçada
- Criação automática de `file_manager_config.json` caso ele ainda não exista

### Requisitos

- Python 3.10 ou superior
- CLI do VS Code disponível no `PATH` como `code` para usar os recursos de abertura
- Git disponível no `PATH` se você habilitar a inicialização de git para projetos

### Estrutura do Repositório

- `main.py`: parser da CLI e despacho dos comandos
- `request_processor.py`: lógica de configuração, criação, abertura, busca e exclusão
- `file_manager_config.json`: configuração persistida do usuário
- `requirements.txt`: arquivo de dependências do ambiente do projeto
- `documents/`: material auxiliar do projeto

### Como Funciona

A CLI é organizada em cinco comandos principais:

- `config`
- `create`
- `open`
- `search`
- `delete`

Os valores de configuração são armazenados em `file_manager_config.json` como URIs de arquivo. Uma configuração típica se parece com isto:

```json
{
	"script": {
		"path": "file:///C:/Users/Arauj/Documents/VScode/python/Scripts",
		"open_files": true,
		"extension": ".py"
	},
	"project": {
		"path": "file:///C:/Users/Arauj/Documents/VScode/python/projetos",
		"git": false,
		"open_files": true,
		"extension": ".py"
	}
}
```

### Instalação

1. Faça clone ou download deste repositório.
2. Abra um terminal na raiz do projeto.
3. Execute os comandos com:

```bash
python main.py <comando> [opções]
```

Você também pode verificar a versão instalada com:

```bash
python main.py --version
```

### Configuração Inicial

Defina as pastas base onde projetos e scripts serão gerenciados.

Caminhos absolutos:

```bash
python main.py config set-project-path "C:/caminho/para/projetos" --absolute-path
python main.py config set-script-path "C:/caminho/para/scripts" --absolute-path
```

Caminhos relativos:

```bash
python main.py config set-project-path projects --relative-path
python main.py config set-script-path scripts --relative-path
```

Depois configure as extensões padrão e as flags de comportamento que deseja usar.

```bash
python main.py config set-project-extension .py
python main.py config set-script-extension .py
python main.py config set-project-open git true
python main.py config set-project-open open_files true
python main.py config set-script-open open_files true
```

### Referência de Comandos

#### `config`

Atualiza a configuração salva.

Ações disponíveis:

- `set-project-path`
- `set-project-extension`
- `set-project-open`
- `set-script-path`
- `set-script-open`
- `set-script-extension`

Exemplos:

```bash
python main.py config set-project-path "C:/workspace/projects" --absolute-path
python main.py config set-project-extension .js
python main.py config set-project-open git false
python main.py config set-project-open open_files true
python main.py config set-script-path "C:/workspace/scripts" --absolute-path
python main.py config set-script-extension .py
python main.py config set-script-open open_files false
```

Observações:

- os valores de caminho precisam apontar para diretórios existentes
- flags booleanas devem ser informadas como `true` ou `false`
- se as seções `project` ou `script` não existirem, elas são criadas automaticamente quando necessário

#### `create`

Cria uma pasta de projeto ou um arquivo de script.

Criação de projeto:

- cria uma pasta com o nome do projeto
- cria `README.md`
- cria `main<extension>`
- opcionalmente inicializa git
- opcionalmente abre a pasta no VS Code

Criação de script:

- cria `<name><extension>` no diretório configurado para scripts
- opcionalmente abre o arquivo no VS Code

Exemplos:

```bash
python main.py create project my_project
python main.py create project my_project --extension .js
python main.py create project my_project --no-open --open-git
python main.py create script my_script
python main.py create script my_script --extension .ts
python main.py create script my_script --no-open
```

Observações:

- quando `--extension` é omitido, a extensão padrão configurada é usada
- quando `--open` ou `--no-open` é omitido, a configuração salva em `open_files` é usada
- para projetos, quando `--open-git` ou `--no-git` é omitido, a configuração salva em `git` é usada

#### `open`

Abre um diretório de projeto existente ou um arquivo de script no VS Code.

Exemplos:

```bash
python main.py open project my_project
python main.py open script my_script.py
```

Observações:

- o alvo precisa existir dentro do diretório base configurado
- para scripts, você deve informar o nome exato do arquivo, incluindo a extensão

#### `search`

Lista itens no diretório configurado ou filtra por nome parcial.

Exemplos:

```bash
python main.py search project api
python main.py search script test
python main.py search project --all
python main.py search script --all
```

Observações:

- a busca usa comparação simples por substring
- se nada for encontrado, o comando imprime uma mensagem em vez de falhar

#### `delete`

Exclui uma pasta de projeto ou um arquivo de script.

Exemplos:

```bash
python main.py delete project my_project
python main.py delete project my_project --force
python main.py delete script my_script.py
python main.py delete script my_script.py --force
```

Observações:

- sem `--force`, o comando solicita confirmação
- excluir um projeto remove todo o diretório do projeto recursivamente
- excluir um script remove apenas um arquivo

### Arquivos Gerados

Quando você cria um projeto, a ferramenta atualmente gera:

```text
my_project/
├── README.md
└── main.py
```

Se a extensão configurada for diferente, o arquivo principal segue essa extensão, por exemplo `main.js` ou `main.ts`.

Quando você cria um script, a ferramenta gera um único arquivo, como:

```text
my_script.py
```

### Tratamento de Erros

A CLI lança erros explícitos quando:

- um caminho configurado está ausente
- um caminho configurado não existe
- um item para abrir ou excluir não existe
- um caminho absoluto no Windows foi informado sem letra de unidade

Se `file_manager_config.json` estiver ausente, ele é criado automaticamente antes da leitura ou escrita da configuração.

### Limitações

- os caminhos precisam existir antes de serem salvos na configuração
- a abertura de arquivos depende do comando `code` disponível no sistema
- a inicialização de git depende do `git` instalado e disponível no `PATH`
- a busca é sensível a maiúsculas e minúsculas porque usa comparação direta por substring
- a ferramenta ainda cria apenas uma estrutura inicial mínima

### Ideias de Roadmap

- templates de projeto para múltiplas stacks
- criação de ambiente virtual
- instalação automática de dependências
- filtros de busca mais ricos
- validação mais segura e ajuda da CLI mais clara
