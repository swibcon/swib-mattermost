# Workshop API procedures for SWIB

These scripts do the following things:
- creating workshop channels
- adding the participants and facilitators
- creating the facilitator workshop channel
- adding all facilitators to the facilitators channel

What happens depends on the settings in `config.yaml` and the scripts you run.

Be cautious: Even when using `test_run: true` users will be added to the test-team-channels. This might confuse them and not be what you want.

The scripts depend on the xml-files generated with the `get_conftool_data.sh` script from the parent folder. Make sure to have run it, before running the python scripts.
Add the path to the folder with the generated xml files to `path_to_data`

## Installation


1. Make a virtual environment `python -m venv venv`
2. Install requirements `pip install -r requirements.txt`
3. `cp .env.example .env`
4. `cp config.yaml.example config.yaml`

Decide what you want to do, with configuration of `config.yaml`-file.

For working on the Test-Channel, set `test_run: true`.

## Create Workshop Channels

- set `create_ws_channels: true`
- if you also wanto to create the Facilitators Channel set `create_facilitators_channel: true`. Edit the other Facilitator channel settings to your liking.
- `event_filter` lets you filter out certain events. It defaults to "Full Conference", "nows", "nowl". To filter out additional workshops add them.

To create the workshop channels run `python create_channels.py`

## Add users to channel

- set `add_participants: true`
- set `add_facilitators: true`

To add the users run `python add_users.py` (be cautious, even if in test run this will add all the users to the Test-Team Channels)

