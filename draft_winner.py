import tkinter
import customtkinter
import requests
import json
from PIL import Image
from io import BytesIO
import pandas as pd
from keras.models import load_model
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_champ_name(id):
    for champ in champions:
        if champions[champ]['key'] == id:
            return True, champ, champions[champ]['name']
    return False, "Champ does not exist", "extra"

def get_champ_id(name):
    for champ in champions:
        if champ.lower() == name:
            return True, int(champions[champ]['key'])
    return False, 0

def get_champ_image(id):
    state, champ, _ = get_champ_name(id)
    if state:
        champ_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champ}.png"
        response = requests.get(champ_url).content
        champ_icon = Image.open(BytesIO(response))
        return champ_icon
    return ""

version_url = 'https://ddragon.leagueoflegends.com/api/versions.json'
versions = requests.get(version_url).json()
version = versions[0]

data_dragon_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
data_dragon_data = requests.get(data_dragon_url).json()
champions = data_dragon_data["data"]

champs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model = load_model(resource_path("tfmodel"))
positions = ["blue_pick_1", "blue_pick_2", "blue_pick_3", "blue_pick_4", "blue_pick_5", "red_pick_1", "red_pick_2", "red_pick_3", "red_pick_4", "red_pick_5"]

def winner():
    winner_helper(winner_label, confidence_label)

def winner_helper(win_label, conf_label):
    if 0 in champs:
        win_label.configure(text = "Fill in all champion fields", font = ("Arial", 17))
        conf_label.configure(text = "Spell champions correctly", font = ("Arial", 17))
        return
    data_point = pd.DataFrame([champs], columns = positions)
    confidence = model.predict(data_point, verbose=0)
    winner = [0 if val < 0.5 else 1 for val in confidence]
    if winner[0] == 0:
        winner = "Blue Side"
        confidence = 1 - confidence
    else:
        winner = "Red Side"
    win_label.configure(text = f"Winning Draft: {winner}", font = ("Arial", 20))
    conf_label.configure(text = f"Confidence: {confidence[0][0]: .2f}", font = ("Arial", 20))
    return
    

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x600")
app.resizable(False, False)
app.title("LeagueofDrafts")


def update(position, icon, label, role):
    input = position.get().lower()
    if input == "":
        input = "a"
    input = input.replace(" ", "").replace("'", "")
    result, id = get_champ_id(input)
    if result:
        image_input = get_champ_image(f"{id}")
    else:
        image_input = Image.open(resource_path("-1.png"))
    new_image = customtkinter.CTkImage(image_input, size = (50,50))
    icon.configure(image = new_image)
    icon.image = new_image
    outcome, first, second = get_champ_name(f"{id}")
    if outcome:
        new_text = f"{role}: {second}"
    else:
        new_text = f"{role}:"
    label.configure(text=new_text)
    return id
        

def set_blue_picks():
    champs[0] = update(blue_top_pick, blue_top_icon, blue_top_label, "Top")
    champs[1] = update(blue_jg_pick, blue_jg_icon, blue_jg_label, "Jungle")
    champs[2] = update(blue_mid_pick, blue_mid_icon, blue_mid_label, "Mid")
    champs[3] = update(blue_bot_pick, blue_bot_icon, blue_bot_label, "Bot")
    champs[4] = update(blue_supp_pick, blue_supp_icon, blue_supp_label, "Support")

def set_red_picks():
    champs[5] = update(red_top_pick, red_top_icon, red_top_label, "Top")
    champs[6] = update(red_jg_pick, red_jg_icon, red_jg_label, "Jungle")
    champs[7] = update(red_mid_pick, red_mid_icon, red_mid_label, "Mid")
    champs[8] = update(red_bot_pick, red_bot_icon, red_bot_label, "Bot")
    champs[9] = update(red_supp_pick, red_supp_icon, red_supp_label, "Support")




blue_side = customtkinter.CTkFrame(master = app, fg_color = "#AAD0FD", width = 318, height = 460, corner_radius = 10)
blue_side.place(x = 28, y = 13)
blue_side.pack_propagate(False)
blue_title = customtkinter.CTkLabel(blue_side, text = "Blue Side", font = ("Arial", 20), text_color = "black")
blue_title.pack(side = "top", pady = 10)



blue_top_frame = customtkinter.CTkFrame(master = blue_side, fg_color = "#AAD0FD")
blue_top_frame.pack(pady = 8)
blue_top_input_frame = customtkinter.CTkFrame(master = blue_top_frame, fg_color = "#AAD0FD")
blue_top_input_frame.pack(side = "left", padx = 20)
blue_top_label = customtkinter.CTkLabel(master = blue_top_input_frame, text = "Top:", text_color = "black")
blue_top_label.pack()
blue_top_pick = customtkinter.CTkEntry(master = blue_top_input_frame, placeholder_text = "Top...")
blue_top_pick.pack()
blue_top_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
blue_top_icon = customtkinter.CTkLabel(master = blue_top_frame, image = blue_top_image, text = "")
blue_top_icon.pack(side = "right", padx = 20)



