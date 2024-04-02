import subprocess
import glob
import time
import sys
import os

# The folder path where the apk files are stored
folder_path = ["/Users/shravanikonda/Desktop/Project/APKA/Entertainment", "/Users/shravanikonda/Desktop/Project/APKA/Social",
"/Users/shravanikonda/Desktop/Project/APKA/Shopping", "/Users/shravanikonda/Desktop/Project/APKA/misc"]

# Function to uninstall APKs from Android Emulator
def uninstall_apks():
    # List all APK files in the folder
    apk_files = glob.glob(os.path.join(folder_path, "*.apk"))+glob.glob(os.path.join(folder_path, "*.apkm"))
    print(apk_files)
    
    # Iterate over each APK file
    for apk_file in apk_files:
        # Extract the package name from the APK file
        package_name = subprocess.check_output(['aapt', 'dump', 'badging', apk_file]).decode().split('package: name=')[1].split(' versionCode')[0]
        
        # Try to uninstall the package
        try:
            subprocess.check_output(['adb', 'uninstall', package_name])
            print(f'Uninstalled: {apk_file}')
        except subprocess.CalledProcessError:
            print(f'{package_name} is not installed')

# Function to install APKs on Android Emulator
def install_apks():
    apk_files = []
    for i in range(len(folder_path)):
    	apk_files += glob.glob(os.path.join(folder_path[i], "*.apk"))

    # Iterate over each APK file and install it on the Android Emulator
    for apk_file in apk_files:
        subprocess.check_output(['adb', 'install', '-r', apk_file])
        print(f'Installed: {apk_file}')

if __name__ == "__main__":
    install_apks()
    