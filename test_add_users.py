from config import config
from mattermost_commons import get_channel_id, get_user_ids_by_email, add_user_to_channel, update_channel_roles
from parse_sessions import ws_facilitators_emails


# for testing
test_user_email = "j.neubert-test@zbw.eu"

def add_users_to_channels(user_emails: list[str], channel_name: str):
    channel_id = get_channel_id(channel_name)
    user_ids = get_user_ids_by_email(user_emails)

    for user_id in user_ids:
        add_user_to_channel(user_id, channel_id)


def make_facilitators_channel_admins(channel_admin_emails: list[str], channel_name: str):
    channel_id = get_channel_id(channel_name)
    user_ids = get_user_ids_by_email(channel_admin_emails)

    for user_id in user_ids:
        update_channel_roles(user_id, channel_id, "channel_admin")


def main():
    if config["add_facilitators"]:
        print("adding facilitators to channel")
        add_users_to_channels([test_user_email], config["ws_facilitators_channel"]["name"])
    
    if config["add_participants"]:
        print("adding workshop participants to their workshop channels")
        from parse_events import events
        for event in events:
            add_users_to_channels([test_user_email], events[event]["name"])
            make_facilitators_channel_admins([test_user_email], events[event]["name"])
        

if __name__ == "__main__":
    main()