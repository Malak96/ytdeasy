import json
import subprocess
from rich import print  

# Comando para obtener la información en formato JSON
command = ["yt-dlp", "-F", "-q", "--dump-json", "https://www.youtube.com/watch?v=B3Gm9eplhCY&t=1s"]
result = subprocess.run(command, capture_output=True, text=True)

# Parsear la salida JSON
print(result)