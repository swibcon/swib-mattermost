import requests

from config import TEAM_ID, config
from mattermost_commons import auth_headers, get_channel_id


CREATE_CHANNELS_URL = "https://swib22.collochat.de/api/v4/channels"
USER_BY_MAIL_URL = f"https://swib22.collochat.de/api/v4/users/email/"


def update_channel(event: dict):
    channel_id = get_channel_id(event["name"])

    r = requests.put(CREATE_CHANNELS_URL + f"/{channel_id}",
                     headers=auth_headers,
                     json={
                         "id": channel_id,
                         "name": f"{event['name']}",
                         "display_name": f"{event['display_name']}",
                         "purpose": f"{event['purpose']}",
                         "header": f"{event['header']}"
                     })
    if r.status_code != 200:
        print(f"error for channel: {event}")


def create_channels(events: dict):
    for event in events:
        r = requests.post(CREATE_CHANNELS_URL,
                        headers=auth_headers,
                        json={
                            "team_id": TEAM_ID,
                            "name": f"{event}",
                            "display_name": f"{events[event]['display_name']}",
                            "purpose": f"{events[event]['purpose']}",
                            "header": f"{events[event]['header']}",
                            "type": f"{events[event]['type']}"
                        })

        if r.json()["id"] == "store.sql_channel.save_channel.exists.app_error":
            if not config["channel_update"]:
                print(
                    "Channel already exists. So you might wanted to update it? Set channel_update to 'true' in your .env")
            else:
                print("Channel already exsits, updating...")
                update_channel(auth_headers, events[event])


def main():
    if config["create_ws_channels"]:
        print("Creating workshop channels...")

        from parse_events import events
        create_channels(events)

    if config["create_facilitators_channel"]:
        print("Creating Workshop-Facilitators channel")
        event = {
            "team_id": TEAM_ID,
            "name": config["ws_facilitators_channel"]["name"],
            "display_name": config["ws_facilitators_channel"]["display_name"],
            "purpose": config["ws_facilitators_channel"]["purpose"],
            "header": config["ws_facilitators_channel"]["header"],
            "type": config["ws_facilitators_channel"]["type"]
        }
        create_channels({"ws-facilitators": event})


if __name__ == "__main__":
    main()
