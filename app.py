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

from flask import Flask, render_template, request, make_response, jsonify
from flask_cors import CORS
from utils import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    fabrics = get_fabrics(endpoint=f"https://{base_url}/rest/control/fabrics")
    print(fabrics)
    return render_template('index.html', fabrics=fabrics)


@app.route('/fabric/switches', methods=['GET', 'POST'])
def get_fabric_switches():
    if request.method == 'POST':
        # Get the selected fabric from the form
        selected_fabric = request.form.get('fabric')

        # Now you can process the selected fabric as needed
        # For example, print it to the console:
        print("Selected Fabric:", selected_fabric)
        inventory = get_fabric_inventory(selected_fabric)

    # If it's a GET request or after processing the POST request, render the template
    return render_template('inventory.html', switches=inventory)

@app.route('/device/policy', methods=['GET', 'POST'])
def get_device_policies():
    if request.method == 'POST':
        # Get the selected fabric from the form
        selected_device = request.form.get('device')

        # Now you can process the selected fabric as needed
        # For example, print it to the console:
        print("Selected device:", selected_device)
        policies = [policy for policy in get_switch_policy(serial=selected_device) if "CONF" in policy['nvPairs'] and policy['nvPairs']['CONF'] != ""]

    # If it's a GET request or after processing the POST request, render the template
    return render_template('policies.html', policies=policies, serial=selected_device)

@app.route('/<serial>/get-policy/<policyId>', methods=['GET'])
def get_policy(serial, policyId):
    for policy in get_switch_policy(serial=serial):
        if policy['policyId'] == policyId:
            p = policy
            break

    response_data = {'current_config': p['nvPairs']['CONF']}
    response = make_response(jsonify(response_data), 200)
    return response
@app.route('/device/<serial>/policy/edit', methods=['GET','POST'])
def edit_policy(serial):
    selected_policy = request.form.get('policy')
    new_config = request.form.get('config')
    for policy in get_switch_policy(serial=serial):
        if policy['policyId'] == selected_policy:
            p = policy
            break
    edit_freeform_policy(policy=p, config=new_config)
    policies = [policy for policy in get_switch_policy(serial=serial) if
                "CONF" in policy['nvPairs'] and policy['nvPairs']['CONF'] != ""]

    return render_template('policies.html', policies=policies, serial=serial)
if __name__ == '__main__':
    app.run(debug=True)
