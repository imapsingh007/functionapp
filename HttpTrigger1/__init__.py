import logging
import os
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

# Load environment variables
SUBSCRIPTION_ID = os.environ["AZURE_SUBSCRIPTION_ID"]
RESOURCE_GROUP = os.environ["AZURE_RESOURCE_GROUP"]
VM_NAME = os.environ["AZURE_VM_NAME"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing VM control request.')

    # Get action from query param or body
    action = req.params.get('action')
    if not action:
        try:
            req_body = req.get_json()
            action = req_body.get('action')
        except ValueError:
            return func.HttpResponse("Please provide ?action=start or stop", status_code=400)

    # Authenticate using Managed Identity
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)

    # Start VM
    if action.lower() == "start":
        async_vm_start = compute_client.virtual_machines.begin_start(RESOURCE_GROUP, VM_NAME)
        async_vm_start.wait()
        return func.HttpResponse(f"✅ VM {VM_NAME} is starting...", status_code=200)

    # Stop VM
    elif action.lower() == "stop":
        async_vm_stop = compute_client.virtual_machines.begin_deallocate(RESOURCE_GROUP, VM_NAME)
        async_vm_stop.wait()
        return func.HttpResponse(f"🛑 VM {VM_NAME} is stopping...", status_code=200)

    else:
        return func.HttpResponse("Invalid action. Use ?action=start or stop", status_code=400)
