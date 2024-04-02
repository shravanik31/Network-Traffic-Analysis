import os
import time
import glob
import subprocess
import re
from mitmproxy.io import FlowReader


# Get the path to the APK files
apk_folder_path = '/Users/shravanikonda/Desktop/Project/APKs'

# Connect to the android emulator
device_id = 'emulator-5554' # This is the default id for the first android emulator instance

# Get a list of all the APK files in the folder
apk_files = [os.path.join(apk_folder_path, f) for f in os.listdir(apk_folder_path) if f.endswith('.apk')]


# The folder path where the apk files are stored
folder_path = "/Users/shravanikonda/Desktop/Project/APKA/Shop"
emulator_name = 'emulator-5554'

def open_mitm(package_name):
    command = "mitmproxy -p 8083 --set flow_export_options=raw -w {}.mitm".format(package_name)
    process = subprocess.Popen(command, shell=True)

def fuzzApps(package_name):
    subprocess.check_output(['adb', 'shell', 'monkey', '-p', package_name, '-v', '500','--throttle','5000']).decode() 

def open_app_using_monkey(package_name):
    command = "adb shell monkey -p {} -c android.intent.category.LAUNCHER 1".format(package_name)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def getTaskID(package_name):
    command = "adb shell am stack list | grep {}".format(package_name)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    taskId = re.search(r'taskId=(\d+)', output.decode()).group(1)
    return taskId

def pinApp(taskId):
    # Use adb to start the activity
    command = "adb shell am task lock {}".format(taskId)        
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def unpinApp():
    command = "adb shell am task lock stop"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def closeApp(package_name):
    command = "adb shell am force-stop {}".format(package_name)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def saveMitmFlow(package_name):
    command = "mitmproxy -p proxy 8083 -q flows {}.flow".format("kohls1234")
    process = subprocess.Popen(command, shell=True)

def closeAndKillMitm():
    command = "ps aux | grep mitmproxy | grep -v grep | awk '{print $2}'"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print("Error:", error.decode())
    else:
        pid = output.decode().strip()
        command = "kill {}".format(pid)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def process_flow(flow):
    # Initialize an empty string to hold the formatted data
    formatted_data = ""

    # Check if the flow is an HTTP flow
    if hasattr(flow, 'request'):
        # Format the request data
        formatted_data += f"Request URL: {flow.request.url}\n"
        formatted_data += f"Request Method: {flow.request.method}\n"
        formatted_data += f"Request Headers: {flow.request.headers}\n\n"

        # Format the response data if it exists
        if hasattr(flow, 'response'):
            formatted_data += f"Response Status Code: {flow.response.status_code}\n"
            formatted_data += f"Response Headers: {flow.response.headers}\n"
            formatted_data += f"Response Content: {flow.response.get_text()}\n"
            formatted_data += "----------------------------------------------------------\n\n"

    return formatted_data

def getFileName(package_name):
    apk_file_name = os.path.basename(package_name)
    unique_apk_file_name = apk_file_name.replace(" ", "").replace(".", "")
    unique_apk_file_name = unique_apk_file_name.split("_")[0]
    return unique_apk_file_name

def open_app(package_name, apk_file):
    input_file = getFileName(apk_file)
    output_file = 'outputs/{}.txt'.format(input_file)
    open_mitm(getFileName(apk_file))
    time.sleep(10)
    open_app_using_monkey(package_name)
    time.sleep(15)
    taskId = getTaskID(package_name)
    pinApp(taskId)	
    time.sleep(10)
    fuzzApps(package_name)
    print("Fuzzed")
    time.sleep(10)
    unpinApp()
    time.sleep(10)
    closeApp(package_name)
    print("closed App")
    time.sleep(10)
    #saveMitmFlow(apk_file)
    print("Close and kill mitm before")
    closeAndKillMitm()
    print("close and kill mitm after")
    input_file = input_file+'.mitm'
    with open(input_file, 'rb') as f_in, open(output_file, 'w') as f_out:
        reader = FlowReader(f_in)
        for flow in reader.stream():
            formatted_data = process_flow(flow)
            f_out.write(formatted_data)


# Function to open app, send monkey fuzzing commands and repeat this for all the apps one by one
def processApp():
    # List all APK files in the folder
    apk_files = glob.glob(os.path.join(folder_path, "*.apk"))
    
    # Iterate over each APK file
    for apk_file in apk_files:	
        # Extract the package name from the APK file
        package_name = subprocess.check_output(['aapt', 'dump', 'badging', apk_file]).decode().split('package: name=')[1].split(' versionCode')[0]
        open_app(package_name, getFileName(apk_file))
        time.sleep(15)
        print(f'Fuzzed: {apk_file}')
        # Wait for 10 seconds before fuzzing the next app
        time.sleep(10)

processApp()