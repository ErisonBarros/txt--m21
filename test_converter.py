#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes Unitários - Conversor TXT para M21
==========================================

Este arquivo contém testes automatizados para validar o funcionamento
do conversor de arquivos TXT para M21.

Como Executar:
--------------
    python test_converter.py
    
    ou
    
    python -m pytest test_converter.py -v

Requisitos:
-----------
    pip install pytest

Autor: Desenvolvido para o repositório ErisonBarros/txt--m21
"""

import unittest
import tempfile
import os
from pathlib import Path
from txt_to_m21_converter import M21Converter


class TestM21Converter(unittest.TestCase):
    """
    Classe de testes para o conversor M21.
    """
    
    def setUp(self):
        """
        Configuração executada antes de cada teste.
        Cria arquivos temporários para testes.
        """
        self.temp_dir = tempfile.mkdtemp()
        self.test_input_file = Path(self.temp_dir) / "test_input.txt"
        self.test_output_file = Path(self.temp_dir) / "test_output.m21"
    
    def tearDown(self):
        """
        Limpeza executada após cada teste.
        Remove arquivos temporários.
        """
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, content: str) -> Path:
        """
        Cria um arquivo de teste com conteúdo específico.
        
        Args:
            content (str): Conteúdo do arquivo
        
        Returns:
            Path: Caminho do arquivo criado
        """
        with open(self.test_input_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return self.test_input_file
    
    # ==========================================================================
    # TESTES DE INICIALIZAÇÃO
    # ==========================================================================
    
    def test_converter_initialization(self):
        """
        Testa se o conversor é inicializado corretamente.
        """
        self.create_test_file("test content")
        converter = M21Converter(str(self.test_input_file))
        
        self.assertEqual(converter.input_file, self.test_input_file)
        self.assertTrue(converter.output_file.suffix == '.m21')
    
    def test_file_not_found(self):
        """
        Testa se o conversor lança exceção quando arquivo não existe.
        """
        with self.assertRaises(FileNotFoundError):
            M21Converter("arquivo_inexistente.txt")
    
    def test_custom_output_file(self):
        """
        Testa se o conversor aceita arquivo de saída personalizado.
        """
        self.create_test_file("test content")
        custom_output = Path(self.temp_dir) / "custom_output.m21"
        converter = M21Converter(str(self.test_input_file), str(custom_output))
        
        self.assertEqual(converter.output_file, custom_output)
    
    # ==========================================================================
    # TESTES DE LEITURA DE ARQUIVO
    # ==========================================================================
    
    def test_read_file_utf8(self):
        """
        Testa leitura de arquivo com codificação UTF-8.
        """
        content = "Teste de conteúdo com acentuação: áéíóú"
        self.create_test_file(content)
        
        converter = M21Converter(str(self.test_input_file))
        read_content = converter.read_file()
        
        self.assertEqual(read_content, content)
        self.assertEqual(converter.statistics['input_size'], len(content))
    
    def test_read_empty_file(self):
        """
        Testa leitura de arquivo vazio.
        """
        self.create_test_file("")
        
        converter = M21Converter(str(self.test_input_file))
        read_content = converter.read_file()
        
        self.assertEqual(read_content, "")
        self.assertEqual(converter.statistics['input_size'], 0)
    
    # ==========================================================================
    # TESTES DE REMOÇÃO DE CARACTERES
    # ==========================================================================
    
    def test_remove_unwanted_characters_start(self):
        """
        Testa remoção de caracteres no início da linha.
        """
        self.create_test_file("test")
        converter = M21Converter(str(self.test_input_file))
        
        test_cases = [
            ("***ABC123", "ABC123"),
            ("###XYZ789", "XYZ789"),
            ("   DATA123", "DATA123"),
            ("@@@PT001", "PT001"),
        ]
        
        for input_line, expected in test_cases:
            result = converter.remove_unwanted_characters(input_line)
            self.assertEqual(result, expected, 
                           f"Falhou para entrada: {input_line}")
    
    def test_remove_unwanted_characters_end(self):
        """
        Testa remoção de caracteres no final da linha.
        """
        self.create_test_file("test")
        converter = M21Converter(str(self.test_input_file))
        
        test_cases = [
            ("ABC123***", "ABC123"),
            ("XYZ789###", "XYZ789"),
            ("DATA123   ", "DATA123"),
            ("PT001@@@", "PT001"),
        ]
        
        for input_line, expected in test_cases:
            result = converter.remove_unwanted_characters(input_line)
            self.assertEqual(result, expected,
                           f"Falhou para entrada: {input_line}")
    
    def test_remove_unwanted_characters_both(self):
        """
        Testa remoção de caracteres no início e fim da linha.
        """
        self.create_test_file("test")
        converter = M21Converter(str(self.test_input_file))
        
        test_cases = [
            ("***ABC123***", "ABC123"),
            ("###XYZ789###", "XYZ789"),
            ("   DATA123   ", "DATA123"),
        ]
        
        for input_line, expected in test_cases:
            result = converter.remove_unwanted_characters(input_line)
            self.assertEqual(result, expected,
                           f"Falhou para entrada: {input_line}")
    
    # ==========================================================================
    # TESTES DE DETECÇÃO DE PADRÕES
    # ==========================================================================
    
    def test_detect_measurement_start(self):
        """
        Testa detecção de início de medição.
        """
        self.create_test_file("test")
        converter = M21Converter(str(self.test_input_file))
        
        # Casos que devem ser detectados como início de medição
        positive_cases = [
            "02GZ0001",
            "GZ000001",
            "PT001",
            "P001",
            "0001 0002",
        ]
        
        for case in positive_cases:
            result = converter.detect_measurement_start(case)
            self.assertTrue(result, f"Deveria detectar: {case}")
        
        # Casos que NÃO devem ser detectados
        negative_cases = [
            "ABC",
            "123",
            "texto aleatório",
            "",
        ]
        
        for case in negative_cases:
            result = converter.detect_measurement_start(case)
            self.assertFalse(result, f"NÃO deveria detectar: {case}")
    
    # ==========================================================================
    # TESTES DE DIVISÃO EM MEDIÇÕES
    # ==========================================================================
    
    def test_split_into_measurements_simple(self):
        """
        Testa divisão de conteúdo em medições simples.
        """
        content = "02GZ0001 DATA1   02GZ0002 DATA2   02GZ0003 DATA3"
        self.create_test_file(content)
        
        converter = M21Converter(str(self.test_input_file))
        converter.read_file()
        measurements = converter.split_into_measurements(content)
        
        # Deve encontrar pelo menos 2 medições
        self.assertGreaterEqual(len(measurements), 2)
    
    def test_split_into_measurements_no_pattern(self):
        """
        Testa divisão quando não há padrão reconhecível.
        """
        content = "Dados sem padrão específico 123 456 789"
        self.create_test_file(content)
        
        converter = M21Converter(str(self.test_input_file))
        converter.read_file()
        measurements = converter.split_into_measurements(content)
        
        # Deve retornar pelo menos uma linha
        self.assertGreaterEqual(len(measurements), 1)
    
    # ==========================================================================
    # TESTES DE VALIDAÇÃO
    # ==========================================================================
    
    def test_validate_output_empty(self):
        """
        Testa validação de saída vazia.
        """
        self.create_test_file("test")
        converter = M21Converter(str(self.test_input_file))
        
        is_valid, issues = converter.validate_output([])
        
        self.assertFalse(is_valid)
        self.assertTrue(any("ERRO" in issue for issue in issues))
    
    def test_validate_output_valid(self):
        """
        Testa validação de saída válida.
        """
        self.create_test_file("test")
        converter = M21Converter(str(self.test_input_file))
        
        valid_lines = [
            "02GZ0001 123.456 789.012",
            "02GZ0002 234.567 890.123",
            "02GZ0003 345.678 901.234",
        ]
        
        is_valid, issues = converter.validate_output(valid_lines)
        
        self.assertTrue(is_valid)
    
    def test_validate_output_warnings(self):
        """
        Testa validação com avisos.
        """
        self.create_test_file("test")
        converter = M21Converter(str(self.test_input_file))
        
        # Apenas uma linha (deve gerar aviso)
        is_valid, issues = converter.validate_output(["02GZ0001 123.456"])
        
        self.assertTrue(is_valid)  # Válido, mas com avisos
        self.assertTrue(any("AVISO" in issue for issue in issues))
    
    # ==========================================================================
    # TESTES DE SALVAMENTO
    # ==========================================================================
    
    def test_save_file(self):
        """
        Testa salvamento de arquivo.
        """
        self.create_test_file("test")
        converter = M21Converter(str(self.test_input_file), 
                                 str(self.test_output_file))
        
        lines = ["Line 1", "Line 2", "Line 3"]
        success = converter.save_file(lines)
        
        self.assertTrue(success)
        self.assertTrue(self.test_output_file.exists())
        
        # Verifica conteúdo
        with open(self.test_output_file, 'r') as f:
            saved_content = f.read()
        
        self.assertIn("Line 1", saved_content)
        self.assertIn("Line 2", saved_content)
        self.assertIn("Line 3", saved_content)
    
    # ==========================================================================
    # TESTES DE CONVERSÃO COMPLETA
    # ==========================================================================
    
    def test_full_conversion_simple(self):
        """
        Testa conversão completa com dados simples.
        """
        content = "***02GZ0001 123.456 789.012***   ***02GZ0002 234.567 890.123***"
        self.create_test_file(content)
        
        converter = M21Converter(str(self.test_input_file),
                                 str(self.test_output_file))
        success = converter.convert()
        
        self.assertTrue(success)
        self.assertTrue(self.test_output_file.exists())
        
        # Verifica se o arquivo de saída tem conteúdo
        self.assertGreater(self.test_output_file.stat().st_size, 0)
    
    def test_full_conversion_with_newlines(self):
        """
        Testa conversão com quebras de linha existentes.
        """
        content = """02GZ0001 123.456 789.012
