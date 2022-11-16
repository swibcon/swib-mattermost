from config import config
from mattermost_commons import get_channel_id, get_user_ids_by_email, add_user_to_channel, update_channel_role
from parse_sessions import ws_facilitators_emails


def add_users_to_channels(user_emails: list[str], channel_name: str):
    channel_id = get_channel_id(channel_name)
    user_ids = get_user_ids_by_email(user_emails)

    if config["test_run"]:
        print(f"Test Run: Would add {len(user_ids)} to channel {channel_name}")
        return

    for user_id in user_ids:
        add_user_to_channel(user_id, channel_id)
        update_channel_role(user_id, channel_id, admin_user=False)


def make_facilitators_channel_admins(channel_admin_emails: list[str], channel_name: str):
    channel_id = get_channel_id(channel_name)
    user_ids = get_user_ids_by_email(channel_admin_emails)

    if config["test_run"]:
        print(f"Test Run: Would add {len(user_ids)} to channel {channel_name}")
        return

    for user_id in user_ids:
        update_channel_role(user_id, channel_id, admin_user=True)


def main():
    if config["add_facilitators"]:
        print("adding facilitators to channel")
        add_users_to_channels(ws_facilitators_emails, config["ws_facilitators_channel"]["name"])
    
    if config["add_participants"]:
        print("adding workshop participants to their workshop channels")
        from parse_events import events
        for event in events:
            add_users_to_channels(events[event]["participants"], events[event]["name"])

            # not all facilitators are also registered in their workshop, 
            # therefore we add them to the channel first to later make them admin
            add_users_to_channels(events[event]["channel_admins"], events[event]["name"])
            make_facilitators_channel_admins(events[event]["channel_admins"], events[event]["name"])
        

if __name__ == "__main__":
    main()