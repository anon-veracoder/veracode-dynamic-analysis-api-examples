import sys
import requests
import getopt
import json
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

api_base = "https://api.veracode.com/was/configservice/v1/"
headers = {
    "User-Agent": "Dynamic Analysis API Example Client",
    "Content-Type": "application/json"
}


def print_help():
    """Prints command line options and exits"""
    print("""veracode-da-app-link.py -a <application_name> -u <target_url> [-d]
        Starts a scan of <target_url> linked to an application identified in the Veracode Platform by <application_name>
""")
    sys.exit()


def launch_app_linked_scan(application_name, url, verbose):
    """Lists the scanner variables that are defined at the organization level. """
    path = api_base + f"platform_applications?application_name={application_name}"
    response = requests.get(path, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    data = response.json()

    if verbose:
        print(data)

    if len(data["_embedded"]["platform_applications"]) == 0:
        print("No applications defined.")
        return
    if len(data["_embedded"]["platform_applications"]) != 1:
        print("Warning - too many matching applications, the first will be used.")
    uuid = data["_embedded"]["platform_applications"][0]["uuid"]
    matched_app_name = data["_embedded"]["platform_applications"][0]["name"]
    print(f"Found uuid '{uuid}' for application '{matched_app_name}' for search term '{application_name}'")
                                           
    scan_request = r'''{
          "name": "Example Veracode applinked scan launched from API",
          "scans": [
            {
              "linked_platform_app_uuid": "{uuid}",
              "scan_config_request": {
                "target_url": {
                  "url": "{url}",
                  "http_and_https": true,
                  "directory_restriction_type": "DIRECTORY_AND_SUBDIRECTORY"
                }
              }
            }
          ],
          "schedule": {
            "now": true,
            "duration": {
              "length": 1,
              "unit": "DAY"
            }
          }
        }'''
    scan_request = scan_request.replace("{uuid}", uuid, 1)
    scan_request = scan_request.replace("{url}", url, 2)

    if verbose:
        print(scan_request)
    
    scan_path = api_base + "analyses"
    response = requests.post(scan_path, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers, json=json.loads(scan_request))

    if verbose:
        print(f"status code {response.status_code}")
        body = response.json()
        if body:
            print(body)
    if response.status_code == 201:
        print("Successfully started applinked scan.")

def main(argv):
    """Simple command line support for creating, deleting, and listing DA scanner variables"""
    try:
        application_name = ''
        verbose = False

        opts, args = getopt.getopt(argv, "hda:u:",
                                   ["application_name=", "target_url="])
        for opt, arg in opts:
            if opt == '-h':
                print_help()
            if opt == '-d':
                verbose = True
            if opt in ('-a', '--application_name'):
                application_name = arg
            if opt in ('-u', '--url'):
                target_url = arg


        if application_name and target_url:
            launch_app_linked_scan(application_name, target_url, verbose)
        else:
            print_help()

    except requests.RequestException as e:
        print("An error occurred!")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
