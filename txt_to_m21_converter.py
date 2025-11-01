#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Conversor de Arquivos TXT para M21 - Estações Totais
=====================================================

Este script automatiza a conversão de arquivos .txt exportados de estações totais
(GD2i, Geodetic, CHC, Topcon, Leica) para o formato .m21, compatível com softwares
de topografia como TG98SE e Topograph.

Autor: Desenvolvido para o repositório ErisonBarros/txt--m21
Licença: Apache License 2.0
Data: Novembro 2025
Versão: 1.0.0

Baseado nas orientações do vídeo:
https://www.youtube.com/watch?v=S9-Wxy4yhmI&t=1s

Problema Resolvido:
-------------------
Os arquivos .txt exportados de estações totais apresentam:
1. Caracteres desnecessários no início e fim de cada linha
2. Ausência de quebras de linha entre medições
3. Formato incompatível com softwares de topografia

Solução Implementada:
--------------------
1. Leitura e análise do arquivo .txt
2. Remoção de caracteres desnecessários
3. Detecção de padrões que indicam nova medição
4. Inserção de quebras de linha apropriadas
5. Validação e salvamento no formato .m21

Uso:
----
    python txt_to_m21_converter.py input.txt output.m21
    
    ou
    
    python txt_to_m21_converter.py input.txt
    (gera automaticamente input_converted.m21)
