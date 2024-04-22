import requests

# Specify the URL to the Packages file
packages_url = 'https://pkg.opspt.org/dists/bookworm/main/binary-amd64/Packages'

codename = 'bookworm'
architecture = 'amd64'
package_name = "k9s"

# Fetch the Packages file
response = requests.get(packages_url)
packages_data = response.text

# Function to construct the URL for the deb file
def construct_deb_url(package_info):
    infos = package_info.split('\n')
    filename = ''
    for info in infos:
        if 'Filename' in info:
            filename = info.split(': ')[1]
    return f'https://pkg.opspt.org/{filename}'

# Parse the Packages file
packages = packages_data.split('\n\n')
for package_info in packages:
    if f'Package: {package_name}' in package_info and f'Architecture: {architecture}' in package_info:
        package_name = package_info.split('\n')[0].split(': ')[1]
        version = package_info.split('\n')[1].split(': ')[1]
        deb_url = construct_deb_url(package_info)

        # Download the deb file
        response = requests.get(deb_url)
        with open(f'{package_name}.deb', 'wb') as deb_file:
            deb_file.write(response.content)
        print(f'Downloaded {package_name}.deb')
