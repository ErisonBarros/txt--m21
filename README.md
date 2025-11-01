Na qualidade de engenheiro de software sênior, elaborei uma documentação abrangente e clara para o projeto, focando na usabilidade, manutenibilidade e extensibilidade. O README a seguir foi estruturado para ser o ponto de partida ideal para qualquer usuário ou desenvolvedor interessado no projeto.

# Conversor de Arquivos TXT para M21 para Estações Totais

[![Licença](https://img.shields.io/badge/licen%C3%A7a-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-est%C3%A1vel-brightgreen.svg)](./)

## Visão Geral

Este projeto oferece uma solução robusta e automatizada para converter arquivos de dados brutos `.txt`, exportados por diversas marcas de estações totais (como **GD2i, Geodetic, CHC, Topcon e Leica**), para o formato `.m21`. Este formato é amplamente utilizado por softwares de topografia no Brasil, como o **Topograph** e o **TG98SE**.

A necessidade deste conversor surge de uma incompatibilidade comum: os arquivos `.txt` exportados frequentemente contêm caracteres indesejados e não possuem a formatação de quebra de linha exigida pelo padrão `.m21`. O processo manual de correção, que envolve o uso de softwares como Excel e Word, é tedioso, propenso a erros e ineficiente para grandes volumes de dados. Este script automatiza todo o processo, garantindo uma conversão rápida, precisa e confiável.

O desenvolvimento foi inspirado pela metodologia apresentada no [vídeo de Felipe Andrade](https://www.youtube.com/watch?v=S9-Wxy4yhmI&t=1s), que detalha o desafio e uma solução manual.

## Funcionalidades Principais

- **Conversão Automatizada**: Transforma arquivos `.txt` em formato `.m21` com um único comando.
- **Limpeza Inteligente de Dados**: Remove automaticamente caracteres e símbolos desnecessários do início e do fim das linhas de medição.
- **Detecção de Padrões**: Identifica de forma inteligente o início de cada medição para inserir as quebras de linha corretamente.
- **Suporte a Múltiplas Marcas**: Pré-configurado com padrões para as principais marcas de estações totais do mercado.
- **Alta Configurabilidade**: Permite que os usuários adicionem facilmente novos padrões para outras marcas ou modelos através de um arquivo de configuração (`config.py`).
- **Relatórios Detalhados**: Gera um relatório completo ao final de cada conversão, com estatísticas sobre o processo.
- **Tratamento de Erros**: Implementa uma gestão robusta de erros, incluindo a tentativa de múltiplas codificações de arquivo (`UTF-8`, `latin-1`, etc.).
- **Testes Unitários**: Acompanha uma suíte de testes completa para garantir a confiabilidade e a estabilidade do código.

## Pré-requisitos

- **Python 3.8 ou superior**

Nenhuma biblioteca externa é necessária para a execução básica do script. Para desenvolvimento e execução dos testes, a biblioteca `pytest` é recomendada:

```bash
pip install pytest
```

## Como Usar

O uso do conversor é simples e pode ser feito diretamente pela linha de comando.

### Uso Básico

Para converter um arquivo, execute o script `txt_to_m21_converter.py` passando o caminho do arquivo de entrada. O arquivo de saída será criado no mesmo diretório com o sufixo `_converted.m21`.

```bash
python txt_to_m21_converter.py /caminho/para/seu/arquivo.txt
```

### Especificando um Arquivo de Saída

Você também pode especificar o nome e o local do arquivo de saída.

```bash
python txt_to_m21_converter.py entrada.txt saida_convertida.m21
```

### Exemplo de Execução

O projeto inclui arquivos de exemplo no diretório `examples/`.

```bash
# Executa a conversão do arquivo de exemplo
python txt_to_m21_converter.py examples/sample_gd2i.txt
```

Após a execução, um relatório será exibido no terminal, e um arquivo `sample_gd2i_converted.m21` será criado.

## Estrutura do Projeto

```
.txt--m21/
├── txt_to_m21_converter.py # Script principal de conversão
├── config.py               # Arquivo para configurações e padrões personalizados
├── test_converter.py       # Testes unitários para garantir a qualidade
├── README.md               # Este arquivo
├── DEVELOPMENT.md          # Guia de desenvolvimento e arquitetura
├── USAGE.md                # Guia de uso detalhado com exemplos
├── LICENSE                   # Licença do projeto (Apache 2.0)
├── examples/
│   ├── sample_gd2i.txt     # Arquivo de exemplo de entrada
│   └── example_usage.py    # Script com exemplos de uso da API
└── ...
```

## Para Desenvolvedores

Encorajamos contribuições para melhorar e expandir a funcionalidade deste conversor. Se você deseja adicionar suporte a novas estações, corrigir um bug ou propor uma melhoria, por favor, consulte nosso **[Guia de Desenvolvimento (DEVELOPMENT.md)](./DEVELOPMENT.md)**.

### Executando os Testes

Para garantir a integridade do código, execute a suíte de testes:

```bash
python -m pytest test_converter.py -v
```

## Como Contribuir

1.  **Faça um Fork** do repositório.
2.  **Crie uma Branch** para sua modificação (`git checkout -b feature/nova-estacao`).
3.  **Faça o Commit** de suas mudanças (`git commit -am 'Adiciona suporte para a estação X'`).
4.  **Envie para o GitHub** (`git push origin feature/nova-estacao`).
5.  **Abra um Pull Request**.

## Licença

Este projeto está licenciado sob a **Licença Apache 2.0**. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

*Este projeto foi desenvolvido como uma solução de automação para a comunidade de topografia, visando simplificar um fluxo de trabalho crítico e propenso a erros. Agradecimentos a Felipe Andrade pela inspiração.*
