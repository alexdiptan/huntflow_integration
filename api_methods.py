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


def get_account_vacancies_statuses(api_url: str, headers: dict, org_id: str) -> dict:
    response = requests.get(f'{api_url}/v2/accounts/{org_id}/vacancies/statuses', headers=headers)
    response.raise_for_status()

    return response.json()


def get_accounts(api_url: str, headers: dict) -> dict:
    response = requests.get(f'{api_url}/v2/accounts', headers=headers)
    response.raise_for_status()

    return response.json()


def get_hired_vacancy_status_id(vacancy_statuses: dict) -> int:
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
    if not Path.exists(dot_env_path):
        print('File .env is not loaded')

    load_dotenv(dot_env_path)
    hf_token = os.environ['HF_API_TOKEN']
    hf_api_url = os.environ['HF_API_URL']
    account_id = os.environ['HF_ORG_ACCOUNT_ID']
    hired_account_status_id = os.environ['HF_HIRED_ACCOUNT_STATUS_ID']
    tag_name = os.environ['TAG_NAME']
    tag_color = os.environ['TAG_COLOR']
    headers = {'Authorization': f'Bearer {hf_token}'}

    vacancy_statuses = get_account_vacancies_statuses(hf_api_url, headers, account_id)
    pprint(vacancy_statuses)
    # hired_status_id = get_hired_vacancy_status_id(vacancy_statuses)

    account_tags = get_account_tags(hf_api_url, account_id, headers)
    # pprint(account_tags)

    account_tags = get_account_tags(hf_api_url, account_id, headers)
    hired_tag_id = find_tag_name_in_account_tags(account_tags, tag_name)
    # delete_account_tag(hf_api_url, account_id, hired_tag_id, headers)
    if not find_tag_name_in_account_tags(account_tags, tag_name):
        hired_tag_id = create_tag(hf_api_url, account_id, tag_name, tag_color, headers)
    #
    print(f'{account_tags=}')
    # pprint(get_applicant_tags(hf_api_url, account_id, 129, headers))

    # applicant_tags = [76, 76]

    # print(update_applicant_tags(hf_api_url, account_id, 129, applicant_tags, headers))


if __name__ == '__main__':
    main()
