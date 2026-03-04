# File Manager CLI

- **Version:** 2.0.0  
- **Author:** [João Vítor Lira (Lirovsk)](https://github.com/Lirovsk)
- **Last added:** Ability to create scripts and project with diferent extensions than the default.

---

## English Documentation

### Overview

`file_manager` is a command-line tool that helps you quickly start projects and scripts by automating repetitive setup tasks.

With this tool, you can:

- Save default paths for **projects** and **scripts**
- Set default file extensions for each area
- Create project folders with starter files
- Create standalone scripts
- Search created items
- Open projects/scripts directly in VS Code

### Requirements

- Python 3.10+ (recommended)
- VS Code CLI available in PATH (`code` command)
- Git installed (optional, only needed when project git initialization is enabled)

### Project Structure

- `main.py`: command-line entry point
- `request_processor.py`: command handlers and business logic
- `file_manager_config.json`: generated configuration file

### Installation / Setup

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Run commands using:

```bash
python main.py <command> [options]
```

### CLI Commands

#### 1) Configure defaults

Set base paths:

```bash
python main.py config set-project-path "C:/path/to/projects" --absolute-path
python main.py config set-script-path "C:/path/to/scripts" --absolute-path
```

Set default extensions:

```bash
python main.py config set-project-extension .py
python main.py config set-script-extension .py
```

Set open/behavior flags:

```bash
python main.py config set-project-open git true
python main.py config set-project-open open_files true
python main.py config set-script-open open_files true
```

#### 2) Create

Create a project (uses configured extension by default):

```bash
python main.py create project my_project
```

Create a project with a custom extension:

```bash
python main.py create project my_project --extension .js
```

Create a script:

```bash
python main.py create script my_script
python main.py create script my_script --extension .py
```

#### 3) Open

Open a project or script in VS Code:

```bash
python main.py open project my_project
python main.py open script my_script.py
```

#### 4) Search

Search by name:

```bash
python main.py search project my
python main.py search script test
```

List all items:

```bash
python main.py search project --all
python main.py search script --all
```

### Notes

- If `file_manager_config.json` does not exist, it is created automatically.
- Paths must point to valid existing directories.
- `open` and some `create` features depend on the `code` command being available.

### Planned Improvements

- Virtual environment creation
- Automatic dependency installation
- More project templates

---

## Documentação em Português

### Visão Geral

O `file_manager` é uma ferramenta de linha de comando para acelerar a criação de projetos e scripts, automatizando tarefas repetitivas de início.

Com essa ferramenta, você pode:

- Salvar caminhos padrão para **projetos** e **scripts**
- Definir extensões padrão para cada área
- Criar pastas de projeto com arquivos iniciais
- Criar scripts avulsos
- Buscar itens criados
- Abrir projetos/scripts diretamente no VS Code

### Requisitos

- Python 3.10+ (recomendado)
- CLI do VS Code no PATH (comando `code`)
- Git instalado (opcional, usado quando a inicialização de git estiver habilitada)

### Estrutura do Projeto

- `main.py`: ponto de entrada da linha de comando
- `request_processor.py`: processamento dos comandos e regras de negócio
- `file_manager_config.json`: arquivo de configuração gerado automaticamente

### Instalação / Uso Inicial

1. Faça clone ou download deste repositório.
2. Abra um terminal na pasta do projeto.
3. Execute os comandos com:

```bash
python main.py <comando> [opções]
```

### Comandos da CLI

#### 1) Configurar padrões

Definir caminhos base:

```bash
python main.py config set-project-path "C:/caminho/para/projetos" --absolute-path
python main.py config set-script-path "C:/caminho/para/scripts" --absolute-path
```

Definir extensões padrão:

```bash
python main.py config set-project-extension .py
python main.py config set-script-extension .py
```

Definir opções de comportamento/abertura:

```bash
python main.py config set-project-open git true
python main.py config set-project-open open_files true
python main.py config set-script-open open_files true
```

#### 2) Criar

Criar um projeto (usa a extensão configurada por padrão):

```bash
python main.py create project meu_projeto
```

Criar um projeto com extensão personalizada:

```bash
python main.py create project meu_projeto --extension .js
```

Criar um script:

```bash
python main.py create script meu_script
python main.py create script meu_script --extension .py
```

#### 3) Abrir

Abrir um projeto ou script no VS Code:

```bash
python main.py open project meu_projeto
python main.py open script meu_script.py
```

#### 4) Buscar

Buscar por nome:

```bash
python main.py search project meu
python main.py search script teste
```

Listar todos os itens:

```bash
python main.py search project --all
python main.py search script --all
```

### Observações

- Se o `file_manager_config.json` não existir, ele será criado automaticamente.
- Os caminhos configurados precisam apontar para diretórios válidos.
- O comando `open` e algumas ações de `create` dependem do comando `code` disponível no sistema.

### Melhorias Planejadas

- Criação de ambiente virtual
- Instalação automática de dependências
- Mais templates de projeto
