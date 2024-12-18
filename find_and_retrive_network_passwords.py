import subprocess

# Function to run a system command and return its output
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout

# Function to get all saved Wi-Fi profiles
def get_wifi_profiles():
    command = "netsh wlan show profiles"
    output = run_command(command)
    profiles = []
    
    # Parse output to get the profile names
    for line in output.splitlines():
        if "All User Profile" in line:
            profile_name = line.split(":")[1].strip()
            profiles.append(profile_name)
    
    return profiles

# Function to get details of a Wi-Fi profile, including the password
def get_wifi_password(profile_name):
    command = f'netsh wlan show profile name="{profile_name}" key=clear'
    output = run_command(command)
    
    # Parse the output to extract the key content (password)
    for line in output.splitlines():
        if "Key Content" in line:
            password = line.split(":")[1].strip()
            return password
    
    return None  # Return None if no password is found

# Main function to retrieve profiles and passwords
def main():
    profiles = get_wifi_profiles()
    
    if not profiles:
        print("No Wi-Fi profiles found.")
        return
    
    for profile in profiles:
        print(f"\nProfile Name: {profile}")
        password = get_wifi_password(profile)
        if password:
            print(f"Password: {password}")
        else:
            print("Password: Not available or not stored in clear text.")

if __name__ == "__main__":
    main()
