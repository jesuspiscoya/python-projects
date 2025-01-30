import re
import requests


def check_url(url, name, timeout):
    try:
        res = requests.head(url, timeout=timeout)

        if res.status_code == 200:
            print(f"LIVE ✅ ➜ {name}")
        elif res.status_code == 302:
            print(f"TIMEOUT ⚠️ ➜ {name}")
        else:
            print(f"DEAD ❌ ➜ {name}")
    except requests.exceptions.Timeout:
        print(f"TIMEOUT ⚠️ ➜ {name}")
    except requests.exceptions.ConnectionError:
        print(f"DEAD ❌ ➜ {name}")
    except requests.RequestException as e:
        print(f"Error al verificar la URL '{url}': {e}")


def check_m3u8(m3u8_url_or_file, timeout):
    try:
        with open(m3u8_url_or_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith('#EXTINF:'):
                # Extraer metadatos usando expresión regular
                match = re.search(r',\s*(.*)$', line)
                url = lines[i + 1].strip()
                name = match.group(1)
                check_url(url, name, timeout)
    except FileNotFoundError:
        print(f"El archivo M3U8 '{m3u8_url_or_file}' no existe.")


check_m3u8('iptv/jesus.m3u', 10)
