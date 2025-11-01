#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arquivo de Configuração - Conversor TXT para M21
================================================

Este arquivo contém configurações personalizáveis para o conversor,
permitindo ajustes para diferentes marcas e modelos de estações totais.

Como Usar:
----------
1. Identifique o padrão específico da sua estação total
2. Adicione novos padrões às listas abaixo
3. Execute o conversor normalmente

Estrutura de Padrões:
--------------------
Os padrões usam expressões regulares (regex) do Python.
Referência: https://docs.python.org/3/library/re.html

Exemplos de Padrões Comuns:
---------------------------
- ^\d{4}     : Inicia com 4 dígitos
- ^[A-Z]{2}  : Inicia com 2 letras maiúsculas
- \d+        : Um ou mais dígitos
- [A-Z]+     : Uma ou mais letras maiúsculas
"""

# ==============================================================================
# PADRÕES DE DETECÇÃO DE MEDIÇÕES
# ==============================================================================

# Padrões específicos por marca de estação total
PATTERNS_BY_BRAND = {
    
    # Geodetic GD2i
    'geodetic_gd2i': [
        r'^\d{2}[A-Z]{2}\d{4}',  # Exemplo: 02GZ0001
        r'^GZ\d{6}',              # Exemplo: GZ000001
    ],
    
    # Topcon
    'topcon': [
        r'^PT\d+',                # Exemplo: PT001, PT002
        r'^\d{4}\s+\d{4}',        # Exemplo: 0001 0002
    ],
    
    # Leica
    'leica': [
        r'^P\d+',                 # Exemplo: P001, P002
        r'^\d{1,4}[A-Z]',         # Exemplo: 1A, 123B
    ],
    
    # CHC
    'chc': [
        r'^[A-Z]{2}\d{4,6}',      # Exemplo: AB123456
        r'^\d{4,6}',              # Exemplo: 123456
    ],
    
    # Padrões genéricos (usados quando marca não é especificada)
    'generic': [
        r'^\d{2}[A-Z]{2}\d{4}',
        r'^[A-Z]{2}\d{4,6}',
        r'^\d{4,6}[A-Z]',
        r'^PT\d+',
        r'^P\d+',
        r'^\d{1,4}\s+\d{1,4}',
    ]
}

# ==============================================================================
# CARACTERES INDESEJADOS
# ==============================================================================

# Caracteres que devem ser removidos do INÍCIO das linhas
UNWANTED_CHARS_START = [
    r'^\s*[^\d\w]+',      # Remove caracteres especiais e espaços no início
    r'^[*#@$%&]+',        # Remove símbolos específicos
    r'^[\[\](){}]+',      # Remove parênteses e colchetes
    r'^[;:,\.]+',         # Remove pontuação
]

# Caracteres que devem ser removidos do FIM das linhas
UNWANTED_CHARS_END = [
    r'[^\d\w]+\s*$',      # Remove caracteres especiais e espaços no final
    r'[*#@$%&]+$',        # Remove símbolos específicos
    r'[\[\](){}]+$',      # Remove parênteses e colchetes
    r'[;:,\.]+$',         # Remove pontuação
]

# ==============================================================================
# CONFIGURAÇÕES DE CODIFICAÇÃO
# ==============================================================================

# Codificações a serem tentadas (em ordem)
ENCODINGS = [
    'utf-8',
    'latin-1',
    'iso-8859-1',
    'cp1252',
    'ascii'
]

# ==============================================================================
# CONFIGURAÇÕES DE VALIDAÇÃO
# ==============================================================================

# Tamanho mínimo de uma linha válida (em caracteres)
MIN_LINE_LENGTH = 5

# Porcentagem mínima de linhas que devem conter números
MIN_NUMERIC_LINES_PERCENT = 0.3  # 30%

# Porcentagem máxima de linhas vazias permitidas
MAX_EMPTY_LINES_PERCENT = 0.5  # 50%

# ==============================================================================
# CONFIGURAÇÕES DE LOG
# ==============================================================================

# Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = 'INFO'

# Nome do arquivo de log
LOG_FILE = 'txt_to_m21_conversion.log'

# Formato do log
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# ==============================================================================
# CONFIGURAÇÕES AVANÇADAS
# ==============================================================================

# Número mínimo de ocorrências de um padrão para considerá-lo válido
MIN_PATTERN_OCCURRENCES = 2

# Tamanho máximo de arquivo a ser processado (em MB)
# Use 0 para sem limite
MAX_FILE_SIZE_MB = 100

# Criar backup do arquivo original antes de converter
CREATE_BACKUP = True

# Sufixo do arquivo de backup
BACKUP_SUFFIX = '.backup'

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def get_patterns_for_brand(brand: str = 'generic') -> list:
    """
    Retorna os padrões de detecção para uma marca específica.
    
    Args:
        brand (str): Nome da marca (geodetic_gd2i, topcon, leica, chc, generic)
    
    Returns:
        list: Lista de padrões regex
    """
    brand = brand.lower()
    return PATTERNS_BY_BRAND.get(brand, PATTERNS_BY_BRAND['generic'])


def add_custom_pattern(brand: str, pattern: str):
    """
    Adiciona um padrão personalizado para uma marca.
    
    Args:
        brand (str): Nome da marca
        pattern (str): Padrão regex a ser adicionado
    """
    if brand not in PATTERNS_BY_BRAND:
        PATTERNS_BY_BRAND[brand] = []
    
    if pattern not in PATTERNS_BY_BRAND[brand]:
        PATTERNS_BY_BRAND[brand].append(pattern)


def validate_config():
    """
    Valida as configurações definidas neste arquivo.
    
    Returns:
        tuple: (válido, mensagens de erro)
    """
    errors = []
    
    # Valida porcentagens
    if not 0 <= MIN_NUMERIC_LINES_PERCENT <= 1:
        errors.append("MIN_NUMERIC_LINES_PERCENT deve estar entre 0 e 1")
    
    if not 0 <= MAX_EMPTY_LINES_PERCENT <= 1:
        errors.append("MAX_EMPTY_LINES_PERCENT deve estar entre 0 e 1")
    
    # Valida tamanho mínimo de linha
    if MIN_LINE_LENGTH < 1:
        errors.append("MIN_LINE_LENGTH deve ser maior que 0")
    
    # Valida padrões
    if not PATTERNS_BY_BRAND:
        errors.append("Nenhum padrão de detecção definido")
    
    return len(errors) == 0, errors


# ==============================================================================
# EXEMPLOS DE USO
# ==============================================================================

"""
Exemplo 1: Usar padrões específicos de uma marca
-------------------------------------------------
from config import get_patterns_for_brand

patterns = get_patterns_for_brand('geodetic_gd2i')
# Usar esses padrões no conversor


Exemplo 2: Adicionar padrão personalizado
------------------------------------------
from config import add_custom_pattern

add_custom_pattern('minha_estacao', r'^CUSTOM\d{4}')


Exemplo 3: Validar configurações
---------------------------------
from config import validate_config

is_valid, errors = validate_config()
if not is_valid:
    print("Erros de configuração:", errors)
"""

if __name__ == "__main__":
    # Testa a configuração quando executado diretamente
    print("Testando configurações...")
    is_valid, errors = validate_config()
    
    if is_valid:
        print("✓ Configurações válidas!")
        print(f"\nMarcas configuradas: {', '.join(PATTERNS_BY_BRAND.keys())}")
        print(f"Total de padrões: {sum(len(p) for p in PATTERNS_BY_BRAND.values())}")
    else:
        print("✗ Erros encontrados:")
        for error in errors:
            print(f"  - {error}")
