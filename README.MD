# File Manager CLI (v3 Documentation)

- **Repository:** [Lirovsk/gerenciador_de_arquivos](https://github.com/Lirovsk/gerenciador_de_arquivos)
- **CLI version output:** `file_manager 2.2.3`
- **Entry point:** `main.py`

---

## English

### Overview

`file_manager` is a command-line tool to manage projects and scripts under one configured base path.

Main capabilities:
- configure a base path and defaults
- create project folders, script files, and language/area folders
- open projects/scripts in VS Code
- search projects/scripts
- delete projects/scripts

### Requirements

- Python 3.10+
- VS Code CLI (`code`) in `PATH` (for `open` and auto-open features)
- Git in `PATH` (when creating projects with git initialization)

### Run the CLI

```bash
python main.py <command> [options]
```

Check version:

```bash
python main.py --version
```

### Command and Flag Reference (Complete)

Top-level commands:

- `config`
- `open`
- `create`
- `search`
- `delete`

---

### 1) `config`

Syntax:

```bash
python main.py config <action> [action-options]
```

Actions:

#### a) `set-path`

Sets the main root path used by the program.

```bash
python main.py config set-path <value> [--absolute-path|-ap] [--relative-path|-rp]
```

Arguments and flags:
- `<value>`: path value to save
- `--absolute-path`, `-ap`: treat `<value>` as absolute path (default behavior)
- `--relative-path`, `-rp`: treat `<value>` as relative to current working directory

Examples:

```bash
python main.py config set-path "C:/workspace/file-manager" --absolute-path
python main.py config set-path workspace/file-manager --relative-path
```

#### b) `set-project-open`

Sets project open behavior.

```bash
python main.py config set-project-open {files|git} [--true|-t] [--false|-f]
```

Arguments and flags:
- `files`: config key for auto-opening project files/folder
- `git`: config key for git initialization behavior
- `--true`, `-t`: set selected config to `true`
- `--false`, `-f`: set selected config to `false`

Examples:

```bash
python main.py config set-project-open files --true
python main.py config set-project-open git --false
```

#### c) `set-project-extension`

Sets default extension for created project main files.

```bash
python main.py config set-project-extension <value>
```

Example:

```bash
python main.py config set-project-extension .py
python main.py config set-project-extension js
```

#### d) `set-script-open`

Sets script open behavior.

```bash
python main.py config set-script-open {files} [--true|-t] [--false|-f]
```

Arguments and flags:
- `files`: config key for script auto-open behavior
- `--true`, `-t`: set to `true`
- `--false`, `-f`: set to `false`

Example:

```bash
python main.py config set-script-open files --true
```

#### e) `set-script-extension`

Sets default extension for created scripts.

```bash
python main.py config set-script-extension <value>
```

Example:

```bash
python main.py config set-script-extension .py
python main.py config set-script-extension ts
```

---

### 2) `open`

Opens an existing project folder or script file in VS Code.

```bash
python main.py open <open_area> <file_to_open>
```

Arguments:
- `<open_area>`: expected values are `project` or `script`
- `<file_to_open>`: name (or partial name) to locate

Examples:

```bash
python main.py open project my_api
python main.py open script init
```

---

### 3) `create`

Creates a project, script, or folder structure.

```bash
python main.py create {project|script|folder} <create_name> [--extension|-e <ext>] [--init-git|-g] [--no--git|-nog] [--open|-o] [--no-open|-no]
```

Arguments:
- `{project|script|folder}`:
  - `project`: create project directory and starter files
  - `script`: create one script file
  - `folder`: create `<language>/projects` and `<language>/scripts`
- `<create_name>`: resource name

Flags:
- `--extension`, `-e`: custom extension for project main file or script file
- `--init-git`, `-g`: initialize git in created project
- `--no--git`, `-nog`: do not initialize git in created project
- `--open`, `-o`: open created project/script in VS Code
- `--no-open`, `-no`: do not open created project/script

Examples:

```bash
python main.py create project billing_api
python main.py create project billing_api -e .js -g -o
python main.py create project billing_api --no--git --no-open
python main.py create script cleanup_job
python main.py create script cleanup_job --extension ts --no-open
python main.py create folder Python
```

Notes:
- If extension has no dot (for example `js`), the program normalizes it to `.js`.
- For `folder`, known language names come from `file_manager_data.json`; unknown names go to `others`.

---

### 4) `search`

Searches projects/scripts or lists all entries.

```bash
python main.py search {project|script|for_all} [search_name]
```

Arguments:
- `{project|script|for_all}`:
  - `project`: search only projects
  - `script`: search only scripts
  - `for_all`: list all non-empty language areas
- `[search_name]` (optional): partial name filter

Examples:

```bash
python main.py search project
python main.py search project api
python main.py search script
python main.py search script util
python main.py search for_all
python main.py search for_all data
```

---

### 5) `delete`

Deletes projects or scripts.

```bash
python main.py delete <delete_area> <delete_name> [--force|-f [FORCE_DELETE]]
```

Arguments:
- `<delete_area>`: expected values are `project` or `script`
- `<delete_name>`: target name (or partial name)

Flag:
- `--force`, `-f`: skip confirmation prompt (recommended usage: pass flag without value)

Examples:

```bash
python main.py delete project billing_api
python main.py delete project billing_api --force
python main.py delete script cleanup_job
python main.py delete script cleanup_job -f
```

---

### Behavior Notes

- Configuration is persisted in `file_manager_config.json`.
- If multiple results match for `open` or `delete`, the CLI asks you to choose by index.
- If no result is found, a message is printed and execution returns normally.
- Paths are stored as file URIs.

### Repository Files

- `/home/runner/work/gerenciador_de_arquivos/gerenciador_de_arquivos/main.py`: CLI parser and command routing
- `/home/runner/work/gerenciador_de_arquivos/gerenciador_de_arquivos/request_processor.py`: command logic
- `/home/runner/work/gerenciador_de_arquivos/gerenciador_de_arquivos/file_manager_data.json`: language/extension/comment mapping

---

## Português

### Visão Geral

`file_manager` é uma ferramenta de linha de comando para gerenciar projetos e scripts em um único caminho base configurado.

Recursos principais:
- configurar caminho base e padrões
- criar pastas de projeto, arquivos de script e estruturas de pasta por linguagem
- abrir projetos/scripts no VS Code
- buscar projetos/scripts
- excluir projetos/scripts

### Requisitos

- Python 3.10+
- CLI do VS Code (`code`) no `PATH` (para `open` e recursos de abertura automática)
- Git no `PATH` (ao criar projetos com inicialização de git)

### Executar a CLI

```bash
python main.py <comando> [opções]
```

Verificar versão:

```bash
python main.py --version
```

### Referência de Comandos e Flags (Completa)

Comandos de topo:

- `config`
- `open`
- `create`
- `search`
- `delete`

---

### 1) `config`

Sintaxe:

```bash
python main.py config <acao> [opcoes-da-acao]
```

Ações:

#### a) `set-path`

Define o caminho raiz principal usado pelo programa.

```bash
python main.py config set-path <value> [--absolute-path|-ap] [--relative-path|-rp]
```

Argumentos e flags:
- `<value>`: valor do caminho a ser salvo
- `--absolute-path`, `-ap`: trata `<value>` como caminho absoluto (comportamento padrão)
- `--relative-path`, `-rp`: trata `<value>` como relativo ao diretório atual

Exemplos:

```bash
python main.py config set-path "C:/workspace/file-manager" --absolute-path
python main.py config set-path workspace/file-manager --relative-path
```

#### b) `set-project-open`

Define comportamento de abertura para projetos.

```bash
python main.py config set-project-open {files|git} [--true|-t] [--false|-f]
```

Argumentos e flags:
- `files`: chave de configuração para abertura automática de arquivos/pasta do projeto
- `git`: chave de configuração para comportamento de inicialização de git
- `--true`, `-t`: define a configuração selecionada como `true`
- `--false`, `-f`: define a configuração selecionada como `false`

Exemplos:

```bash
python main.py config set-project-open files --true
python main.py config set-project-open git --false
```

#### c) `set-project-extension`

Define a extensão padrão para o arquivo principal de projetos criados.

```bash
python main.py config set-project-extension <value>
```

Exemplo:

```bash
python main.py config set-project-extension .py
python main.py config set-project-extension js
```

#### d) `set-script-open`

Define comportamento de abertura para scripts.

```bash
python main.py config set-script-open {files} [--true|-t] [--false|-f]
```

Argumentos e flags:
- `files`: chave de configuração para abertura automática de scripts
- `--true`, `-t`: define como `true`
- `--false`, `-f`: define como `false`

Exemplo:

```bash
python main.py config set-script-open files --true
```

#### e) `set-script-extension`

Define a extensão padrão para scripts criados.

```bash
python main.py config set-script-extension <value>
```

Exemplo:

```bash
python main.py config set-script-extension .py
python main.py config set-script-extension ts
```

---

### 2) `open`

Abre uma pasta de projeto existente ou arquivo de script no VS Code.

```bash
python main.py open <open_area> <file_to_open>
```

Argumentos:
- `<open_area>`: valores esperados são `project` ou `script`
- `<file_to_open>`: nome (ou parte do nome) para localizar

Exemplos:

```bash
python main.py open project my_api
python main.py open script init
```

---

### 3) `create`

Cria projeto, script ou estrutura de pastas.

```bash
python main.py create {project|script|folder} <create_name> [--extension|-e <ext>] [--init-git|-g] [--no--git|-nog] [--open|-o] [--no-open|-no]
```

Argumentos:
- `{project|script|folder}`:
  - `project`: cria diretório de projeto e arquivos iniciais
  - `script`: cria um arquivo de script
  - `folder`: cria `<linguagem>/projects` e `<linguagem>/scripts`
- `<create_name>`: nome do recurso

Flags:
- `--extension`, `-e`: extensão customizada para arquivo principal do projeto ou arquivo de script
- `--init-git`, `-g`: inicializa git no projeto criado
- `--no--git`, `-nog`: não inicializa git no projeto criado
- `--open`, `-o`: abre projeto/script criado no VS Code
- `--no-open`, `-no`: não abre projeto/script criado

Exemplos:

```bash
python main.py create project billing_api
python main.py create project billing_api -e .js -g -o
python main.py create project billing_api --no--git --no-open
python main.py create script cleanup_job
python main.py create script cleanup_job --extension ts --no-open
python main.py create folder Python
```

Observações:
- Se a extensão vier sem ponto (por exemplo `js`), o programa normaliza para `.js`.
- Para `folder`, nomes de linguagem conhecidos vêm de `file_manager_data.json`; nomes desconhecidos vão para `others`.

---

### 4) `search`

Busca projetos/scripts ou lista todas as entradas.

```bash
python main.py search {project|script|for_all} [search_name]
```

Argumentos:
- `{project|script|for_all}`:
  - `project`: busca apenas projetos
  - `script`: busca apenas scripts
  - `for_all`: lista todas as áreas de linguagem não vazias
- `[search_name]` (opcional): filtro por parte do nome

Exemplos:

```bash
python main.py search project
python main.py search project api
python main.py search script
python main.py search script util
python main.py search for_all
python main.py search for_all data
```

---

### 5) `delete`

Exclui projetos ou scripts.

```bash
python main.py delete <delete_area> <delete_name> [--force|-f [FORCE_DELETE]]
```

Argumentos:
- `<delete_area>`: valores esperados são `project` ou `script`
- `<delete_name>`: nome alvo (ou parte do nome)

Flag:
- `--force`, `-f`: ignora prompt de confirmação (uso recomendado: passar a flag sem valor)

Exemplos:

```bash
python main.py delete project billing_api
python main.py delete project billing_api --force
python main.py delete script cleanup_job
python main.py delete script cleanup_job -f
```

---

### Notas de Comportamento

- A configuração é persistida em `file_manager_config.json`.
- Se múltiplos resultados combinarem em `open` ou `delete`, a CLI pede escolha por índice.
- Se nada for encontrado, uma mensagem é exibida e a execução termina normalmente.
- Caminhos são armazenados como URI de arquivo.

### Arquivos do Repositório

- `/home/runner/work/gerenciador_de_arquivos/gerenciador_de_arquivos/main.py`: parser da CLI e roteamento de comandos
- `/home/runner/work/gerenciador_de_arquivos/gerenciador_de_arquivos/request_processor.py`: lógica dos comandos
- `/home/runner/work/gerenciador_de_arquivos/gerenciador_de_arquivos/file_manager_data.json`: mapeamento de linguagem/extensão/comentário
