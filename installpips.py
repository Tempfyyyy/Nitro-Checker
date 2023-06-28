import os

required_packages = [
    "requests",
    "colorama"
]

def install_package(package_name):
    os.system(f"pip install {package_name}")

for package in required_packages:
    install_package(package)
