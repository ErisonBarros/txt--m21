# Resumo do Projeto: Conversor TXT para M21

## Visão Geral do Desenvolvimento

Este documento apresenta um resumo executivo do desenvolvimento do **Conversor de Arquivos TXT para M21**, uma ferramenta automatizada criada para resolver um problema crítico enfrentado por profissionais de topografia no Brasil.

## Contexto e Motivação

Os profissionais de topografia que utilizam estações totais (equipamentos de medição de alta precisão) frequentemente enfrentam um desafio técnico significativo ao processar os dados coletados em campo. Os arquivos `.txt` exportados por essas estações contêm dados de medição válidos, mas em um formato incompatível com os principais softwares de processamento topográfico utilizados no Brasil, como o **Topograph** e o **TG98SE**.

O problema se manifesta de duas formas principais:

1.  **Caracteres Indesejados**: Os arquivos exportados frequentemente contêm símbolos e caracteres especiais (como `***`, `###`, etc.) no início e no final de cada linha de dados. Esses caracteres não fazem parte da medição e impedem o reconhecimento correto dos dados.

2.  **Ausência de Quebras de Linha**: Todas as medições são concatenadas em um único bloco de texto contínuo, sem as quebras de linha necessárias para delimitar cada ponto medido. O formato `.m21` requer que cada medição esteja em uma linha separada.

