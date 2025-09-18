import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        "<h1>Hello from Python Function App on Azure!</h1>",
        mimetype="text/html"
    )
