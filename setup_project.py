import subprocess
import sys
from pathlib import Path

REQUIREMENTS_PATH = Path("requirements.txt")


def run_command(command):
    print(f"\nÇalıştırılıyor: {' '.join(command)}")
    result = subprocess.run(command)

    if result.returncode != 0:
        print("\nHata oluştu.")
        sys.exit(result.returncode)


def main():
    if not REQUIREMENTS_PATH.exists():
        print("requirements.txt bulunamadı.")
        sys.exit(1)

    print("Pip güncelleniyor...")
    run_command([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip"
    ])

    print("Gerekli paketler yükleniyor...")
    run_command([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        str(REQUIREMENTS_PATH)
    ])

    print("\nKurulum tamamlandı.")


if __name__ == "__main__":
    main()