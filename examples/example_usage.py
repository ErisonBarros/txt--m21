#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemplos de Uso - Conversor TXT para M21
=========================================

Este arquivo demonstra diferentes formas de usar o conversor,
tanto via linha de comando quanto via API Python.

Autor: Desenvolvido para o repositório ErisonBarros/txt--m21
"""

import sys
import os

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from txt_to_m21_converter import M21Converter
from config import get_patterns_for_brand, add_custom_pattern


def example_1_basic_usage():
    """
    Exemplo 1: Uso básico do conversor
    """
    print("\n" + "="*70)
    print("EXEMPLO 1: Uso Básico")
    print("="*70)
    
    # Cria conversor com arquivo de entrada
    # O arquivo de saída será gerado automaticamente
    converter = M21Converter('sample_input.txt')
    
    # Executa a conversão
    success = converter.convert()
    
    if success:
        print(f"✓ Conversão bem-sucedida!")
        print(f"  Arquivo de saída: {converter.output_file}")
    else:
        print("✗ Erro na conversão")


def example_2_custom_output():
    """
    Exemplo 2: Especificar arquivo de saída personalizado
    """
    print("\n" + "="*70)
    print("EXEMPLO 2: Arquivo de Saída Personalizado")
    print("="*70)
    
    # Especifica tanto entrada quanto saída
    converter = M21Converter(
        input_file='sample_input.txt',
        output_file='meu_arquivo_convertido.m21'
    )
    
    success = converter.convert()
    
    if success:
        print(f"✓ Arquivo salvo em: {converter.output_file}")


def example_3_custom_encoding():
    """
    Exemplo 3: Usar codificação específica
    """
    print("\n" + "="*70)
    print("EXEMPLO 3: Codificação Personalizada")
    print("="*70)
    
    # Especifica codificação (útil para arquivos antigos)
    converter = M21Converter(
        input_file='sample_input.txt',
        encoding='latin-1'
    )
    
    success = converter.convert()
    
    if success:
        print(f"✓ Arquivo processado com codificação: {converter.encoding}")


def example_4_step_by_step():
    """
    Exemplo 4: Processamento passo a passo
    """
    print("\n" + "="*70)
    print("EXEMPLO 4: Processamento Passo a Passo")
    print("="*70)
    
    converter = M21Converter('sample_input.txt')
    
    # Passo 1: Ler arquivo
    print("\n1. Lendo arquivo...")
    content = converter.read_file()
    print(f"   Tamanho: {len(content)} caracteres")
    
    # Passo 2: Processar conteúdo
    print("\n2. Processando conteúdo...")
    lines = converter.process_content()
    print(f"   Linhas geradas: {len(lines)}")
    
    # Passo 3: Validar
    print("\n3. Validando saída...")
    is_valid, issues = converter.validate_output(lines)
    print(f"   Válido: {is_valid}")
    if issues:
        print("   Avisos/Erros:")
        for issue in issues:
            print(f"     - {issue}")
    
    # Passo 4: Salvar
    print("\n4. Salvando arquivo...")
    if is_valid:
        success = converter.save_file(lines)
        if success:
            print(f"   ✓ Salvo em: {converter.output_file}")
    
    # Passo 5: Gerar relatório
    print("\n5. Gerando relatório...")
    report = converter.generate_report()
    print(report)


def example_5_batch_processing():
    """
    Exemplo 5: Processar múltiplos arquivos
    """
    print("\n" + "="*70)
    print("EXEMPLO 5: Processamento em Lote")
    print("="*70)
    
    # Lista de arquivos a processar
    input_files = [
        'arquivo1.txt',
        'arquivo2.txt',
        'arquivo3.txt',
    ]
    
    results = []
    
    for input_file in input_files:
        print(f"\nProcessando: {input_file}")
        
        # Verifica se arquivo existe
        if not os.path.exists(input_file):
            print(f"  ⚠ Arquivo não encontrado, pulando...")
            continue
        
        try:
            converter = M21Converter(input_file)
            success = converter.convert()
            
            results.append({
                'file': input_file,
                'success': success,
                'output': str(converter.output_file) if success else None
            })
            
            if success:
                print(f"  ✓ Convertido: {converter.output_file}")
            else:
                print(f"  ✗ Erro na conversão")
        
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            results.append({
                'file': input_file,
                'success': False,
                'error': str(e)
            })
    
    # Resumo
    print("\n" + "-"*70)
    print("RESUMO DO PROCESSAMENTO EM LOTE")
    print("-"*70)
    successful = sum(1 for r in results if r['success'])
    print(f"Total de arquivos: {len(input_files)}")
    print(f"Convertidos com sucesso: {successful}")
    print(f"Falhas: {len(input_files) - successful}")


def example_6_custom_patterns():
    """
    Exemplo 6: Usar padrões personalizados
    """
    print("\n" + "="*70)
    print("EXEMPLO 6: Padrões Personalizados")
    print("="*70)
    
    # Adiciona um padrão personalizado
    print("\n1. Adicionando padrão personalizado...")
    add_custom_pattern('minha_estacao', r'^CUSTOM\d{4}')
    
    # Obtém padrões para uma marca específica
    print("\n2. Obtendo padrões para Geodetic GD2i...")
    patterns = get_patterns_for_brand('geodetic_gd2i')
    print(f"   Padrões encontrados: {len(patterns)}")
    for pattern in patterns:
        print(f"     - {pattern}")
    
    # Usa o conversor normalmente
    print("\n3. Convertendo arquivo...")
    converter = M21Converter('sample_input.txt')
    
    # Sobrescreve os padrões do conversor com os personalizados
    converter.MEASUREMENT_PATTERNS = patterns
    
    success = converter.convert()
    if success:
        print("   ✓ Conversão concluída com padrões personalizados")


def example_7_error_handling():
    """
    Exemplo 7: Tratamento de erros
    """
    print("\n" + "="*70)
    print("EXEMPLO 7: Tratamento de Erros")
    print("="*70)
    
    # Tenta converter arquivo inexistente
    print("\n1. Tentando converter arquivo inexistente...")
    try:
        converter = M21Converter('arquivo_que_nao_existe.txt')
    except FileNotFoundError as e:
        print(f"   ✓ Erro capturado corretamente: {e}")
    
    # Tenta converter arquivo vazio
    print("\n2. Tentando converter arquivo vazio...")
    
    # Cria arquivo vazio temporário
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        temp_file = f.name
    
    try:
        converter = M21Converter(temp_file)
        success = converter.convert()
        
        if not success:
            print("   ✓ Conversão falhou como esperado para arquivo vazio")
        else:
            print("   ⚠ Conversão bem-sucedida (inesperado)")
    
    finally:
        # Remove arquivo temporário
        os.unlink(temp_file)


def example_8_access_statistics():
    """
    Exemplo 8: Acessar estatísticas da conversão
    """
    print("\n" + "="*70)
    print("EXEMPLO 8: Estatísticas da Conversão")
    print("="*70)
    
    converter = M21Converter('sample_input.txt')
    converter.convert()
    
    # Acessa estatísticas
    stats = converter.statistics
    
    print("\nEstatísticas coletadas:")
    print(f"  Tamanho da entrada:      {stats['input_size']:,} bytes")
    print(f"  Tamanho da saída:        {stats['output_size']:,} bytes")
    print(f"  Linhas processadas:      {stats['lines_processed']}")
    print(f"  Medições encontradas:    {stats['measurements_found']}")
    print(f"  Caracteres removidos:    {stats['chars_removed']:,}")
    
    # Calcula métricas adicionais
    if stats['input_size'] > 0:
        reduction = (1 - stats['output_size'] / stats['input_size']) * 100
        print(f"  Redução de tamanho:      {reduction:.2f}%")


def main():
    """
    Função principal que executa todos os exemplos.
    """
    print("""
