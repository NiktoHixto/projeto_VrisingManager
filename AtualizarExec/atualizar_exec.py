import argparse
import os
import shutil
import subprocess
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
VRISING_DIR = os.path.join(PROJECT_DIR, "VRisingManager")
MAIN_FILE = os.path.join(VRISING_DIR, "main.py")
DIST_DIR = os.path.join(PROJECT_DIR, "dist")
BUILD_DIR = os.path.join(PROJECT_DIR, "build", "pyinstaller")
SPEC_DIR = os.path.join(PROJECT_DIR, "build", "pyinstaller")


def ensure_pyinstaller():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return True
    except Exception:
        pass

    print("PyInstaller não encontrado. Instalando...")
    install = subprocess.run(
        [sys.executable, "-m", "pip", "install", "pyinstaller"],
        check=False,
    )
    return install.returncode == 0


def build_executable(clean=False):
    if not os.path.isfile(MAIN_FILE):
        raise FileNotFoundError(f"Arquivo principal não encontrado: {MAIN_FILE}")

    if clean and os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)

    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(SPEC_DIR, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--name",
        "VRisingManager",
        "--distpath",
        DIST_DIR,
        "--workpath",
        BUILD_DIR,
        "--specpath",
        SPEC_DIR,
        MAIN_FILE,
    ]

    print("Gerando executável com o comando:")
    print(" ".join(command))

    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise RuntimeError("Falha ao gerar o executável.")

    executable = os.path.join(DIST_DIR, "VRisingManager.exe")
    if not os.path.exists(executable):
        executable = os.path.join(DIST_DIR, "VRisingManager")

    return executable


def main():
    parser = argparse.ArgumentParser(
        description="Cria ou atualiza o executável do projeto VRisingManager."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove a build antiga antes de gerar uma nova versão.",
    )
    args = parser.parse_args()

    if not ensure_pyinstaller():
        raise RuntimeError("Não foi possível instalar o PyInstaller.")

    executable = build_executable(clean=args.clean)
    print(f"Executável atualizado com sucesso em: {executable}")


if __name__ == "__main__":
    main()
