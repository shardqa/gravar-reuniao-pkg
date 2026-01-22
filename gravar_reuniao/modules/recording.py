import subprocess
import sys
from pathlib import Path
from .audio_devices import get_default_monitor, get_default_source

def record_audio(output_path, duration=None):
    monitor_name = get_default_monitor()
    source_name = get_default_source()
    
    if not monitor_name:
        print("Erro: Não foi possível obter o monitor do sink padrão", file=sys.stderr)
        return False
    
    if not source_name:
        print("Erro: Não foi possível obter a fonte padrão (microfone)", file=sys.stderr)
        return False
    
    print(f"Gravando do monitor (desktop): {monitor_name}")
    print(f"Gravando do microfone: {source_name}")
    print(f"Arquivo: {output_path}")
    if duration:
        print(f"Duração: {duration} segundos")
    else:
        print("Duração: ilimitada (Ctrl+C para parar)")
    print()
    
    filter_complex = (
        "[0:a]volume=3.0[desktop];"
        "[1:a]volume=1.0[microphone];"
        "[desktop][microphone]amix=inputs=2:duration=longest:dropout_transition=0"
    )
    
    cmd = [
        "ffmpeg",
        "-f", "pulse", "-i", monitor_name,
        "-f", "pulse", "-i", source_name,
        "-filter_complex", filter_complex,
        "-acodec", "flac",
        "-compression_level", "8",
        "-ac", "2",
        "-ar", "48000",
        "-y",
        str(output_path)
    ]
    
    try:
        if duration:
            print(f"Gravando por {duration} segundos...")
            cmd.extend(["-t", str(duration)])
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            try:
                process.wait(timeout=duration + 5)
            except subprocess.TimeoutExpired:
                # Tentar parar graciosamente com 'q' primeiro
                try:
                    if process.stdin:
                        process.stdin.write(b'q')
                        process.stdin.flush()
                        process.stdin.close()
                    process.wait(timeout=2)
                except (subprocess.TimeoutExpired, OSError):
                    # Se não funcionar, usar terminate como último recurso
                    process.terminate()
                    process.wait()
        else:
            print("Gravando... (Ctrl+C para parar)")
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            try:
                process.wait()
            except KeyboardInterrupt:
                # Parar graciosamente enviando 'q' para o ffmpeg finalizar corretamente
                try:
                    if process.stdin:
                        process.stdin.write(b'q')
                        process.stdin.flush()
                        process.stdin.close()
                    process.wait()
                except (OSError, BrokenPipeError):
                    # Se o stdin já estiver fechado, usar terminate como fallback
                    process.terminate()
                    process.wait()
                print("\nParando gravação...")
        
        if output_path.exists() and output_path.stat().st_size > 0:
            abs_path = output_path.resolve()
            print(f"\n✓ Gravação concluída: {output_path}")
            return True
        else:
            print("Erro: Arquivo não foi criado ou está vazio", file=sys.stderr)
            return False
    except FileNotFoundError:
        print("Erro: ffmpeg não encontrado. Instale ffmpeg", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Erro ao gravar: {e}", file=sys.stderr)
        return False
