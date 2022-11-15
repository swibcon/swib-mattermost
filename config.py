import os
from dotenv import load_dotenv
import yaml

load_dotenv()

with open("config.yaml", mode="rt", encoding="utf-8") as file:
    config = yaml.safe_load(file)



LOGIN_ID = os.getenv("LOGIN_ID")
PW = os.getenv("PW")

SWIB = os.getenv("SWIB")


TEST_TEAM = config["test_team"]
SWIB_TEAM = config["swib_team"]

TEAM_ID = TEST_TEAM if config["test_run"] else SWIB_TEAM