"""

import re
import sys
import os
import logging
from typing import List, Tuple, Optional
from pathlib import Path
from datetime import datetime


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('txt_to_m21_conversion.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class M21Converter:
    """
    Classe principal para conversão de arquivos TXT para M21.
    
    Esta classe encapsula toda a lógica de conversão, incluindo:
    - Leitura de arquivos TXT
    - Limpeza de caracteres desnecessários
    - Detecção de padrões de medição
    - Formatação para o padrão M21
    - Validação e salvamento
    
    Attributes:
        input_file (Path): Caminho do arquivo de entrada
        output_file (Path): Caminho do arquivo de saída
        encoding (str): Codificação do arquivo (padrão: utf-8)
        patterns (dict): Padrões regex para detecção de medições
    """
    
    # Padrões comuns que indicam início de uma nova medição
    # Estes padrões podem ser ajustados conforme necessário
    MEASUREMENT_PATTERNS = [
        r'^\d{2}[A-Z]{2}\d{4}',  # Padrão: 02GZ0001 (número + letras + número)
        r'^[A-Z]{2}\d{4,6}',      # Padrão: GZ000001 (letras + números)
        r'^\d{4,6}[A-Z]',         # Padrão: 0001A (números + letra)
        r'^PT\d+',                # Padrão: PT001, PT002 (ponto + número)
        r'^P\d+',                 # Padrão: P001, P002 (ponto + número)
        r'^\d{1,4}\s+\d{1,4}',    # Padrão: número espaço número (estação e ponto)
    ]
    
    # Caracteres comuns que devem ser removidos do início/fim das linhas
    UNWANTED_CHARS_START = [
        r'^\s*[^\d\w]+',  # Remove caracteres especiais no início
        r'^[*#@$%&]+',    # Remove símbolos específicos
    ]
    
    UNWANTED_CHARS_END = [
        r'[^\d\w]+\s*$',  # Remove caracteres especiais no final
        r'[*#@$%&]+$',    # Remove símbolos específicos
    ]
    
    def __init__(self, input_file: str, output_file: Optional[str] = None, 
                 encoding: str = 'utf-8'):
        """
        Inicializa o conversor.
        
        Args:
            input_file (str): Caminho do arquivo TXT de entrada
            output_file (str, optional): Caminho do arquivo M21 de saída.
                                        Se não fornecido, será gerado automaticamente.
            encoding (str): Codificação do arquivo (padrão: utf-8)
        
        Raises:
            FileNotFoundError: Se o arquivo de entrada não existir
        """
        self.input_file = Path(input_file)
        
        if not self.input_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")
        
        if output_file:
            self.output_file = Path(output_file)
        else:
            # Gera nome do arquivo de saída automaticamente
            self.output_file = self.input_file.with_stem(
                f"{self.input_file.stem}_converted"
            ).with_suffix('.m21')
        
        self.encoding = encoding
        self.raw_content = ""
        self.cleaned_lines = []
        self.statistics = {
            'input_size': 0,
            'output_size': 0,
            'lines_processed': 0,
            'measurements_found': 0,
            'chars_removed': 0
        }
        
        logger.info(f"Conversor inicializado: {self.input_file} -> {self.output_file}")
    
    def read_file(self) -> str:
        """
        Lê o conteúdo do arquivo de entrada.
        
        Returns:
            str: Conteúdo completo do arquivo
        
        Raises:
            IOError: Se houver erro na leitura do arquivo
        """
        try:
            with open(self.input_file, 'r', encoding=self.encoding) as f:
                self.raw_content = f.read()
            
            self.statistics['input_size'] = len(self.raw_content)
            logger.info(f"Arquivo lido com sucesso: {self.statistics['input_size']} caracteres")
            return self.raw_content
        
        except UnicodeDecodeError:
            # Tenta com codificação alternativa
            logger.warning(f"Erro com codificação {self.encoding}, tentando latin-1")
            with open(self.input_file, 'r', encoding='latin-1') as f:
                self.raw_content = f.read()
            self.encoding = 'latin-1'
            self.statistics['input_size'] = len(self.raw_content)
            return self.raw_content
        
        except Exception as e:
            logger.error(f"Erro ao ler arquivo: {e}")
            raise IOError(f"Não foi possível ler o arquivo: {e}")
    
    def remove_unwanted_characters(self, line: str) -> str:
        """
        Remove caracteres desnecessários do início e fim da linha.
        
        Args:
            line (str): Linha a ser limpa
        
        Returns:
            str: Linha limpa
        """
        original_length = len(line)
        
        # Remove caracteres do início
        for pattern in self.UNWANTED_CHARS_START:
            line = re.sub(pattern, '', line)
        
        # Remove caracteres do final
        for pattern in self.UNWANTED_CHARS_END:
            line = re.sub(pattern, '', line)
        
        # Remove espaços extras
        line = line.strip()
        
        chars_removed = original_length - len(line)
        self.statistics['chars_removed'] += chars_removed
        
        return line
    
    def detect_measurement_start(self, line: str) -> bool:
        """
        Detecta se a linha marca o início de uma nova medição.
        
        Args:
            line (str): Linha a ser analisada
        
        Returns:
            bool: True se a linha inicia uma nova medição
        """
        for pattern in self.MEASUREMENT_PATTERNS:
            if re.match(pattern, line):
                return True
        return False
    
    def split_into_measurements(self, content: str) -> List[str]:
        """
        Divide o conteúdo em medições individuais.
        
        Esta função tenta identificar onde cada medição começa e divide
        o texto em linhas separadas.
        
        Args:
            content (str): Conteúdo completo do arquivo
        
        Returns:
            List[str]: Lista de linhas de medição
        """
        # Remove quebras de linha existentes e espaços múltiplos
        content = content.replace('\n', ' ').replace('\r', ' ')
        content = re.sub(r'\s+', ' ', content)
        
        measurements = []
        current_line = ""
        
        # Tenta dividir por padrões conhecidos
        # Primeiro, tenta encontrar padrões que indicam início de medição
        for pattern in self.MEASUREMENT_PATTERNS:
            matches = list(re.finditer(pattern, content))
            if len(matches) > 1:  # Se encontrou múltiplas ocorrências
                logger.info(f"Padrão detectado: {pattern} ({len(matches)} ocorrências)")
                
                # Divide o conteúdo nos pontos onde o padrão foi encontrado
                measurements = []
                last_end = 0
                
                for i, match in enumerate(matches):
                    if i > 0:  # Pula a primeira iteração
                        # Extrai o texto entre o match anterior e o atual
                        measurement = content[last_end:match.start()].strip()
                        if measurement:
                            measurements.append(measurement)
                    last_end = match.start()
                
                # Adiciona a última medição
                if last_end < len(content):
                    measurement = content[last_end:].strip()
                    if measurement:
                        measurements.append(measurement)
                
                if measurements:
                    self.statistics['measurements_found'] = len(measurements)
                    return measurements
        
        # Se não encontrou padrões, tenta dividir por tamanho fixo
        # (algumas estações exportam com tamanho fixo de registro)
        logger.warning("Nenhum padrão específico detectado, tentando divisão por espaçamento")
        
        # Divide por múltiplos espaços (geralmente indicam separação de registros)
        measurements = re.split(r'\s{3,}', content)
        measurements = [m.strip() for m in measurements if m.strip()]
        
        if measurements:
            self.statistics['measurements_found'] = len(measurements)
            return measurements
        
        # Se ainda não conseguiu, retorna o conteúdo como uma única linha
        logger.warning("Não foi possível detectar divisões automáticas")
        return [content.strip()]
    
    def process_content(self) -> List[str]:
        """
        Processa o conteúdo completo do arquivo.
        
        Returns:
            List[str]: Lista de linhas processadas e limpas
        """
        logger.info("Iniciando processamento do conteúdo")
        
        # Divide em medições
        measurements = self.split_into_measurements(self.raw_content)
        
        # Limpa cada medição
        cleaned = []
        for i, measurement in enumerate(measurements, 1):
            cleaned_measurement = self.remove_unwanted_characters(measurement)
            if cleaned_measurement:  # Só adiciona se não estiver vazia
                cleaned.append(cleaned_measurement)
                logger.debug(f"Medição {i} processada: {cleaned_measurement[:50]}...")
        
        self.cleaned_lines = cleaned
        self.statistics['lines_processed'] = len(cleaned)
        
        logger.info(f"Processamento concluído: {len(cleaned)} linhas geradas")
        return cleaned
    
    def validate_output(self, lines: List[str]) -> Tuple[bool, List[str]]:
        """
        Valida o conteúdo processado antes de salvar.
        
        Args:
            lines (List[str]): Linhas a serem validadas
        
        Returns:
            Tuple[bool, List[str]]: (válido, lista de erros/avisos)
        """
        issues = []
        
        if not lines:
            issues.append("ERRO: Nenhuma linha foi gerada após o processamento")
            return False, issues
        
        if len(lines) < 2:
            issues.append("AVISO: Apenas uma linha foi gerada. Verifique se o arquivo foi processado corretamente.")
        
        # Verifica se as linhas têm conteúdo mínimo
        empty_lines = sum(1 for line in lines if len(line.strip()) < 5)
        if empty_lines > len(lines) * 0.5:
            issues.append(f"AVISO: {empty_lines} linhas parecem estar vazias ou muito curtas")
        
        # Verifica se há dados numéricos (esperado em arquivos de medição)
        lines_with_numbers = sum(1 for line in lines if re.search(r'\d', line))
        if lines_with_numbers < len(lines) * 0.5:
            issues.append("AVISO: Poucas linhas contêm dados numéricos")
        
        if issues:
            for issue in issues:
                if issue.startswith("ERRO"):
                    logger.error(issue)
                else:
                    logger.warning(issue)
        
        # Retorna True se não houver erros críticos
        has_errors = any(issue.startswith("ERRO") for issue in issues)
        return not has_errors, issues
    
    def save_file(self, lines: List[str]) -> bool:
        """
        Salva as linhas processadas no arquivo de saída.
        
        Args:
            lines (List[str]): Linhas a serem salvas
        
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            # Cria diretório se não existir
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Salva o arquivo
            with open(self.output_file, 'w', encoding=self.encoding) as f:
                for line in lines:
                    f.write(line + '\n')
            
            self.statistics['output_size'] = self.output_file.stat().st_size
            logger.info(f"Arquivo salvo com sucesso: {self.output_file}")
            logger.info(f"Tamanho do arquivo de saída: {self.statistics['output_size']} bytes")
            
            return True
        
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo: {e}")
            return False
    
    def generate_report(self) -> str:
        """
        Gera um relatório detalhado da conversão.
        
        Returns:
            str: Relatório formatado
        """
        report = f"""
{'='*70}
RELATÓRIO DE CONVERSÃO TXT PARA M21
{'='*70}

Arquivo de Entrada:  {self.input_file}
Arquivo de Saída:    {self.output_file}
Data/Hora:           {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Codificação:         {self.encoding}

{'='*70}
ESTATÍSTICAS
{'='*70}

Tamanho do arquivo de entrada:     {self.statistics['input_size']:,} bytes
Tamanho do arquivo de saída:       {self.statistics['output_size']:,} bytes
Linhas processadas:                {self.statistics['lines_processed']}
Medições encontradas:              {self.statistics['measurements_found']}
Caracteres removidos:              {self.statistics['chars_removed']:,}

Redução de tamanho:                {((1 - self.statistics['output_size'] / max(self.statistics['input_size'], 1)) * 100):.2f}%

{'='*70}
STATUS: CONVERSÃO CONCLUÍDA COM SUCESSO
{'='*70}
"""
        return report
    
    def convert(self) -> bool:
        """
        Executa o processo completo de conversão.
        
        Returns:
            bool: True se a conversão foi bem-sucedida
        """
        try:
            logger.info("="*70)
            logger.info("INICIANDO CONVERSÃO TXT PARA M21")
            logger.info("="*70)
            
            # 1. Ler arquivo
            self.read_file()
            
            # 2. Processar conteúdo
            processed_lines = self.process_content()
            
            # 3. Validar saída
            is_valid, issues = self.validate_output(processed_lines)
            
            if not is_valid:
                logger.error("Validação falhou. Conversão abortada.")
                return False
            
            # 4. Salvar arquivo
            if not self.save_file(processed_lines):
                return False
            
            # 5. Gerar relatório
            report = self.generate_report()
            print(report)
            logger.info("Conversão concluída com sucesso!")
            
            return True
        
        except Exception as e:
            logger.error(f"Erro durante a conversão: {e}", exc_info=True)
            return False


