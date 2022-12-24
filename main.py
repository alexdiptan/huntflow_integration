import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
import api_methods

app = FastAPI()

dot_env_path = Path(Path.cwd(), 'config/.env')
if Path.exists(dot_env_path):
    load_dotenv(dot_env_path)

hf_token = os.environ['HF_API_TOKEN']
hf_api_url = os.environ['HF_API_URL']
account_id = os.environ['ORG_ACCOUNT_ID']
hired_account_status_id = int(os.environ['HIRED_ACCOUNT_STATUS_ID'])
tag_name = os.environ['TAG_NAME']
tag_color = os.environ['TAG_COLOR']
headers = {'Authorization': f'Bearer {hf_token}'}


@app.post("/applicant")
async def applicant(request: Request):
    event = request.headers.get("X-Huntflow-Event")

    if event != "APPLICANT":
        return {"status": "ERR"}

    hf_body = await request.json()
    hf_applicant_status = hf_body["event"]["applicant_log"]["status"]

    if hf_applicant_status:
        hf_applicant_status = hf_body["event"]["applicant_log"]["status"]["id"]

    applicant_id = int(hf_body["event"]["applicant"]["id"])

    if hf_applicant_status != hired_account_status_id or not hf_applicant_status:
        return {"status": "EXIT"}

    applicant_tags = api_methods.get_applicant_tags(hf_api_url, account_id, applicant_id, headers)["tags"]
    account_tags = api_methods.get_account_tags(hf_api_url, account_id, headers)
    hired_tag_id = api_methods.find_tag_name_in_account_tags(account_tags, tag_name)

    if not api_methods.find_tag_name_in_account_tags(account_tags, tag_name):
        hired_tag_id = api_methods.create_tag(hf_api_url, account_id, tag_name, tag_color, headers)["id"]

    if hired_tag_id not in applicant_tags:
        applicant_tags.append(hired_tag_id)

    api_methods.update_applicant_tags(hf_api_url, account_id, applicant_id, applicant_tags, headers)

    return {"status": "OK"}
