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
    print("""scanner-variables-example.py [-x variable_name] [-k <variable_name> -v <variable_value>] [-l]
        -l          List all variables defined at account level.
        -d          Debug mode, prints out requests / response JSON.
        -k          Variable key to add, can be referenced in selenium scripts with ${variable_name}
        -v          Value of variable
        -x          Variable id to delete (id can be obtained from -l)
""")
    sys.exit()


def list_scanner_variables(verbose):
    """Lists the scanner variables that are defined at the organization level. """
    print("Account-scoped scanner variables:")
    path = api_base + "/scanner_variables"
    response = requests.get(path, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    data = response.json()

    if verbose:
        print(data)

    if len(data["_embedded"]["scanner_variables"]) == 0:
        print("No variables defined.")

    for variable in data["_embedded"]["scanner_variables"]:
        print(f"{variable['reference_key']} = {variable['value']} [id = {variable['scanner_variable_id']}]")
                                             
def set_scanner_variable(verbose, key, value):
    """Creates a new scanner variable with the passed reference key and value.
       Note that this example uses a POST - use a PUT on /scanner_variables/{id} if you 
       wish to maintain the id. This example only creates a variable with a specified 
       reference key, but it is optional - if not passed selenium scripts will need to 
       reference the value by id, for example ${5868c121991c64a90ef97f8709649086}."""

    if not value:
        # obligatory XKCD reference: https://xkcd.com/936/
        value = "correct horse battery staple"
    if not key:
        key = "PASSWORD"
    print(f"Setting scanner variable {key}")

    request_body = {"description": "Example variable",
                    "reference_key": key,
                    "value": value}
    if verbose:
        print(f"Sending {json.dumps(request_body)}")
    response = requests.post(api_base + "/scanner_variables",
                             auth=RequestsAuthPluginVeracodeHMAC(),
                             headers=headers, json=request_body)

    if verbose and response.ok:
        data = response.json()
        print(data)

    if not response.ok:
        print(f"Error setting scanner variable: {str(response)}")
        data = response.json()
        print(data)


def delete_scanner_variable(verbose, scanner_variable_id):
    """Deletes the specified scanner variable by id (example '5868c121991c64a90ef97f8709649086'"""    
    print(f"Deleting scanner variable {scanner_variable_id}")
    path = api_base + "/scanner_variables/" + scanner_variable_id
    response = requests.delete(path,
                               auth=RequestsAuthPluginVeracodeHMAC(),
                               headers=headers)
    if verbose and response.ok:
        print(f"Status code: {response.status_code}")
    if not response.ok:
        print(f"Error deleting scanner variable: {str(response)}")
        data = response.json()
        print(data)


def main(argv):
    """Simple command line support for creating, deleting, and listing DA scanner variables"""
    try:
        variable_name = ''
        variable_value = ''
        verbose = False
        show_vars = False
        delete_key = ''

        opts, args = getopt.getopt(argv, "hdlk:v:x:",
                                   ["key=", "value=", "delete_key="])
        for opt, arg in opts:
            if opt == '-h':
                print_help()
            if opt == '-d':
                verbose = True
            if opt == '-l':
                show_vars = True
            if opt in ('-k', '--key'):
                variable_name = arg
            if opt in ('-v', '--value'):
                variable_value = arg
            if opt in ('-x', '--delete_key'):
                delete_key = arg

        if variable_name or variable_value:
            set_scanner_variable(verbose, variable_name, variable_value)
        if delete_key:
            delete_scanner_variable(verbose, delete_key)
        if show_vars:
            list_scanner_variables(verbose)
    except requests.RequestException as e:
        print("An error occurred!")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