A solução manual, demonstrada no [vídeo de Felipe Andrade](https://www.youtube.com/watch?v=S9-Wxy4yhmI&t=1s), envolve o uso de **Microsoft Excel** (para remover caracteres indesejados usando a função "Texto para Colunas") e **Microsoft Word** (para inserir quebras de linha usando "Localizar e Substituir"). Este processo é:

-   **Tedioso**: Requer múltiplas etapas manuais.
-   **Propenso a Erros**: Fácil de cometer erros, especialmente com grandes volumes de dados.
-   **Ineficiente**: Consome tempo valioso que poderia ser dedicado à análise dos dados.

## Solução Desenvolvida

O projeto entrega uma solução de software completa e robusta que automatiza todo o processo de conversão. A solução é composta por:

### 1. Script Principal de Conversão (`txt_to_m21_converter.py`)

Este é o núcleo do sistema, implementado como uma classe Python chamada `M21Converter`. A classe encapsula toda a lógica de conversão em um fluxo de trabalho estruturado:

-   **Leitura Inteligente de Arquivos**: Implementa *fallback* automático para diferentes codificações de texto (`UTF-8`, `latin-1`, `ISO-8859-1`, etc.), garantindo que arquivos de diferentes origens sejam lidos corretamente.

-   **Detecção Automática de Padrões**: Utiliza uma biblioteca de expressões regulares (regex) para identificar automaticamente onde cada nova medição começa no texto. O sistema testa múltiplos padrões conhecidos e seleciona o que melhor se aplica ao arquivo em questão.

-   **Limpeza de Dados**: Remove caracteres indesejados do início e do fim de cada linha de medição, aplicando um conjunto configurável de regras de limpeza.

-   **Inserção de Quebras de Linha**: Divide o texto contínuo em linhas individuais, com cada linha representando uma medição completa.

-   **Validação de Saída**: Antes de salvar, o sistema verifica se os dados processados atendem a critérios de qualidade mínimos (presença de dados numéricos, número razoável de linhas, etc.).

-   **Geração de Relatórios**: Produz um relatório detalhado com estatísticas sobre o processo de conversão, incluindo tamanho dos arquivos, número de linhas processadas, caracteres removidos e redução percentual de tamanho.

-   **Sistema de Logging**: Registra todas as operações em um arquivo de log (`txt_to_m21_conversion.log`) para auditoria e depuração.

### 2. Sistema de Configuração (`config.py`)

Para garantir a extensibilidade e a facilidade de manutenção, toda a configuração do sistema foi externalizada em um arquivo dedicado. Este arquivo permite:

-   **Definição de Padrões por Marca**: Um dicionário mapeia marcas de estações totais (GD2i, Topcon, Leica, CHC, etc.) a seus respectivos padrões de formatação. Adicionar suporte a uma nova marca é tão simples quanto adicionar uma nova entrada neste dicionário.

-   **Regras de Limpeza Configuráveis**: Os padrões de caracteres a serem removidos podem ser ajustados sem modificar o código principal.

-   **Parâmetros de Validação**: Critérios de validação (como porcentagem mínima de linhas com dados numéricos) podem ser ajustados para diferentes cenários de uso.

### 3. Suíte de Testes Automatizados (`test_converter.py`)

Seguindo as melhores práticas de engenharia de software, o projeto inclui uma suíte completa de testes unitários. Os testes cobrem:

-   Inicialização e configuração do conversor.
-   Leitura de arquivos com diferentes codificações.
-   Remoção de caracteres indesejados.
-   Detecção de padrões de medição.
-   Validação de dados de saída.
-   Processo de conversão de ponta a ponta.

Os testes podem ser executados com um único comando (`python -m pytest test_converter.py -v`) e garantem que futuras modificações não introduzam regressões.

### 4. Documentação Completa

O projeto é acompanhado por três documentos principais:

-   **README.md**: Apresentação do projeto, funcionalidades principais, instruções de instalação e uso básico.
-   **DEVELOPMENT.md**: Guia para desenvolvedores, explicando a arquitetura do sistema, decisões de design e como estender a funcionalidade.
-   **USAGE.md**: Guia de uso detalhado com exemplos práticos de uso via linha de comando e como biblioteca Python.

### 5. Exemplos Práticos

O diretório `examples/` contém:

-   Arquivos de exemplo de entrada (`.txt`) representando dados reais de estações totais.
-   Scripts Python (`example_usage.py`) demonstrando diferentes formas de usar o conversor, incluindo processamento em lote e acesso a estatísticas.

## Tecnologias e Ferramentas Utilizadas

-   **Linguagem**: Python 3.8+
-   **Bibliotecas Padrão**: `re` (expressões regulares), `logging`, `pathlib`, `unittest`
-   **Controle de Versão**: Git e GitHub
-   **Licença**: Apache License 2.0

## Resultados e Impacto

O conversor desenvolvido oferece os seguintes benefícios:

1.  **Automação Completa**: Elimina a necessidade de intervenção manual, reduzindo o tempo de processamento de horas para segundos.

2.  **Redução de Erros**: A automação elimina erros humanos comuns no processo manual.

3.  **Escalabilidade**: Capaz de processar grandes volumes de dados de forma eficiente.

4.  **Extensibilidade**: Fácil de adaptar para novas marcas e modelos de estações totais.

5.  **Confiabilidade**: Testes automatizados garantem que o sistema funciona corretamente.

6.  **Acessibilidade**: Pode ser usado tanto por usuários técnicos (via linha de comando ou API) quanto por usuários não técnicos (potencial para futura interface gráfica).

## Estrutura de Arquivos do Projeto

```
txt--m21/
├── txt_to_m21_converter.py    # Script principal de conversão
├── config.py                   # Configurações e padrões
├── test_converter.py           # Testes unitários
├── README.md                   # Documentação principal
├── DEVELOPMENT.md              # Guia de desenvolvimento
├── USAGE.md                    # Guia de uso detalhado
├── PROJECT_SUMMARY.md          # Este documento
├── LICENSE                     # Licença Apache 2.0
└── examples/                   # Exemplos e arquivos de teste
    ├── sample_gd2i.txt
    ├── sample_input.txt
    ├── example_usage.py
    └── ...
```

## Próximos Passos e Melhorias Futuras

1.  **Interface Gráfica (GUI)**: Desenvolver uma interface gráfica simples para facilitar o uso por profissionais não técnicos.

2.  **Empacotamento para PyPI**: Publicar o projeto no Python Package Index para instalação via `pip install txt-to-m21`.

3.  **Suporte a Mais Formatos**: Estender o conversor para suportar outros formatos de saída além do `.m21`.

4.  **Integração com Softwares de Topografia**: Desenvolver plugins para integração direta com softwares como Topograph e TG98SE.

5.  **Validação de Dados de Medição**: Implementar verificações mais sofisticadas para detectar anomalias nos dados de medição (ex: coordenadas fora de um intervalo esperado).

## Conclusão

Este projeto representa uma solução completa e profissional para um problema real enfrentado pela comunidade de topografia. Ao automatizar um processo manual tedioso e propenso a erros, o conversor libera tempo valioso dos profissionais e aumenta a confiabilidade do processamento de dados topográficos.

O código foi desenvolvido seguindo as melhores práticas de engenharia de software, com ênfase em qualidade, manutenibilidade e extensibilidade. A documentação abrangente garante que o projeto possa ser facilmente compreendido, utilizado e estendido por outros desenvolvedores e usuários.

---

**Repositório GitHub**: [https://github.com/ErisonBarros/txt--m21](https://github.com/ErisonBarros/txt--m21)

**Referência**: [Vídeo Tutorial de Felipe Andrade](https://www.youtube.com/watch?v=S9-Wxy4yhmI&t=1s)

**Licença**: Apache License 2.0

**Data de Conclusão**: Novembro de 2025
