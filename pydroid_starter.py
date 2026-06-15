import subprocess
import sys

def install_dependencies():
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py", "requests", "aiohttp", "pillow"])
    print("Dependencies installed successfully!")

if __name__ == "__main__":
    try:
        import discord
        print("discord.py already installed.")
    except ImportError:
        install_dependencies()
    
    print("\n--- Panduan Pydroid 3 ---")
    print("1. Pastikan Anda sudah memiliki Token Bot dari Discord Developer Portal.")
    print("2. Masukkan Token di file config.py.")
    print("3. Jalankan main.py untuk memulai bot.")
    print("-------------------------\n")
