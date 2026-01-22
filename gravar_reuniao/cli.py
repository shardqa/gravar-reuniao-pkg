#!/usr/bin/env python3

import argparse
import sys
import time
from pathlib import Path
from .modules.recording import record_audio

def main():
    parser = argparse.ArgumentParser(
        description="Grava áudio do desktop e microfone simultaneamente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Gravar (gera arquivo automaticamente com data/hora)
  gravar-reuniao

  # Gravar com nome específico
  gravar-reuniao --output minha_reuniao.wav

  # Gravar por tempo determinado
  gravar-reuniao --duration 300
        """
    )
    parser.add_argument(
        "--output", type=str,
        help="Arquivo de saída (padrão: audio_YYYYMMDD_HHMMSS.flac)"
    )
    parser.add_argument(
        "--duration", type=int,
        help="Duração da gravação em segundos (opcional)"
    )
    
    args = parser.parse_args()
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    output_dir = Path("capturas")
    output_dir.mkdir(exist_ok=True)
    
    if args.output:
        output_path = Path(args.output)
        if not output_path.suffix:
            output_path = output_path.with_suffix('.flac')
        if not output_path.is_absolute():
            output_path = output_dir / output_path
    else:
        output_path = output_dir / f"audio_{timestamp}.flac"
    
    try:
        if not record_audio(output_path, args.duration):
            sys.exit(1)
    except KeyboardInterrupt:
        # Se o KeyboardInterrupt escapar do record_audio, ainda tentamos salvar
        print("\nParando gravação...")
        # Verifica se o arquivo foi criado antes de sair
        if not output_path.exists() or output_path.stat().st_size == 0:
            print("Gravação interrompida antes de salvar arquivo.", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