02GZ0002 234.567 890.123
02GZ0003 345.678 901.234"""
        self.create_test_file(content)
        
        converter = M21Converter(str(self.test_input_file),
                                 str(self.test_output_file))
        success = converter.convert()
        
        self.assertTrue(success)
        self.assertTrue(self.test_output_file.exists())
    
    # ==========================================================================
    # TESTES DE ESTATÍSTICAS
    # ==========================================================================
    
    def test_statistics_tracking(self):
        """
        Testa se as estatísticas são rastreadas corretamente.
        """
        content = "***02GZ0001 DATA***   ***02GZ0002 DATA***"
        self.create_test_file(content)
        
        converter = M21Converter(str(self.test_input_file),
                                 str(self.test_output_file))
        converter.convert()
        
        # Verifica se estatísticas foram preenchidas
        self.assertGreater(converter.statistics['input_size'], 0)
        self.assertGreater(converter.statistics['lines_processed'], 0)
        self.assertGreater(converter.statistics['chars_removed'], 0)
    
    def test_report_generation(self):
        """
        Testa geração de relatório.
        """
        content = "02GZ0001 123.456"
        self.create_test_file(content)
        
        converter = M21Converter(str(self.test_input_file),
                                 str(self.test_output_file))
        converter.convert()
        
        report = converter.generate_report()
        
        # Verifica se o relatório contém informações esperadas
        self.assertIn("RELATÓRIO", report)
        self.assertIn(str(self.test_input_file), report)
        self.assertIn(str(self.test_output_file), report)
        self.assertIn("ESTATÍSTICAS", report)


class TestConfigIntegration(unittest.TestCase):
    """
    Testes de integração com o arquivo de configuração.
    """
    
    def test_config_import(self):
        """
        Testa se o arquivo de configuração pode ser importado.
        """
        try:
            import config
            self.assertTrue(hasattr(config, 'PATTERNS_BY_BRAND'))
            self.assertTrue(hasattr(config, 'get_patterns_for_brand'))
        except ImportError:
            self.fail("Não foi possível importar o módulo config")
    
    def test_config_validation(self):
        """
        Testa validação das configurações.
        """
        from config import validate_config
        
        is_valid, errors = validate_config()
        self.assertTrue(is_valid, f"Configuração inválida: {errors}")


def run_tests():
    """
    Executa todos os testes e exibe relatório.
    """
    print("""
╔════════════════════════════════════════════════════════════════════╗
║           TESTES UNITÁRIOS - CONVERSOR TXT PARA M21                ║
╚════════════════════════════════════════════════════════════════════╝
""")
    
    # Cria suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona testes
    suite.addTests(loader.loadTestsFromTestCase(TestM21Converter))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigIntegration))
    
    # Executa testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exibe resumo
    print("\n" + "="*70)
    print("RESUMO DOS TESTES")
    print("="*70)
    print(f"Testes executados: {result.testsRun}")
    print(f"Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Falhas: {len(result.failures)}")
    print(f"Erros: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
