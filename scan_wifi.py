import subprocess
import re

def run_command(command):
    """Executes a system command and returns the output."""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout

def get_wifi_networks():
    """Gets a list of Wi-Fi networks with their signal strength."""
    # Run netsh wlan show networks command
    command = "netsh wlan show networks mode=Bssid"
    output = run_command(command)

    # List to store networks and their signal strength
    networks = []

    # Regular expressions to capture the SSID (network name) and signal strength
    ssid_pattern = re.compile(r"SSID (\d+) : (.+)")
    signal_pattern = re.compile(r"Signal\s+:\s+(\d+)%")

    ssid = None
    signal = None

    # Process the output line by line
    for line in output.splitlines():
        # Check for SSID (network name)
        ssid_match = ssid_pattern.search(line)
        if ssid_match:
            ssid = ssid_match.group(2)  # Extract the SSID (network name)
        
        # Check for Signal strength
        signal_match = signal_pattern.search(line)
        if signal_match:
            signal = signal_match.group(1)  # Extract signal strength in percentage

            # If both SSID and signal are found, append them to the list
            if ssid and signal:
                networks.append({"SSID": ssid, "Signal Strength": signal})
                ssid = None  # Reset SSID for the next network

    return networks

def main():
    networks = get_wifi_networks()
    
    if networks:
        print(f"{'SSID':<30} {'Signal Strength (%)'}")
        print("-" * 40)
        for network in networks:
            print(f"{network['SSID']:<30} {network['Signal Strength']}%")
    else:
        print("No Wi-Fi networks found.")

if __name__ == "__main__":
    main()
