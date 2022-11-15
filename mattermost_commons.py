import requests

from config import TEAM_ID, LOGIN_ID, PW

AUTH_URL = "https://swib22.collochat.de/api/v4/users/login"
GET_CHANNEL_BY_NAME = "https://swib22.collochat.de/api/v4/teams/{team_id}/channels/name/{channel_name}"
GET_USER_IDS_PER_MAIL = "https://swib22.collochat.de/api/v4/users/email/{email}"
ADD_USER_TO_CHANNEL = "https://swib22.collochat.de/api/v4/channels/{channel_id}/members"
UPDATE_CHANNEL_ROLE = "https://swib22.collochat.de/api/v4/channels/{channel_id}/members/{user_id}/roles"


def get_token():
    r = requests.post(AUTH_URL, json={
        "login_id": LOGIN_ID,
        "password": PW
    })
    return r.headers["Token"]


token = get_token()
auth_headers = {"Authorization": f"Bearer {token}"}


def get_channel_id(channel_name: str) -> str:
    channel_id = requests.get(GET_CHANNEL_BY_NAME.replace(
        "{team_id}", TEAM_ID).replace("{channel_name}", channel_name),
        headers=auth_headers
    ).json()["id"]
    return channel_id


def get_user_ids_by_email(emails: list[str]) -> list[str]:
    user_ids = []
    for email in emails:
        user_id = requests.get(GET_USER_IDS_PER_MAIL.replace(
            "{email}", email),
            headers=auth_headers
        ).json()["id"]
        user_ids.append(user_id)
    return user_ids


def add_user_to_channel(user_id: str, channel_id: str):
    r = requests.post(ADD_USER_TO_CHANNEL.replace("{channel_id}", channel_id),
                      headers=auth_headers,
                      json={
        "user_id": user_id
    }
    )
    if r.status_code != 201:
        print(
            f"Something went wrong while adding {user_id} to channel {channel_id}:")
        print(r.text)


def update_channel_roles(user_id: str, channel_id: str, channel_role: str):
    r = requests.put(UPDATE_CHANNEL_ROLE.replace("{channel_id}", channel_id).replace("{user_id}", user_id),
                      headers=auth_headers,
                      json={
        "roles": channel_role
    }
    )
    if r.status_code != 200:
        print(
            f"Something went wrong while changing role of {user_id} in channel {channel_id} to role {channel_role}:")
        print(r.text)
