# CMSP Bot

![Logo](./assets/cmsp_bot-logo.png)

Script de resposta automática para Centro de Mídias de São Paulo, escrito em Python

**Recursos**

- [x] Ler parâmetros do CLI
- [x] Login automático
- [x] Logout automático
- [x] Navegação até a lista de tarefas
- [x] Resposta automática (aleatória)
  - [x] checkbox
  - [x] radio
  - [x] text
- [ ] Resposta correta
- [ ] Lista de usuários
- [x] Binário
  - [x] Linux
  - [ ] Windows

---

## Uso

### No Linux

Para usar o script _python_ digite `python ./src/main.py [ARGUMENTOS]` no terminal.

Para usar o _binário_ digite `cmsp-bot [ARGUMENTOS]` no terminal

> O arquivo binário não tem dependências adicionais, alem do navegado suportado.

### Lista de argumentos

| Argumento                     | Descrição                            | Exemplo                                 |
| ----------------------------- | ------------------------------------ | --------------------------------------- |
| `-h`, `--help` : `[Bool]`     | Mostra o menu de ajuda e sai         | `-h`                                    |
| `-V`, `--version` : `[Bool]`  | Mostra a versão do programa e sai    | `-V`                                    |
| `-u`, `--ra` : `[Str, Int]`   | RA do usuário, com dígito            | `-u 123456789-0`                        |
| `-c`, `--uf` : `[Str]`        | UF do usuário                        | `-c sp`                                 |
| `-p`, `--password` : `[Str]`  | Código de acesso do usuário          | `-p a1b2c3b4`                           |
| `-t`, `--team` : `[Str, Int]` | Classe onde se encontra as tarefas   | `-t "[CLASSE] Turma 1°A Escola"` ou     |
| `-a`, `--amount` : `[Int]`    | Quantidade de tarefas para responder | `-a 50` ou `-a 0` para todas as tarefas |

## Desenvolvimento

**Dependências**

| Dependências locais | Função              |
| ------------------: | :------------------ |
|   chrome / chromuim | Navegador suportado |
|         pyinstaller | Gerar binário       |

| Dependências do projeto | Função              |
| ----------------------: | :------------------ |
|                selenium | Acessar o navegador |

Verifique se está na pasta de desenvolvimento com o comando `pwd`, se o ultimo diretório for **/cmsp-bot** prosiga.

### No Linux

#### Ambiente virtual

Crie um ambiente virtual com `python -m virtualenv cmsp --activators bash, powershell`.

Entre no ambiente virtual com `source cmsp/bin/activate`.

#### Instalar dependências do projeto

Apos dentro do ambiente virtual, instale as dependências do python com `pip install -r requirements.txt`.

#### Gerar binário

Crie binários usando `pyinstaler --paths cmsp/lib/python*/site-packages -F ./src/main.py`.
