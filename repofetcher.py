import requests
import os

# GitHub API endpoint for releases
repo_owner = "openbao"  # Replace with the repository owner
repo_name = "openbao"    # Replace with the repository name
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"

# Create the 'packages' directory if it doesn't exist
output_dir = 'amd64'
os.makedirs(output_dir, exist_ok=True)

# Get the releases from the API
response = requests.get(api_url)

if response.status_code == 200:
    releases = response.json()
    
    for release in releases:
        print(f"Release: {release['name']}")
        for asset in release['assets']:
            asset_url = asset['browser_download_url']
            file_name = asset['name']
            
            # Filter by RPM files or GPG signature files
            if file_name.endswith('amd64.rpm') or file_name.endswith('amd64.rpm.gpgsig'):
                # Define the full path to save the file in 'packages' directory
                file_path = os.path.join(output_dir, file_name)

                # Download the asset
                print(f"Downloading {file_name} from {asset_url}")
                asset_response = requests.get(asset_url)
                
                # Save the asset into the 'packages' directory
                with open(file_path, 'wb') as file:
                    file.write(asset_response.content)
                print(f"Downloaded {file_name} to {file_path}")
            else:
                print(f"Skipped {file_name}, not an RPM or GPG signature.")
else:
    print(f"Failed to fetch releases: {response.status_code}")
