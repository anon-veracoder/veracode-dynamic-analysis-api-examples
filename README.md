# Veracode Python Dynamic Analysis Scanner Variables Example

A simple example of usage of the Veracode Dynamic Analysis API to configure 
scanner variables. Scanner variables are commonly used to centrally manage
 credentials that can be shared across many analyses.

## Setup

Clone this repository:

    git clone https://github.com/veracode/veracode-da-scanner-vars-example.git

Install dependencies:

    cd veracode-da-scanner-vars-example
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

If you have saved credentials as above you can add a new account-level scanner
variable with:

    python veracode-da-scanner-vars.py -k PASSWORD -v 'hzZK2HgBC5@['
    
You can then list the defined variables with:

    python veracode-da-scanner-vars.py -l

Otherwise you will need to set environment variables before running `example.py`:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python veracode-da-scanner-vars-example.py -l
