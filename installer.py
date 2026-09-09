import os
import sys
import zipfile
import urllib.request
import tempfile
import shutil

# --- Configure these for your project ---
JUNGLESCRIPT_URL = "https://github.com/yourusername/junglescript/releases/latest/download/junglescript.zip"
INSTALL_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "JungleScript")
# ------------------------------------------

def download_junglescript(url, dest_zip):
    print(f"Downloading JungleScript from {url} ...")
    urllib.request.urlretrieve(url, dest_zip)
    print("Download complete.")

def extract_zip(zip_path, target_dir):
    print(f"Extracting to {target_dir} ...")
    os.makedirs(target_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target_dir)
    print("Extraction complete.")

def add_to_user_path(path_to_add):
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
    try:
        current_path, _ = winreg.QueryValueEx(key, "Path")
    except FileNotFoundError:
        current_path = ""
    if path_to_add.lower() not in current_path.lower():
        new_path = f"{current_path};{path_to_add}" if current_path else path_to_add
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        print("Added JungleScript to your PATH. Restart your terminal to use it.")
    else:
        print("JungleScript is already on PATH.")
    winreg.CloseKey(key)

def main():
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, "junglescript.zip")
        download_junglescript(JUNGLESCRIPT_URL, zip_path)
        extract_zip(zip_path, INSTALL_DIR)

    try:
        add_to_user_path(INSTALL_DIR)
    except Exception as e:
        print(f"Could not update PATH automatically: {e}")
        print(f"Add this folder to PATH manually: {INSTALL_DIR}")

    print("\nJungleScript installed successfully!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
