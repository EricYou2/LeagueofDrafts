import config
import requests
import json
import csv
import time

api_key = config.API_KEY
BLUE = 0
RED = 1


def get_top_players():
    leaderboard_request = f"https://na1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1&api_key={api_key}"
    leaderboard_info = requests.get(leaderboard_request).json()
    for info in leaderboard_info[0:155]:
        summoners.append(info["summonerName"])


def get_matches(summoner):
    summoner_request = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api_key}"
    summoner_info = requests.get(summoner_request).json()
    puuid = summoner_info["puuid"]
    # Getting the matches by player id
    matches_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=100&api_key={api_key}"
    matches = requests.get(matches_request).json()
    return matches


def get_specific_match_data(match):
    # Data gathering for the specific match
    specific_match_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}?api_key={api_key}"
    match_data = requests.get(specific_match_request).json()["info"]
    participant_data = match_data["participants"]
    # blue_side_bans = []
    # red_side_bans = []
    blue_side_picks = []
    red_side_picks = []
    # bad data point
    if len(participant_data) == 0:
        blue_side = {
            # "bans": blue_side_bans,
            "picks": [0, 0, 0, 0, 0]
        }
        red_side = {
            # "bans": red_side_bans,
            "picks": [0, 0, 0, 0, 0]
        }
        win = -1
        return (blue_side, red_side, win)
    team_data = match_data["teams"]
    for x in range(5):
        blue_side_picks.append(participant_data[x]["championId"])
    for x in range(5, 10):
        red_side_picks.append(participant_data[x]["championId"])
    # for ban in team_data[BLUE]["bans"]:
    # blue_side_bans.append(ban["championId"])
    # for ban in team_data[RED]["bans"]:
    # red_side_bans.append(ban["championId"])

    # 0 means blue won, 1 means red won
    win = 1
    if team_data[BLUE]["win"]:
        win = 0

    blue_side = {
        # "bans": blue_side_bans,
        "picks": blue_side_picks,
    }
    red_side = {
        # "bans": red_side_bans,
        "picks": red_side_picks,
    }
    return (blue_side, red_side, win)


def create_data_point(blue_side, red_side, win):
    # data_point = (
    #     blue_side["bans"] + blue_side["picks"] + red_side["bans"] + red_side["picks"]
    # )
    data_point = blue_side["picks"] + red_side["picks"]
    data_point.append(win)
    return data_point


def write_to_csv(data):
    fields = [
        # "blue_ban_1",
        # "blue_ban_2",
        # "blue_ban_3",
        # "blue_ban_4",
        # "blue_ban_5",
        "blue_pick_1",
        "blue_pick_2",
        "blue_pick_3",
        "blue_pick_4",
        "blue_pick_5",
        # "red_ban_1",
        # "red_ban_2",
        # "red_ban_3",
        # "red_ban_4",
        # "red_ban_5",
        "red_pick_1",
        "red_pick_2",
        "red_pick_3",
        "red_pick_4",
        "red_pick_5",
        "win",
    ]

    with open("./match_data/matches.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(data)


# -1 means that nothing was banned
summoners = []
data = []
get_top_players()
time.sleep(120)
for summoner in summoners:
    match_list = get_matches(summoner)[0:97]  # riot only allows for 100 API calls every 2 minutes
    for match in match_list:
        blue_side, red_side, win = get_specific_match_data(match)
        data.append(create_data_point(blue_side, red_side, win))
    time.sleep(120)  # riot only allows for 100 API calls every 2 minutes
write_to_csv(data)
print("done")