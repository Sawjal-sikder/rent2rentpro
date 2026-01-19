import requests #type: ignore
from celery import shared_task  # type: ignore
from django.contrib.auth import get_user_model
from service.models import ContractAnalysis, LocationSuitability
User = get_user_model()

def make_agent_request(url: str, payload: dict) -> dict:
    
    if not url or not payload:
        return {"error": "Invalid URL or payload"}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        # print(response.json())
        # print("-------------------------------------------------------------------")
        return response.json()
    except requests.RequestException as e:
        # Log the error or handle it as needed
        print(f"Error making agent request: {e}")
        return {"error": str(e)}
    
    



@shared_task
def make_file_request(url: str, file_path: str, contract_analysis_id: int):
    try:
        # Open and read the file
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            response.raise_for_status()
            result = response.json()
    except requests.RequestException as e:
        # Update the ContractAnalysis with error
        ContractAnalysis.objects.filter(id=contract_analysis_id).update(
            contract_analysis_result={"error": str(e)}
        )
        return {"error": str(e)}

    # Update ContractAnalysis with results
    try:
        ContractAnalysis.objects.filter(id=contract_analysis_id).update(
            contract_analysis_result=result
        )
    except Exception as e:
        return {"error": f"Failed to update ContractAnalysis: {e}"}

    return {"success": True, "analysis_result": result}


@shared_task(bind=True)
def generate_location_request(self, url: str, payload: dict, location_suitability_id: int):
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()

    # Update DB after AI response
    LocationSuitability.objects.filter(
        id=location_suitability_id
    ).update(analysis_summary=data)

    return data