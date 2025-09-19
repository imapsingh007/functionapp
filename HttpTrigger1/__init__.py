import logging
import os
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    resource_group = os.environ["AZURE_RESOURCE_GROUP"]
    vm_name = os.environ["AZURE_VM_NAME"]

    action = req.params.get("action")
    if not action:
        try:
            req_body = req.get_json()
        except:
            pass
        else:
            action = req_body.get("action")

    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    try:
        if action == "start":
            async_vm_start = compute_client.virtual_machines.begin_start(resource_group, vm_name)
            async_vm_start.result()
            return func.HttpResponse(f"VM {vm_name} started successfully.", status_code=200)

        elif action == "stop":
            async_vm_stop = compute_client.virtual_machines.begin_power_off(resource_group, vm_name)
            async_vm_stop.result()
            return func.HttpResponse(f"VM {vm_name} stopped successfully.", status_code=200)

        else:
            return func.HttpResponse("Please provide a valid action (start/stop).", status_code=400)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
