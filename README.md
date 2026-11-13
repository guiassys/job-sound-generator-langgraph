# 🤖 Job Sound Generator LangGraph (LangGraph + Ollama Local)

Pipeline de Inteligência Artificial autônoma construída com **LangGraph** para criar trilhas sonoras instrumentais de 60 segundos a partir de prompts descritivos em linguagem natural, seguindo uma arquitetura modular baseada em grafos de estados. O sistema opera 100% local utilizando modelos executados via **Ollama** (`qwen3-coder:30b`) e o modelo de áudio HuggingFace (`facebook/musicgen-large`) em ambiente acelerado por GPU (RTX 5080).

---

## 🏗️ Como o Projeto Funciona (Arquitetura)

O projeto utiliza um pipeline sequencial controlado por um Grafo de Estados (*StateGraph*), composto por três nós especializados cujos papéis e diretrizes são desacoplados no arquivo de configuração `config/prompts.yaml`:

1. **Diretor Musical e Arquiteto de Trilhas Sonoras (`composer_agent`):**
   - Analisa o prompt descritivo inserido pelo usuário (ex: *"jogo de aventura medieval"*).
   - Traduz conceitos abstratos em parâmetros instrumentais precisos (BPM, escala, atmosfera e ausência de vocais).
   - Gera um slug descritivo e divide a composição em blocos temporais progressivos (Intro, Meio, Clímax e Encerramento).

2. **Engenheiro de Som Sênior (`sound_engineer_agent`):**
   - Gerencia a exclusividade de recursos de hardware para evitar estouros de VRAM (*CUDA Out of Memory*) entre o Ollama e a GPU.
   - Executa a ferramenta local baseada no `facebook/musicgen-large` para renderizar os blocos parciais de áudio.
   - Aplica técnicas de crossfade e concatenação para entregar uma faixa final homogênea de exatamente 60 segundos exportada em formato `.mp3`.

3. **Editor Técnico e Documentador (`editor_agent`):**
   - Recebe os metadados consolidados da execução, o prompt original, os parâmetros musicais inferidos e os caminhos dos arquivos.
   - Valida e compila a documentação estruturada em Markdown, salvando o relatório final vinculado ao arquivo de áudio.

---

## 📂 Estrutura do Projeto

```text
job-sound-generator-langgraph/
├── config/
│   └── prompts.yaml      # Configuração unificada de papéis, goals, backstories e templates
├── data/                 # Diretório opcional para dados complementares
├── output/               # Diretório onde os arquivos de áudio (.mp3) e relatórios (.md) são salvos com timestamp e slug
├── src/
│   ├── __init__.py
│   ├── state.py          # Contrato de dados compartilhado (TypedDict) que trafega no grafo
│   ├── tools.py          # Ferramenta de síntese de áudio (MusicGen) e gestão de VRAM da GPU
│   ├── nodes.py          # Funções de cada etapa executando via ChatOllama
│   └── graph.py          # Montagem, interligação das arestas e compilação do StateGraph
├── .env                  # Variáveis de ambiente (URL do Ollama e modelo)
├── README.md             # Documentação do projeto
├── .gitignore            # Contrato de arquivos a serem ignorados pelo Git
├── main.py               # Ponto de entrada leve (executa o fluxo e persiste os arquivos)
└── requirements.txt      # Dependências do projeto
```

---

## ⚙️ Pré-requisitos

- **Python 3.10+** (Ambiente WSL / Ubuntu recomendado)
- **FFmpeg** instalado no sistema operacional (`sudo apt install ffmpeg`)
- **Ollama** rodando localmente (ex: via Docker) com o modelo configurado (`qwen3-coder:30b` na porta `11434`).
- **Placa de Vídeo NVIDIA** com suporte CUDA (ex: RTX 5080) para inferência dos modelos locais de linguagem e áudio.

---

## 🚀 Instalação e Configuração

Abra o seu terminal no WSL/Ubuntu e siga os passos abaixo:

1. **Instalar dependências de sistema (FFmpeg)**
   ```bash
   sudo apt update && sudo apt install -y ffmpeg
   ```

2. **Navegue até o diretório do projeto**
   ```bash
   cd ~/devtools/repos/job-sound-generator-langgraph
   ```

3. **Criar e ativar o ambiente virtual Python**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Instalar as dependências do projeto**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## ▶️ Como Executar o Projeto

Certifique-se de que o seu container do Ollama está rodando e acessível na porta `11434`.

Com o ambiente virtual ativado (`source venv/bin/activate`), basta executar o script principal:

```bash
python main.py
```

O pipeline será iniciado, os agentes realizarão o planejamento musical, a síntese de áudio na GPU e a documentação passo a passo. Os arquivos gerados serão salvos automaticamente no diretório `output/` utilizando um prefixo unificado com timestamp e slug de estilo (ex: `20261113_183000_jogo-de-aventura.mp3` e `20261113_183000_jogo-de-aventura.md`).