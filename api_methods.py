import os
from pathlib import Path
from pprint import pprint

import requests
from dotenv import load_dotenv


def update_applicant_tags(api_url: str, org_id: str, applicant_id: int, applicant_tags: list, headers: dict) -> int:
    payload = {"tags": applicant_tags}
    response = requests.post(f'{api_url}/v2/accounts/{org_id}/applicants/{applicant_id}/tags', headers=headers,
                             json=payload)
    response.raise_for_status()

    return response.status_code


def get_applicant_tags(api_url: str, org_id: str, applicant_id: int, headers: dict) -> dict:
    response = requests.get(f'{api_url}/v2/accounts/{org_id}/applicants/{applicant_id}/tags', headers=headers)
    response.raise_for_status()

    return response.json()


def delete_account_tag(api_url: str, org_id: str, tag_id: int, headers: dict) -> int:
    response = requests.delete(f'{api_url}/v2/accounts/{org_id}/tags/{tag_id}', headers=headers)
    response.raise_for_status()

    return response.status_code


def create_tag(api_url: str, org_id: str, tag_name: str, color: str, headers: dict, ) -> dict:
    payload = {"name": tag_name,
               "color": color,
               }
    response = requests.post(f'{api_url}/v2/accounts/{org_id}/tags', headers=headers, json=payload)
    response.raise_for_status()

    return response.json()


def get_account_tags(api_url: str, org_id: str, headers: dict) -> dict:
    response = requests.get(f'{api_url}/v2/accounts/{org_id}/tags', headers=headers)
    response.raise_for_status()

    return response.json()


def get_account_vacancies_statuses(api_url: str, org_id: str, headers: dict) -> dict:
    response = requests.get(f'{api_url}/v2/accounts/{org_id}/vacancies/statuses', headers=headers)
    response.raise_for_status()

    return response.json()


def get_accounts(api_url: str, headers: dict) -> dict:
    response = requests.get(f'{api_url}/v2/accounts', headers=headers)
    response.raise_for_status()

    return response.json()


def get_hired_vacancy_status_id(vacancy_statuses: dict):
    hired_status_id = None
    for vacancy_status in vacancy_statuses['items']:
        if 'hired' in vacancy_status.values():
            hired_status_id = vacancy_status['id']

    return hired_status_id


def find_tag_name_in_account_tags(account_tags: dict, account_tag_name: str):
    tag_id = None
    for account_tag in account_tags['items']:
        if account_tag_name in account_tag.values():
            tag_id = account_tag['id']

    return tag_id


def main():
    dot_env_path = Path(Path.cwd(), 'config/.env')
    if Path.exists(dot_env_path):
        load_dotenv(dot_env_path)

    load_dotenv(dot_env_path)

    hf_token = os.environ['HF_API_TOKEN']
    hf_api_url = os.environ['HF_API_URL']
    org_id = os.environ['ORG_ID']
    headers = {'Authorization': f'Bearer {hf_token}'}

    accounts_by_token = get_accounts(hf_api_url, headers)
    account_vacancy_statuses = get_account_vacancies_statuses(hf_api_url, org_id, headers)
    hired_status_id = get_hired_vacancy_status_id(account_vacancy_statuses)


if __name__ == '__main__':
    main()