blue_jg_frame = customtkinter.CTkFrame(master = blue_side, fg_color = "#AAD0FD")
blue_jg_frame.pack(pady = 8)
blue_jg_input_frame = customtkinter.CTkFrame(master = blue_jg_frame, fg_color = "#AAD0FD")
blue_jg_input_frame.pack(side = "left", padx = 20)
blue_jg_label = customtkinter.CTkLabel(master = blue_jg_input_frame, text = "Jungle:", text_color = "black")
blue_jg_label.pack()
blue_jg_pick = customtkinter.CTkEntry(master = blue_jg_input_frame, placeholder_text = "Jungle...")
blue_jg_pick.pack()
blue_jg_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
blue_jg_icon = customtkinter.CTkLabel(master = blue_jg_frame, image = blue_jg_image, text = "")
blue_jg_icon.pack(side = "right", padx = 20)


blue_mid_frame = customtkinter.CTkFrame(master = blue_side, fg_color = "#AAD0FD")
blue_mid_frame.pack(pady = 8)
blue_mid_input_frame = customtkinter.CTkFrame(master = blue_mid_frame, fg_color = "#AAD0FD")
blue_mid_input_frame.pack(side = "left", padx = 20)
blue_mid_label = customtkinter.CTkLabel(master = blue_mid_input_frame, text = "Mid:", text_color = "black")
blue_mid_label.pack()
blue_mid_pick = customtkinter.CTkEntry(master = blue_mid_input_frame, placeholder_text = "Mid...")
blue_mid_pick.pack()
blue_mid_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
blue_mid_icon = customtkinter.CTkLabel(master = blue_mid_frame, image = blue_mid_image, text = "")
blue_mid_icon.pack(side = "right", padx = 20)


blue_bot_frame = customtkinter.CTkFrame(master = blue_side, fg_color = "#AAD0FD")
blue_bot_frame.pack(pady = 8)
blue_bot_input_frame = customtkinter.CTkFrame(master = blue_bot_frame, fg_color = "#AAD0FD")
blue_bot_input_frame.pack(side = "left", padx = 20)
blue_bot_label = customtkinter.CTkLabel(master = blue_bot_input_frame, text = "Bot:", text_color = "black")
blue_bot_label.pack()
blue_bot_pick = customtkinter.CTkEntry(master = blue_bot_input_frame, placeholder_text = "Bot...")
blue_bot_pick.pack()
blue_bot_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
blue_bot_icon = customtkinter.CTkLabel(master = blue_bot_frame, image = blue_bot_image, text = "")
blue_bot_icon.pack(side = "right", padx = 20)

blue_supp_frame = customtkinter.CTkFrame(master = blue_side, fg_color = "#AAD0FD")
blue_supp_frame.pack(pady = 8)
blue_supp_input_frame = customtkinter.CTkFrame(master = blue_supp_frame, fg_color = "#AAD0FD")
blue_supp_input_frame.pack(side = "left", padx = 20)
blue_supp_label = customtkinter.CTkLabel(master = blue_supp_input_frame, text = "Support:", text_color = "black")
blue_supp_label.pack()
blue_supp_pick = customtkinter.CTkEntry(master = blue_supp_input_frame, placeholder_text = "Support...")
blue_supp_pick.pack()
blue_supp_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
blue_supp_icon = customtkinter.CTkLabel(master = blue_supp_frame, image = blue_supp_image, text = "")
blue_supp_icon.pack(side = "right", padx = 20)

blue_lock_in = customtkinter.CTkButton(blue_side, text = "Lock In", command = set_blue_picks, text_color = "white",hover = True,
    hover_color = "#3f98d7",
    height = 40,
    width = 120,
    border_width = 2,
    corner_radius = 20,
    border_color = "#2d6f9e", 
    fg_color = "#3b8cc6")
blue_lock_in.pack(pady = 5) 



red_side = customtkinter.CTkFrame(master = app, fg_color = "#F1B1B1", width = 318, height = 460, corner_radius = 10)
red_side.place(x = 374, y = 13)
red_side.pack_propagate(False)
red_title = customtkinter.CTkLabel(red_side, text = "Red Side", font = ("Arial", 20), text_color = "black")
red_title.pack(side = "top", pady = 10)


red_top_frame = customtkinter.CTkFrame(master = red_side, fg_color = "#F1B1B1")
red_top_frame.pack(pady = 8)
red_top_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
red_top_icon = customtkinter.CTkLabel(master = red_top_frame, image = red_top_image, text = "")
red_top_icon.pack(side = "left", padx = 20)
red_top_input_frame = customtkinter.CTkFrame(master = red_top_frame, fg_color = "#F1B1B1")
red_top_input_frame.pack(side = "right", padx = 20)
red_top_label = customtkinter.CTkLabel(master = red_top_input_frame, text = "Top:", text_color = "black")
red_top_label.pack()
red_top_pick = customtkinter.CTkEntry(master = red_top_input_frame, placeholder_text = "Top...")
red_top_pick.pack()



