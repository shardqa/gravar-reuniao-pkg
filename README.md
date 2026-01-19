# Gravar Reunião - Sistema Portável de Gravação de Áudio

Sistema leve e portável para gravação simultânea de áudio do desktop e microfone, ideal para capturar reuniões, palestras e apresentações.

## Características

- **Zero dependências Python**: Usa apenas bibliotecas padrão do Python
- **Portável**: Funciona em qualquer PC Linux com PulseAudio
- **Simples**: Um único comando para gravar
- **Flexível**: Grave com duração definida ou ilimitada
- **Qualidade**: Áudio em WAV PCM 16-bit, 48kHz, estéreo

## Requisitos do Sistema

### Software Necessário

1. **Python 3.8 ou superior**
   ```bash
   python3 --version
   ```

2. **FFmpeg** - Para captura e processamento de áudio
   ```bash
   # Verificar se está instalado
   which ffmpeg
   
   # Instalar no Gentoo
   sudo emerge media-video/ffmpeg
   
   # Instalar no Debian/Ubuntu
   sudo apt install ffmpeg
   
   # Instalar no Fedora
   sudo dnf install ffmpeg
   ```

3. **PulseAudio Utils** - Para detectar dispositivos de áudio
   ```bash
   # Verificar se está instalado
   which pactl
   
   # Instalar no Gentoo
   sudo emerge media-sound/pulseaudio
   
   # Instalar no Debian/Ubuntu
   sudo apt install pulseaudio-utils
   
   # Instalar no Fedora
   sudo dnf install pulseaudio-utils
   ```

## Instalação

### Método 1: Instalação Local (Desenvolvimento)

```bash
cd gravar-reuniao-pkg
pip install -e .
```

### Método 2: Instalação Global com pipx (Recomendado)

```bash
# Instalar pipx se não tiver
pip install --user pipx
pipx ensurepath

# Instalar o pacote
cd gravar-reuniao-pkg
pipx install .
```

### Método 3: Instalação Direta com pip

```bash
cd gravar-reuniao-pkg
pip install .
```

## Uso

### Gravar Reunião

```bash
# Gravar com nome automático (audio_YYYYMMDD_HHMMSS.wav)
gravar-reuniao

# Gravar com nome específico
gravar-reuniao --output minha_reuniao.wav

# Gravar por tempo determinado (em segundos)
gravar-reuniao --duration 300  # 5 minutos

# Gravar em diretório específico (caminho absoluto)
gravar-reuniao --output /caminho/completo/reuniao.wav
```

### Durante a Gravação

- Pressione `Ctrl+C` para parar a gravação (o arquivo será salvo)
- A gravação captura simultaneamente:
  - **Áudio do desktop** (aplicativos, navegador, música, etc.) - volume 3x
  - **Áudio do microfone** - volume 1x

### Arquivos Gerados

Por padrão, os arquivos são salvos na pasta `capturas/` no diretório atual:

```
./capturas/
├── audio_20260119_143052.wav
├── audio_20260119_150234.wav
└── minha_reuniao.wav
```

## Verificação da Instalação

Execute estes comandos para verificar se tudo está funcionando:

```bash
# 1. Verificar se o comando está disponível
which gravar-reuniao

# 2. Ver ajuda do comando
gravar-reuniao --help

# 3. Verificar dependências do sistema
which ffmpeg && echo "✓ FFmpeg instalado"
which pactl && echo "✓ PulseAudio instalado"

# 4. Testar dispositivos de áudio
pactl get-default-sink    # Deve mostrar seu dispositivo de saída
pactl get-default-source  # Deve mostrar seu microfone

# 5. Fazer uma gravação de teste (5 segundos)
gravar-reuniao --duration 5 --output teste.wav
```

## Solução de Problemas

### Erro: "ffmpeg não encontrado"

```bash
# Instale o FFmpeg
sudo emerge media-video/ffmpeg  # Gentoo
# ou
sudo apt install ffmpeg  # Debian/Ubuntu
```

### Erro: "Não foi possível obter o monitor do sink padrão"

```bash
# Verifique se o PulseAudio está rodando
pulseaudio --check && echo "PulseAudio está rodando"

# Liste os dispositivos disponíveis
pactl list sinks short
pactl list sources short

# Configure um sink padrão
pactl set-default-sink <nome-do-sink>
```

### Erro: "Não foi possível obter a fonte padrão (microfone)"

```bash
# Configure uma fonte padrão
pactl set-default-source <nome-da-fonte>

# Ou verifique se o microfone não está mudo
pactl list sources | grep -A 10 "Name.*monitor"
```

### Gravação sem áudio ou muito baixa

- Verifique os volumes no PulseAudio:
  ```bash
  pavucontrol  # Interface gráfica de controle de volume
  ```
- Ajuste o volume do desktop e microfone durante a gravação
- O volume do desktop é amplificado 3x automaticamente

## Desinstalação

```bash
# Se instalou com pipx
pipx uninstall gravar-reuniao

# Se instalou com pip
pip uninstall gravar-reuniao
```

## Sincronização Entre PCs

Para usar em múltiplos PCs:

1. **Opção A - Instalar em cada PC:**
   ```bash
   # Copie a pasta gravar-reuniao-pkg para cada PC
   # Instale localmente
   cd gravar-reuniao-pkg
   pipx install .
   ```

2. **Opção B - Publicar em repositório Git:**
   ```bash
   # No primeiro PC
   cd gravar-reuniao-pkg
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <seu-repo>
   git push -u origin main
   
   # No segundo PC
   git clone <seu-repo>
   cd gravar-reuniao-pkg
   pipx install .
   ```

3. **Opção C - Instalação direta via Git:**
   ```bash
   pipx install git+https://github.com/seu-usuario/gravar-reuniao-pkg.git
   ```

## Estrutura do Projeto

```
gravar-reuniao-pkg/
├── pyproject.toml              # Configuração do pacote
├── README.md                   # Este arquivo
├── gravar_reuniao/
│   ├── __init__.py            # Inicialização do pacote
│   ├── __main__.py            # Entry point para python -m
│   ├── cli.py                 # Interface de linha de comando
│   └── modules/
│       ├── __init__.py
│       ├── recording.py       # Lógica de gravação com FFmpeg
│       └── audio_devices.py   # Detecção de dispositivos PulseAudio
```

## Licença

MIT License - Livre para uso pessoal e comercial.

## Autor

Richard

## Contribuições

Sugestões e melhorias são bem-vindas!
