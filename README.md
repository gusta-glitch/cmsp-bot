# CMSP Bot

![Logo](./assets/cmsp_bot-logo.png)

Script de resposta automatica para Centro de Mídias de São Paulo, escrito em Python

**Recursos**

- [x] Ler parametros do CLI
- [x] Login automatico
- [x] Logout automatico
- [x] Navegação até a lista de tarefas
- [x] Resposta automatica (aleatória)
  - [ ] checkbox
  - [x] radio
  - [ ] text
- [ ] Resposta correta
- [ ] Lista de usuários
- [x] Binário
  - [x] Linux
  - [ ] Windows

**Sistemas operacionais**

- [x] Linux
- [ ] Windows

---

## Desenvolvimento

**Dependencias**

| Dependencias locais | Função              |
| ------------------: | :------------------ |
|   chrome / chromuim | Navegador suportado |
|         pyinstaller | Gerar binário       |

| Dependencias do projeto | Função              |
| ----------------------: | :------------------ |
|                selenium | Acessar o navegador |

Verifiique se está na pasta de desenvovimento com o comando `pwd`, se o ultimo diretório for **/cmsp-bot** prosiga.

### No Linux

#### Ambiente virtual

Crie um ambiente virtual com `python -m virtualenv cmsp --activators bash, powershell`.

Entre no ambiente virtual com `source cmsp/bin/activate`.

#### Instalar dependências do projeto

Apos dentro do ambiente virtual, instale as dependência do python com `pip install -r requirements.txt`.

#### Gerar binário

Crie binários usando `pyinstaler --paths cmsp/lib/python*/site-packages -F ./main.py`.
