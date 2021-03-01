# Veracode Python Dynamic Analysis Scanner Variables Example

A simple example of usage of the Veracode Dynamic Analysis API to configure 
scanner variables. Scanner variables are commonly used to centrally manage
 credentials that can be shared across many analyses.

## Setup

Clone this repository:

    git clone https://github.com/anon-veracoder/veracode-dynamic-analysis-api-examples.git

Install dependencies:

    cd veracode-dynamic-analysis-api-examples
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

### Scanner Variables

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

    python veracode--vars.py -k PASSWORD -v 'hzZK2HgBC5@['

Note that if you get a 400 back, try running with -d.  Common issues are reusing the same analysis name, and linking an app that is already linked to another scan (example payload that comes back in that case):

    {'_embedded': {'errors': [{'code': 'APP_IS_LINKED_TO_ANOTHER_SCAN', 'title': 'Application is linked to a different scan', 'detail': 'Application is aleady linked to a different scan.', 'meta': {'error_type': 'APP_IS_LINKED_TO_ANOTHER_SCAN', 'scan_id': '32a3633fd74488ca19561c521f1d9f2d', 'app_id': '914bedaf-ee52-43ff-9020-cf0d5dbf7f1b'}, 'status': '400'}]}}
