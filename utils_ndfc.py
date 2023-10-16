"""
CISCO SAMPLE CODE LICENSE
                                  Version 1.1
                Copyright (c) 2022 Cisco and/or its affiliates
   These terms govern this Cisco Systems, Inc. ("Cisco"), example or demo
   source code and its associated documentation (together, the "Sample
   Code"). By downloading, copying, modifying, compiling, or redistributing
   the Sample Code, you accept and agree to be bound by the following terms
   and conditions (the "License"). If you are accepting the License on
   behalf of an entity, you represent that you have the authority to do so
   (either you or the entity, "you"). Sample Code is not supported by Cisco
   TAC and is not tested for quality or performance. This is your only
   license to the Sample Code and all rights not expressly granted are
   reserved.
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import re
import requests
from requests.auth import HTTPBasicAuth
import json
from random import randrange
from decouple import config

"""
This Utility file is for use with NFDC (version 12+)

For use with DCNM (< version 12) please use the utils.py file.
"""



# Fetch the variables from the .env file
NFDC_IP = config('DCNM_IP')
username = config('username')
password = config('password')

def authenticate_ndfc(username, password, NFDC_IP=NFDC_IP):
    url = f"https://{NFDC_IP}/login"
    payload = {
        "userName": username,
        "userPasswd": password,
        "domain": "DefaultAuth"
    }
    response = requests.post(url, auth=HTTPBasicAuth(username, password), verify=False, data=json.dumps(payload))
    print(response.status_code)
    if response.text:
        return response.json()["token"]
    else:
        return None


DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    "Accept": "application/json",
    "dcnm-token": f"{authenticate_ndfc(NFDC_IP=NFDC_IP, username=username, password=password)}"
}

def get_request(endpoint, headers=DEFAULT_HEADERS, verify=False):
    try:
        response = requests.get(endpoint, headers=headers, verify=verify)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError:
        print("No JSON object could be decoded")
    return None

def post_request(endpoint, payload, headers=DEFAULT_HEADERS, verify=False):
    try:
        response = requests.post(endpoint, json=payload, headers=headers, verify=verify)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError:
        print("No JSON object could be decoded")
    return None

def get_inventory_ndfc(endpoint=f"https://{NFDC_IP}/appcenter/cisco/nfdc/api/v1/lan-fabric/rest/inventory/allswitches"):
    response = get_request(endpoint=endpoint)
    return response

def get_policy_ndfc(serial, endpoint=f"https://{NFDC_IP}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/serial_number"):
    endpoint = endpoint.replace("serial_number", serial)
    response = get_request(endpoint=endpoint)

def update_policy(policy_id, config, policy, endpoint=f"https://{NFDC_IP}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies/policy_id"):
    endpoint = endpoint.replace("policy_id", policy_id)
    policy['nvPairs']['CONFIG'] = config
    requests.put(endpoint, data=json.dumps(policy), headers=DEFAULT_HEADERS, verify=False)

def create_policy(payload, endpoint="https://{NFDC_IP}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies/switches"):
    response = post_request(endpoint=endpoint,payload=json.dumps(payload))
    return response

def get_policy_details(policy, endpoint=f"https://{NFDC_IP}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies/shared/details/policy_id"):
    endpoint = endpoint.replace("policy_id", policy)
    response = get_request(endpoint=endpoint)
    return response
