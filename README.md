# VRisingManager

Ferramenta desenvolvida para facilitar o gerenciamento de servidores dedicados de **V Rising**, oferecendo automação de tarefas administrativas, monitoramento e utilitários para simplificar a administração do servidor.

## Funcionalidades

* Verificação de status do servidor
* Monitoramento de jogadores online
* Gerenciamento de processos do servidor
* Automação de tarefas administrativas
* Interface simplificada para operações comuns
* Sistema modular para futuras expansões

## Tecnologias Utilizadas

* Python
* SteamCMD
* APIs e ferramentas de gerenciamento de servidores
* Interface gráfica (quando aplicável)

## Estrutura do Projeto

```text
projeto_VRisingManager/
├── src/
├── core/
├── services/
├── utils/
├── assets/
├── config/
├── build/
├── logs/
└── main.py
```

## Instalação

Clone o repositório:

```bash
git clone git@github.com:NiktoHixto/projeto_VrisingManager.git
```

Acesse a pasta do projeto:

```bash
cd projeto_VrisingManager
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

## Build Executável

Caso o projeto utilize PyInstaller:

```bash
pyinstaller VRisingManager.spec
```

O executável será gerado na pasta:

```text
dist/
```

## Objetivos

Este projeto foi criado para:

* Centralizar o gerenciamento de servidores V Rising
* Reduzir tarefas manuais repetitivas
* Facilitar atualizações e manutenção
* Servir como estudo de arquitetura modular em Python

## Contribuição

Contribuições são bem-vindas. Sinta-se à vontade para abrir Issues e Pull Requests.

## Licença

Este projeto está licenciado sob a licença MIT.
