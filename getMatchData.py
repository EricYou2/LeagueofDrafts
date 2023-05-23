import config
import requests
import urllib, json
import csv

api_key = config.API_KEY
BLUE = 0
RED = 1

summoner = "TheGhostPig"
summoner_request = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api_key}"
summoner_info = requests.get(summoner_request).json()
puuid = summoner_info["puuid"]



matches_request= f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=20&api_key={api_key}"
matches = requests.get(matches_request).json()
test_match = matches[0]

specific_match_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/{test_match}?api_key={api_key}"
match_data = requests.get(specific_match_request).json()["info"]
participant_data = match_data["participants"]
team_data = match_data["teams"]
blue_side_bans = []
red_side_bans = []
# Maybe in the future we have role dependency
# red_side_picks = [None, None, None, None, None]
# blue_side_picks = [None, None, None, None, None]
blue_side_picks = []
red_side_picks = []
blue_side_win = team_data[BLUE]["win"]
red_side_win = team_data[RED]["win"]
# game_time =
blue_side = {
    "bans": blue_side_bans,
    "picks": blue_side_picks,
    "win": blue_side_win
}
red_side = {
    "bans": red_side_bans,
    "picks": red_side_picks,
    "win": red_side_win
}
for x in range(5):
    blue_side_picks.append(participant_data[x]["championId"])
for x in range(5,10):
    red_side_picks.append(participant_data[x]["championId"])

for ban in team_data[BLUE]["bans"]:
    blue_side_bans.append(ban["championId"])
for ban in team_data[RED]["bans"]:
    red_side_bans.append(ban["championId"])

print("blue side: ", blue_side)
print("red side: ", red_side)