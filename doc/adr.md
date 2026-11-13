# Architecture Decision Records (ADRs): Soundtrack Generator Simplificado

Este documento estabelece as decisões arquiteturais para a versão simplificada do script de geração de trilhas sonoras a partir de prompts em linguagem natural.

---

## ADR 001: Arquitetura de Script Linear e Direta

* **Status:** Aprovado
* **Data:** 13 de Novembro de 2026

### Contexto e Problema
A versão anterior previa uma arquitetura baseada em LangGraph com múltiplos agentes autônomos. No entanto, para um fluxo enxuto onde a intenção do usuário é apenas fornecer um prompt descritivo (ex: *"Crie uma trilha sonora para um mini game ao estilo lofi"*) e obter diretamente os arquivos de saída, a complexidade de grafos de estados e múltiplos nós de IA introduz sobrecarga operacional desnecessária.

### Decisão
Adotar uma arquitetura de **script sequencial direto**, executado em etapas procedurais lineares, mantendo a robustez tecnológica (Python, Ollama e HuggingFace MusicGen) sem a complexidade de orquestração de grafos.

---

## ADR 002: Fluxo de Processamento em Duas Etapas

* **Status:** Aprovado
* **Data:** 13 de Novembro de 2026

### Contexto e Problema
O sistema precisa interpretar o texto abstrato do usuário, transformá-lo em uma faixa de áudio coesa de 60 segundos e documentar o processo.

### Decisão
O script seguirá um pipeline linear de duas fases principais:
1. **Fase de Planejamento e Síntese (Áudio):** O modelo local de linguagem (Ollama) analisa o prompt do usuário para estruturar os parâmetros da trilha (estilo instrumental, ritmo e atmosfera), acionando em seguida o modelo gerador de áudio (`facebook/musicgen-large`) para renderizar a faixa final de 60 segundos de forma limpa e sem vocais.
2. **Fase de Documentação (Markdown):** Um bloco procedural extrai os metadados da execução para compilar e salvar o relatório técnico.

---

## ADR 003: Geração Automatizada de Saídas Vinculadas (`output/`)

* **Status:** Aprovado
* **Data:** 13 de Novembro de 2026

### Contexto e Problema
Os arquivos gerados precisam ser salvos de forma organizada e intuitiva para o usuário final, garantindo rastreabilidade entre a trilha sonora e seus detalhes de processamento.

### Decisão
A cada execução bem-sucedida, o script criará automaticamente o diretório `output/` (caso não exista) e gerará um par de arquivos vinculados utilizando um prefixo com timestamp unificado e um slug descritivo extraído do prompt (ex: `YYYYMMDD_HHMMSS_estilo-lofi.mp3` e `YYYYMMDD_HHMMSS_estilo-lofi.md`). O arquivo `.md` conterá as seções padronizadas de cabeçalho, prompt original, parâmetros musicais inferidos e o caminho do áudio associado.