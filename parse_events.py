import xml.etree.ElementTree as ET

from config import config
from parse_sessions import workshops

event_filter = []

if config["event_filter"]:
    event_filter.extend(config["event_filter"])

print(f"These events will be filtered out: {', '.join(event_filter)} ")

def collect_participants_for_events(root):
    """
    Collects the events and filters them.
    Beautifies the title with the ⚒️ Symbol and titlezies the shorttitle.
    """
    events = {}

    for participant in root:
        event_shorttitle = participant.find("event_shorttitle").text

        if (
            event_shorttitle not in event_filter and
            not event_shorttitle.endswith("-wl")
        ):
            events.setdefault(event_shorttitle, {
                "participants": [],
                "event_title": participant.find("event_title").text
            })

        if event_shorttitle in events.keys():
            events[event_shorttitle]["participants"].append(participant.find(
                "email").text)

    events = enrich_event_data(events)

    return events


def enrich_event_data(events):
    """
    Enrichtes the events with data needed for Mattermost Channel creation
    """
    for event in events:
        events[event]["display_name"] = f"⚒️ {event.title()} - Workshop"
        events[event]["name"] = event
        events[event]["purpose"] = f"""Chat for the participants and facilitators of the Workshop: '{events[event]["event_title"]}'"""
        events[event]["header"] = ""
        events[event]["type"] = "P"
        # to get the channel admins, we compare the workshop titles from both data sets, since these are shared between the data sources (session.xml and events_participants.xml)
        events[event]["channel_admins"] = list(*[item["ws_facilitators_emails"] for item in workshops if item["ws_title"] == events[event]["event_title"]])
    return events


def parse_events_participants():
    tree = ET.parse(f"{config['path_to_data']}/event_participants.xml")
    root = tree.getroot()

    events = collect_participants_for_events(root)

    return events


events = parse_events_participants()


if __name__ == "__main__":
    parse_events_participants()
