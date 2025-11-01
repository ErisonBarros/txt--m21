# Guia de Uso Detalhado

Este guia oferece instruções detalhadas e exemplos práticos para ajudá-lo a aproveitar ao máximo o **Conversor TXT para M21**.

## Sumário

1.  [Instalação](#1-instalação)
2.  [Uso via Linha de Comando](#2-uso-via-linha-de-comando)
    -   [Conversão Básica](#conversão-básica)
    -   [Especificando Arquivo de Saída](#especificando-arquivo-de-saída)
    -   [Argumentos e Opções](#argumentos-e-opções)
3.  [Uso como Biblioteca Python (API)](#3-uso-como-biblioteca-python-api)
    -   [Exemplo 1: Conversão Simples](#exemplo-1-conversão-simples)
    -   [Exemplo 2: Processamento em Lote](#exemplo-2-processamento-em-lote)
    -   [Exemplo 3: Acessando Estatísticas](#exemplo-3-acessando-estatísticas)
4.  [Personalização](#4-personalização)
    -   [Adicionando Padrões para Novas Estações](#adicionando-padrões-para-novas-estações)
5.  [Solução de Problemas](#5-solução-de-problemas)

---

## 1. Instalação

O script foi projetado para ser executado com uma instalação padrão do **Python 3.8 ou superior**. Nenhuma dependência externa é necessária.

1.  **Clone o repositório** ou faça o download dos arquivos:

    ```bash
    git clone https://github.com/ErisonBarros/txt--m21.git
    cd txt--m21
    ```

2.  (Opcional) Para desenvolvimento, instale o `pytest`:

    ```bash
    pip install pytest
    ```

## 2. Uso via Linha de Comando

A maneira mais comum de usar o conversor é através de um terminal ou prompt de comando.

### Conversão Básica

Esta é a forma mais simples de usar. Forneça apenas o caminho para o arquivo de entrada. O script criará automaticamente um arquivo de saída no mesmo diretório, com o mesmo nome do original, mas com o sufixo `_converted.m21`.

**Comando:**

```bash
python txt_to_m21_converter.py /caminho/completo/para/dados_brutos.txt
```

**Resultado:**

-   Um arquivo chamado `dados_brutos_converted.m21` será criado.
-   Um relatório de conversão será exibido no terminal.
-   Um arquivo de log `txt_to_m21_conversion.log` será gerado com detalhes do processo.

### Especificando Arquivo de Saída

Se você deseja ter controle total sobre o nome e o local do arquivo de saída, forneça-o como o segundo argumento.

**Comando:**

```bash
python txt_to_m21_converter.py entrada.txt C:\Topografia\Projetos\projeto_final.m21
```

**Resultado:**

-   O arquivo convertido será salvo exatamente no caminho especificado.

### Argumentos e Opções

O script aceita os seguintes argumentos posicionais:

-   `arquivo_entrada.txt` (obrigatório): O caminho para o arquivo `.txt` a ser convertido.
-   `[arquivo_saida.m21]` (opcional): O caminho para o arquivo `.m21` de saída.

## 3. Uso como Biblioteca Python (API)

A classe `M21Converter` pode ser importada e utilizada em seus próprios scripts Python, o que é ideal para automação e integração com outros sistemas.

### Exemplo 1: Conversão Simples

```python
from txt_to_m21_converter import M21Converter

try:
    # Inicializa o conversor
    converter = M21Converter("examples/sample_gd2i.txt")
    
    # Executa a conversão
    success = converter.convert()
    
    if success:
        print(f"Conversão concluída com sucesso! Arquivo salvo em: {converter.output_file}")
    else:
        print("A conversão falhou. Verifique o log para mais detalhes.")

except FileNotFoundError:
    print("Erro: O arquivo de entrada não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
```

### Exemplo 2: Processamento em Lote

Este exemplo mostra como converter múltiplos arquivos em um diretório.

```python
import os
from txt_to_m21_converter import M21Converter

directory = "/caminho/para/seus/arquivos_txt/"

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        input_path = os.path.join(directory, filename)
        print(f"Processando {input_path}...")
        
        try:
            converter = M21Converter(input_path)
            converter.convert()
        except Exception as e:
            print(f"  Erro ao processar {filename}: {e}")
```

### Exemplo 3: Acessando Estatísticas

Você pode acessar os dados da conversão através do atributo `statistics`.

```python
from txt_to_m21_converter import M21Converter

converter = M21Converter("examples/sample_gd2i.txt")
if converter.convert():
    stats = converter.statistics
    print("\n--- Estatísticas da Conversão ---")
    print(f"Linhas processadas: {stats["lines_processed"]}")
    print(f"Caracteres removidos: {stats["chars_removed"]}")
    print(f"Tamanho do arquivo de saída: {stats["output_size"]} bytes")
```

## 4. Personalização

Se o seu equipamento exporta dados em um formato que não é reconhecido automaticamente, você pode facilmente adicionar suporte a ele.

### Adicionando Padrões para Novas Estações

1.  Abra o arquivo `config.py`.
2.  Localize o dicionário `PATTERNS_BY_BRAND`.
3.  Adicione uma nova chave com o nome da sua estação (em letras minúsculas) e uma lista contendo um ou mais padrões de expressão regular (regex) que identificam o início de uma linha de medição.

**Exemplo:**

Suponha que sua estação gere linhas que começam com `STN-` seguido por números.

```python
# Em config.py
PATTERNS_BY_BRAND = {
    # ... outros padrões
    "minha_estacao_xyz": [
        r"^STN-\d+"  # Regex para "STN-" seguido por um ou mais dígitos
    ]
}
```

O conversor usará automaticamente esses novos padrões na próxima execução.

## 5. Solução de Problemas

-   **Erro "Arquivo não encontrado"**: Verifique se o caminho para o arquivo de entrada está correto e se você tem permissão para acessá-lo.

-   **Conversão Falha ou Arquivo de Saída Vazio**: Isso geralmente significa que o script não conseguiu identificar um padrão de medição no seu arquivo. Verifique o arquivo de log (`txt_to_m21_conversion.log`) para mensagens de aviso (`WARNING`). A solução mais provável é [adicionar um padrão personalizado](#adicionando-padrões-para-novas-estações) em `config.py`.

-   **Caracteres Estranhos no Arquivo de Saída**: Isso pode ser um problema de codificação de caracteres. O script tenta `utf-8` e `latin-1` automaticamente, mas você pode adicionar outras codificações à lista `ENCODINGS` no arquivo `config.py`.

-   **O Script Remove Dados Válidos**: Se o script está sendo muito agressivo e removendo partes importantes dos seus dados, você pode ajustar os padrões `UNWANTED_CHARS_START` e `UNWANTED_CHARS_END` em `config.py` para serem mais específicos.
