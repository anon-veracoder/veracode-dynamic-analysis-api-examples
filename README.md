# Veracode Python Dynamic Analysis API Examples

## Overview

This project contains small command line utilites that illustrate the use of Veracode's Dynamic Analysis REST APIs.

### Scanner Variables

A simple example of usage of the Veracode Dynamic Analysis API to configure scanner variables. Scanner variables are commonly used to centrally manage credentials that can be shared across many analyses.

The veracode-da-app-link.py shows how to use these APIs.

### App Linked Scans

Scans can be linked to applications in the vercode platform.  

The veracode-da-app-link.py script illustrates how this can be automated.

## Installation

Clone this repository:

    git clone https://github.com/veracode/veracode-da-scanner-vars-example.git

Install dependencies:

    cd veracode-da-scanner-vars-example
    pip install -r requirements.txt

## Usage

### Getting Started

It is highly recommended that you store veracode API credentials on disk, in a secure file that has 
appropriate file protections in place.

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

### Scanner Variables

    scanner-variables-example.py [-x <variable_name>] [-k <variable_name> -v <variable_value>] [-l]
            -l          List all variables defined at account level.
            -d          Debug mode, prints out requests / response JSON.
            -k          Variable key to add, can be referenced in selenium scripts with ${variable_name}
            -v          Value of variable
            -x          Variable id to delete (id can be obtained from -l)

If you have saved credentials as above you can add a new account-level scanner
variable with:

    python veracode-da-scanner-vars.py -k PASSWORD -v 'hzZK2HgBC5@['
    
You can then list the defined variables with:

    python veracode-da-scanner-vars.py -l

Otherwise you will need to set environment variables before running `example.py`:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python veracode-da-scanner-vars-example.py -l

### App Linked Scans

If you have saved credentials as above you can initiate an app linked scan with:

    python veracode-da-app-link.py -a <application_name> -u <target_url>

Note that if you get a 400 back, try running with -d.  Common issues are reusing the same analysis name, and linking an app that is already linked to another scan (example payload that comes back in that case):

    {'_embedded': {'errors': [{'code': 'APP_IS_LINKED_TO_ANOTHER_SCAN', 'title': 'Application is linked to a different scan', 'detail': 'Application is aleady linked to a different scan.', 'meta': {'error_type': 'APP_IS_LINKED_TO_ANOTHER_SCAN', 'scan_id': '32a3633fd74488ca19561c521f1d9f2d', 'app_id': '914bedaf-ee52-43ff-9020-cf0d5dbf7f1b'}, 'status': '400'}]}}


## License

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

See the [LICENSE](LICENSE) file for details

## Security 

See the [SECURITY.md](Security Policy) for details on how to report vulnerabilities and any known static analysis issues.
