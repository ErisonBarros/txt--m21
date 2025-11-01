# Guia de Desenvolvimento e Arquitetura

Este documento fornece uma visão aprofundada da arquitetura, das decisões de design e das convenções de codificação utilizadas no **Conversor TXT para M21**. Ele é destinado a desenvolvedores que desejam entender, manter ou estender a funcionalidade do projeto.

## Filosofia de Design

O projeto foi desenvolvido com base nos seguintes princípios:

1.  **Simplicidade e Usabilidade**: A ferramenta deve ser fácil de usar, tanto para o usuário final (via linha de comando) quanto para o desenvolvedor (via API).
2.  **Robustez e Confiabilidade**: O código deve ser resiliente, tratar erros de forma graciosa e ser coberto por testes automatizados.
3.  **Extensibilidade**: A arquitetura deve facilitar a adição de suporte para novos formatos de arquivo e marcas de estação total com o mínimo de esforço.
4.  **Manutenibilidade**: O código deve ser limpo, bem documentado e seguir as melhores práticas do Python (PEP 8).

## Arquitetura do Software

O sistema é composto por três componentes principais, cada um com responsabilidades bem definidas:

### 1. `txt_to_m21_converter.py`: O Núcleo do Conversor

Este é o coração do projeto. Ele contém a classe `M21Converter`, que encapsula toda a lógica de conversão. A classe foi projetada para ser instanciada com os caminhos dos arquivos de entrada e saída e expõe um método principal, `convert()`, que orquestra todo o fluxo de trabalho.

#### Fluxo de Trabalho da Conversão

O método `convert()` executa as seguintes etapas em sequência:

1.  **Inicialização**: Valida os caminhos dos arquivos e define as configurações iniciais.
2.  **Leitura do Arquivo (`read_file`)**: Lê o conteúdo do arquivo de entrada. Implementa uma lógica de *fallback* para tentar diferentes codificações (ex: `utf-8`, `latin-1`) caso a primeira tentativa falhe.
3.  **Divisão em Medições (`split_into_measurements`)**: Esta é a etapa mais crítica. O método remove todas as quebras de linha existentes e, em seguida, utiliza uma lista de padrões de expressão regular (regex) para identificar os pontos onde cada nova medição começa. Uma vez que os pontos de início são encontrados, o conteúdo é dividido nessas posições, criando uma lista de strings, onde cada string é uma medição completa.
4.  **Limpeza de Caracteres (`remove_unwanted_characters`)**: Itera sobre cada medição e aplica um conjunto de padrões regex para remover caracteres indesejados do início e do fim da string.
5.  **Validação da Saída (`validate_output`)**: Antes de salvar, o script realiza uma verificação de sanidade nos dados processados. Ele verifica se linhas foram geradas, se não há um número excessivo de linhas vazias e se os dados contêm informações numéricas, o que é esperado para arquivos de medição.
6.  **Salvamento do Arquivo (`save_file`)**: Escreve as linhas processadas em um novo arquivo `.m21`, adicionando uma quebra de linha após cada medição.
7.  **Geração de Relatório (`generate_report`)**: Coleta estatísticas durante todo o processo (tamanho dos arquivos, número de linhas, caracteres removidos) e gera um relatório formatado que é exibido no console.

### 2. `config.py`: O Centro de Configuração

Para evitar que a lógica de detecção de padrões ficasse "hardcoded" no script principal, foi criado um arquivo de configuração. Isso permite que usuários e desenvolvedores ajustem o comportamento do conversor sem modificar o código principal.

As principais seções do `config.py` são:

-   **`PATTERNS_BY_BRAND`**: Um dicionário que mapeia nomes de marcas (ex: `'geodetic_gd2i'`) a uma lista de padrões regex. Isso permite que o sistema seja facilmente estendido para novas marcas.
-   **`UNWANTED_CHARS_START` e `UNWANTED_CHARS_END`**: Listas de padrões regex para os caracteres que devem ser removidos.
-   **`ENCODINGS`**: Uma lista de codificações de texto a serem tentadas em ordem.
-   **Configurações de Validação e Log**: Parâmetros para ajustar os critérios de validação e o nível de detalhe dos logs.

### 3. `test_converter.py`: A Garantia de Qualidade

Utilizando o framework `unittest` do Python, este arquivo contém uma suíte de testes unitários que cobrem as principais funcionalidades da classe `M21Converter`.

Os testes validam:

-   A inicialização correta do conversor.
-   O tratamento de erros, como arquivos não encontrados.
-   A leitura de arquivos com diferentes codificações.
-   A eficácia da remoção de caracteres indesejados.
-   A precisão da detecção de padrões de medição.
-   O processo de conversão de ponta a ponta.
-   A integração com o arquivo `config.py`.

## Como Adicionar Suporte a uma Nova Estação Total

O processo para estender o suporte a uma nova marca ou modelo de estação total é simples e direto:

1.  **Analise o Arquivo `.txt`**: Abra um arquivo de exemplo exportado pela nova estação e identifique:
    *   O padrão de caracteres que marca o início de cada linha de medição (ex: `PONTO_`, `EST:`, etc.).
    *   Quaisquer caracteres ou símbolos indesejados que aparecem no início ou no fim das linhas.

2.  **Crie um Padrão Regex**: Traduza o padrão de início de medição em uma expressão regular. Ferramentas online como o [Regex101](https://regex101.com/) podem ser muito úteis.

3.  **Atualize o `config.py`**: Abra o arquivo `config.py` e adicione uma nova entrada ao dicionário `PATTERNS_BY_BRAND`.

    ```python
    # Exemplo de adição para uma marca "NovaMarca"
    PATTERNS_BY_BRAND = {
        # ... padrões existentes
        'novamarca': [
            r'^PONTO_\d+',  # Padrão 1 para a NovaMarca
            r'^EST:\d+',    # Padrão 2 para a NovaMarca
        ],
    }
    ```

4.  **Teste**: Crie um arquivo de exemplo para a nova marca no diretório `examples/` e execute o conversor para validar se a conversão funciona como esperado.

5.  **(Opcional, mas recomendado)** Adicione um novo teste unitário em `test_converter.py` para automatizar a verificação do novo formato.

## Convenções de Código

-   **Estilo de Código**: O projeto segue estritamente o guia de estilo **PEP 8**.
-   **Docstrings**: Todas as classes e funções públicas possuem *docstrings* no formato Google Style para explicar seu propósito, argumentos e valores de retorno.
-   **Type Hinting**: O código faz uso extensivo de *type hints* (PEP 484) para melhorar a clareza e permitir a verificação estática de tipos.
-   **Logging**: O logging é utilizado para fornecer feedback sobre o processo de conversão, com diferentes níveis (INFO, WARNING, ERROR) para diferentes tipos de mensagem.

## Futuras Melhorias

-   **Interface Gráfica (GUI)**: Desenvolver uma interface gráfica simples (usando Tkinter, PyQt ou uma aplicação web) para facilitar o uso por usuários não técnicos.
-   **Seleção de Marca via Linha de Comando**: Adicionar um argumento (`--brand`) para permitir que o usuário especifique a marca da estação, otimizando a detecção de padrões.
-   **Plugin de Auto-Update**: Implementar um mecanismo para que o script possa buscar novas definições de padrões de um repositório central.
-   **Empacotamento para PyPI**: Empacotar o projeto para que possa ser facilmente instalado via `pip`.