╔════════════════════════════════════════════════════════════════════╗
║            EXEMPLOS DE USO - CONVERSOR TXT PARA M21                ║
╚════════════════════════════════════════════════════════════════════╝

Este script demonstra diferentes formas de usar o conversor.
Cada exemplo é independente e pode ser executado separadamente.
""")
    
    # Menu de exemplos
    examples = {
        '1': ('Uso Básico', example_1_basic_usage),
        '2': ('Arquivo de Saída Personalizado', example_2_custom_output),
        '3': ('Codificação Personalizada', example_3_custom_encoding),
        '4': ('Processamento Passo a Passo', example_4_step_by_step),
        '5': ('Processamento em Lote', example_5_batch_processing),
        '6': ('Padrões Personalizados', example_6_custom_patterns),
        '7': ('Tratamento de Erros', example_7_error_handling),
        '8': ('Estatísticas da Conversão', example_8_access_statistics),
    }
    
    print("\nExemplos disponíveis:")
    for key, (title, _) in examples.items():
        print(f"  {key}. {title}")
    print("  0. Executar todos os exemplos")
    print("  q. Sair")
    
    choice = input("\nEscolha um exemplo (ou 'q' para sair): ").strip()
    
    if choice == 'q':
        print("\nSaindo...")
        return
    
    if choice == '0':
        print("\nExecutando todos os exemplos...\n")
        for title, func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"\n✗ Erro no exemplo '{title}': {e}")
    elif choice in examples:
        title, func = examples[choice]
        try:
            func()
        except Exception as e:
            print(f"\n✗ Erro: {e}")
    else:
        print("\n✗ Opção inválida")
    
    print("\n" + "="*70)
    print("Exemplos concluídos!")
    print("="*70)


if __name__ == "__main__":
    main()
