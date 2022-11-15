import xml.etree.ElementTree as ET
from config import config

def has_speaker_status(parents: list[ET.Element]) -> ET.Element:
    """
    checks if the author has a speaker status. If so we can be pretty sure,
    we found the right participant.
    This might be necessary because there might be common first and last name participants.
    But that there are two persons having the same first and last name and both being
    speakers seems pretty unlikely.
    """
    for parent_element in parents:
        if "speaker" in parent_element.findtext("user_status"):
            return parent_element


def lookup_email(authors: list[str]) -> list:
    tree = ET.parse(f"{config['path_to_data']}/participants.xml")
    root = tree.getroot()
    emails = []

    for author in authors:
        last, first = author.split(", ")
        firstname_parent_matches = root.findall(f".//firstname[.='{first.strip()}']..")
        lastname_parent_matches =  root.findall(f".//name[.='{last.strip()}']..")

        parent_matches = set([*firstname_parent_matches, *lastname_parent_matches])
        if parent:=has_speaker_status(parent_matches):
            emails.append(parent.findtext("email"))
        else:
            print(f"Error: Did not find participant: {first} {last} in participant list!")

    return emails


def parse_sessions_for_mails():
    tree = ET.parse(f"{config['path_to_data']}/sessions.xml")
    root = tree.getroot()

    # Workshops are identified by session_short = ws
    ws_parent = root.find("./session/session_short[.='ws']..")
    num_presentations = int(ws_parent.findtext("presentations"))

    ws = []
    for i in range(num_presentations):
        authors_string = ws_parent.findtext(f"p{i+1}_presenting_author")
        authors = [author for author in authors_string.split(";")]
        emails = lookup_email(authors)
        ws.append({
            "ws_facilitators_emails": emails,
            "ws_title": ws_parent.findtext(f"p{i+1}_title")
        })
    return ws

workshops = parse_sessions_for_mails()

# flat_list = [item for sublist in l for item in sublist]
ws_facilitators_emails = [item for sublist in [item['ws_facilitators_emails'] for item in workshops] for item in sublist]