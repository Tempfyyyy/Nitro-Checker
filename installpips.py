import subprocess

def install_packages():
    packages = ['ctypes', 'requests', 'colorama']

    for package in packages:
        try:
            subprocess.check_call(['pip', 'install', package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
        except Exception as e:
            print(f"Unexpected error occurred while installing {package}: {e}")

install_packages()