red_jg_frame = customtkinter.CTkFrame(master = red_side, fg_color = "#F1B1B1")
red_jg_frame.pack(pady = 8)
red_jg_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
red_jg_icon = customtkinter.CTkLabel(master = red_jg_frame, image = red_jg_image, text = "")
red_jg_icon.pack(side = "left", padx = 20)
red_jg_input_frame = customtkinter.CTkFrame(master = red_jg_frame, fg_color = "#F1B1B1")
red_jg_input_frame.pack(side = "right", padx = 20)
red_jg_label = customtkinter.CTkLabel(master = red_jg_input_frame, text = "Jungle:", text_color = "black")
red_jg_label.pack()
red_jg_pick = customtkinter.CTkEntry(master = red_jg_input_frame, placeholder_text = "Jungle...")
red_jg_pick.pack()


red_mid_frame = customtkinter.CTkFrame(master = red_side, fg_color = "#F1B1B1")
red_mid_frame.pack(pady = 8)
red_mid_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
red_mid_icon = customtkinter.CTkLabel(master = red_mid_frame, image = red_mid_image, text = "")
red_mid_icon.pack(side = "left", padx = 20)
red_mid_input_frame = customtkinter.CTkFrame(master = red_mid_frame, fg_color = "#F1B1B1")
red_mid_input_frame.pack(side = "right", padx = 20)
red_mid_label = customtkinter.CTkLabel(master = red_mid_input_frame, text = "Mid:", text_color = "black")
red_mid_label.pack()
red_mid_pick = customtkinter.CTkEntry(master = red_mid_input_frame, placeholder_text = "Mid...")
red_mid_pick.pack()


red_bot_frame = customtkinter.CTkFrame(master = red_side, fg_color = "#F1B1B1")
red_bot_frame.pack(pady = 8)
red_bot_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
red_bot_icon = customtkinter.CTkLabel(master = red_bot_frame, image = red_bot_image, text = "")
red_bot_icon.pack(side = "left", padx = 20)
red_bot_input_frame = customtkinter.CTkFrame(master = red_bot_frame, fg_color = "#F1B1B1")
red_bot_input_frame.pack(side = "right", padx = 20)
red_bot_label = customtkinter.CTkLabel(master = red_bot_input_frame, text = "Bot:", text_color = "black")
red_bot_label.pack()
red_bot_pick = customtkinter.CTkEntry(master = red_bot_input_frame, placeholder_text = "Bot...")
red_bot_pick.pack()


red_supp_frame = customtkinter.CTkFrame(master = red_side, fg_color = "#F1B1B1")
red_supp_frame.pack(pady = 8)
red_supp_image = customtkinter.CTkImage(Image.open(resource_path("-1.png")), size = (50,50))
red_supp_icon = customtkinter.CTkLabel(master = red_supp_frame, image = red_supp_image, text = "")
red_supp_icon.pack(side = "left", padx = 20)
red_supp_input_frame = customtkinter.CTkFrame(master = red_supp_frame, fg_color = "#F1B1B1")
red_supp_input_frame.pack(side = "right", padx = 20)
red_supp_label = customtkinter.CTkLabel(master = red_supp_input_frame, text = "Support:", text_color = "black")
red_supp_label.pack()
red_supp_pick = customtkinter.CTkEntry(master = red_supp_input_frame, placeholder_text = "Support...")
red_supp_pick.pack()



red_lock_in = customtkinter.CTkButton(red_side, text = "Lock In", command = set_red_picks, text_color = "white",hover = True,
  hover_color = "#e06a61",
  height = 40,
  width = 120,
  border_width = 2,
  corner_radius = 20,
  border_color = "#9e4a43", 
  fg_color = "#c75d55")
red_lock_in.pack(pady = 5) 


winner_frame = customtkinter.CTkFrame(master = app, fg_color = "gray", width = 665, height = 70)
winner_frame.pack(side = "bottom", expand = "false", pady = 17)
winner_frame.pack_propagate(False)
get_winner = customtkinter.CTkButton(winner_frame, text = "Who Won Draft?", command = winner, text_color = "#363636",hover = True,
    hover_color = "#f2f2f2",
    height = 40,
    width = 120,
    border_width = 2,
    corner_radius = 20,
    border_color = "#d3d3d3", 
    fg_color = "#fafafa")
get_winner.pack(side="right", padx = 20)

results_frame = customtkinter.CTkFrame(master = winner_frame, fg_color = "gray")
results_frame.pack(side = "left", padx = 20)
conf_frame = customtkinter.CTkFrame(master = winner_frame, fg_color = "gray")
conf_frame.pack(side = "left", padx = 20)
winner_label = customtkinter.CTkLabel(master = results_frame, text = "Winning Side: ", text_color = "black", font = ("Arial", 20))
winner_label.pack(side = "left")
confidence_label = customtkinter.CTkLabel(master = conf_frame, text = "Confidence: ", text_color = "black", font = ("Arial", 20))
confidence_label.pack(side = "left", padx = 20)

app.mainloop()