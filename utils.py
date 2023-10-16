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
from prettyprinter import pprint
from decouple import config

# Fetch the variables from the .env file
base_url = config('DCNM_IP')
username = config('username')
password = config('password')


def authenticate(base_url, username, password):
    url = f"https://{base_url}/rest/logon"
    payload = {
        "expirationTime": 90000000
    }
    response = requests.post(url, auth=HTTPBasicAuth(username, password), verify=False, data=json.dumps(payload))
    print(response.status_code)
    if response.text:
        return response.json()["Dcnm-Token"]
    else:
        return None


DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    "Accept": "application/json",
    "dcnm-token": f"{authenticate(base_url=base_url, username='admin', password='Cisco1234!')}"
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


def authenticate(base_url, username, password):
    url = f"https://{base_url}/rest/logon"
    response = requests.post(url, auth=HTTPBasicAuth(username, password), verify=False)
    print(response.status_code)
    print(response.text)
    if response.text:
        return response.json()
    else:
        return None


def find_static_routes(config_data):
    pattern = r"ip route (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?: (\d+))?"
    matches = re.findall(pattern, config_data)
    for match in matches:
        yield match


def create_freeform_policy(serial, config, endpoint=f"https://{base_url}/rest/control/policies/bulk-create"):
    payload = {"serialNumber": serial, "entityType": "SWITCH", "entityName": "SWITCH",
               "templateName": "switch_freeform", "priority": "500", "nvPairs": {"CONF": config}}
    response = post_request(endpoint=endpoint, payload=payload)
    return response


def get_switch_policy(serial,
                      endpoint=f"https://{base_url}/rest/control/policies/switches?serialNumber=serial_number", ):
    endpoint = endpoint.replace("serial_number", serial)
    response = get_request(endpoint)
    pprint(response)
    return response


def edit_freeform_policy(policy: dict, config, base_url=base_url, headers=DEFAULT_HEADERS):
    url = f"https://{base_url}/rest/control/policies/{policy['policyId']}"
    policy['nvPairs']['CONF'] = config
    response = requests.put(url, headers=headers, verify=False, data=json.dumps(policy))
    print(response.status_code)
    return response.json()


def get_fabrics(endpoint):
    fabrics = get_request(endpoint=endpoint)
    return fabrics


def get_fabric_inventory(fabric, endpoint=f"https://{base_url}/rest/control/fabrics/fabric_name/inventory", ):
    endpoint = endpoint.replace('fabric_name', fabric)
    response = get_request(endpoint=endpoint)
    return response


def get_all_fabric_inventories(fabrics):
    for fabric in fabrics:
        inventory = get_fabric_inventory(fabric['fabricName'])
        for switch in inventory:
            yield switch
