import os
from pathlib import Path
from pprint import pprint

from dotenv import load_dotenv
from fastapi import FastAPI, Request
import api_methods

app = FastAPI()

dot_env_path = Path(Path.cwd(), 'config/.env')
if Path.exists(dot_env_path):
    load_dotenv(dot_env_path)

hf_token = os.environ['HF_API_TOKEN']
hf_api_url = os.environ['HF_API_URL']
account_id = os.environ['ORG_ID']
start_vacancy_status_id = os.environ['START_VACANCY_STATUS_ID']
hired_account_status_id = int(os.environ['HIRED_STATUS_ID'])
vacancy_position = os.environ['VACANCY_POSITION']
tag_name = os.environ['TAG_NAME']
tag_color = os.environ['TAG_COLOR']
headers = {'Authorization': f'Bearer {hf_token}'}


@app.post("/vacancy")
async def applicant(request: Request):
    event = request.headers.get("X-Huntflow-Event")

    if event != "VACANCY":
        return {"status": "ERR: event is not VACANCY"}

    hf_body = await request.json()
    vacancy_state = hf_body["event"]["vacancy_log"]["state"]

    if vacancy_state != "CREATED":
        return {"status": "ERR: Vacancy state is not CREATED"}

    vacancy_id = hf_body["event"]["vacancy"]["id"]
    created_vacancy_position = hf_body["event"]["vacancy"]["position"]
    applicants_with_requested_position = api_methods.search_applicants_with_position(hf_api_url, account_id,
                                                                                     vacancy_position,
                                                                                     headers)
    if applicants_with_requested_position['total_items'] == 0:
        return {"status": "ERR: There is no applicant without vacancy or needed position name"}

    applicant_id = applicants_with_requested_position['items'][0]['id']

    if created_vacancy_position != vacancy_position:
        return {"status": "ERR: Vacancy position is not equal applicant position"}

    api_methods.add_applicant_to_vacancy(hf_api_url, account_id, applicant_id, vacancy_id,
                                         start_vacancy_status_id, headers)

    return {"status": "OK"}


@app.post("/applicant")
async def applicant(request: Request):
    event = request.headers.get("X-Huntflow-Event")

    if event != "APPLICANT":
        return {"status": "ERR: event is not APPLICANT"}

    hf_body = await request.json()
    hf_applicant_status = hf_body["event"]["applicant_log"]["status"]

    if hf_applicant_status:
        hf_applicant_status = hf_body["event"]["applicant_log"]["status"]["id"]

    applicant_id = int(hf_body["event"]["applicant"]["id"])

    if hf_applicant_status != hired_account_status_id or not hf_applicant_status:
        return {"status": "ERR: Status not a hired"}

    applicant_tags = api_methods.get_applicant_tags(hf_api_url, account_id, applicant_id, headers)["tags"]
    account_tags = api_methods.get_account_tags(hf_api_url, account_id, headers)
    hired_tag_id = api_methods.find_tag_name_in_account_tags(account_tags, tag_name)

    if not api_methods.find_tag_name_in_account_tags(account_tags, tag_name):
        hired_tag_id = api_methods.create_tag(hf_api_url, account_id, tag_name, tag_color, headers)["id"]

    if hired_tag_id not in applicant_tags:
        applicant_tags.append(hired_tag_id)

    api_methods.update_applicant_tags(hf_api_url, account_id, applicant_id, applicant_tags, headers)

    return {"status": "OK"}
