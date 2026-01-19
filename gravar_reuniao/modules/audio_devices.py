import subprocess
import sys

def get_default_monitor():
    try:
        result = subprocess.run(
            ["pactl", "get-default-sink"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            default_sink = result.stdout.strip()
            monitor_name = f"{default_sink}.monitor"
            return monitor_name
    except Exception as e:
        print(f"Erro ao obter monitor: {e}", file=sys.stderr)
    return None

def get_default_source():
    try:
        result = subprocess.run(
            ["pactl", "get-default-source"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Erro ao obter fonte padrão: {e}", file=sys.stderr)
    return None