def main():
    """
    Função principal para execução via linha de comando.
    """
    print("""
╔════════════════════════════════════════════════════════════════════╗
║      CONVERSOR DE ARQUIVOS TXT PARA M21 - ESTAÇÕES TOTAIS          ║
║                                                                    ║
║  Converte arquivos .txt exportados de estações totais para o      ║
║  formato .m21 compatível com softwares de topografia.             ║
╚════════════════════════════════════════════════════════════════════╝
""")
    
    # Verifica argumentos
    if len(sys.argv) < 2:
        print("Uso: python txt_to_m21_converter.py <arquivo_entrada.txt> [arquivo_saida.m21]")
        print("\nExemplos:")
        print("  python txt_to_m21_converter.py dados.txt")
        print("  python txt_to_m21_converter.py dados.txt dados_convertidos.m21")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Cria o conversor
        converter = M21Converter(input_file, output_file)
        
        # Executa a conversão
        success = converter.convert()
        
        if success:
            print(f"\n✓ Arquivo convertido com sucesso!")
            print(f"  Arquivo de saída: {converter.output_file}")
            print(f"  Log detalhado: txt_to_m21_conversion.log")
            sys.exit(0)
        else:
            print("\n✗ Erro durante a conversão. Verifique o log para mais detalhes.")
            sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"\n✗ Erro: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erro inesperado: {e}")
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
