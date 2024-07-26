import random
import os
import keyboard
from time import sleep
from colorama import Fore, Back, Style
import json

# Constants initialization
MAP_HEIGHT = 15
MAP_WIDTH = 30
MAX_RESSOURCES_ON_MAP = 30
GROUND_ICON = f"{"⬛":<2}"
TURNS_BETWEEN_REST = 5

WOODS = {"Wood1" : {"icon": f"{"🪵":<3}",
                "value": 4},
         "Wood2": {"icon": f"{"🌳":<2}",
                "value" : 8}
         }

STONES = {"Stone1": {"icon": f"{"🪨":<3}",
                "value" : 4},
          "Stone2": {"icon": f"{"💎":<2}",
                "value" : 8}
          }

BATS = {"Houses": {
            "House":{
                "id": 1,
                "icon": f"{"⛺":<2}",
                "woodNeeded": 10,
                "stoneNeeded": 0,
                "staminaCost": 15,
                "staminaRestoreRate": 0.2},
            "House2":{
                "id": 6,
                "icon": f"{"🏡":<2}",
                "woodNeeded": 10,
                "stoneNeeded": 10,
                "staminaCost": 20,
                "staminaRestoreRate": 0.5},
            "House3":{
                "id": 7,
                "icon": f"{"🕌":<2}",
                "woodNeeded": 25,
                "stoneNeeded": 25,
                "staminaCost": 35,
                "staminaRestoreRate": 0.75},
        },
        "Woods":{
            "WoodFactory":{
                "id": 2,
                "icon": f"{"🎋":<2}",
                "woodNeeded": 10,
                "stoneNeeded": 5,
                "bonusValue": 0.1,
                "staminaCost": 10},
            "WoodFactory2":{
                "id": 4,
                "icon": f"{"🏟️":<2}",
                "woodNeeded": 25,
                "stoneNeeded": 15,
                "bonusValue": 0.2,
                "staminaCost": 25}
            },
        "Stones": {
            "StoneFactory":{
                "id": 3,
                "icon": f"{"🏔️":<3}",
                "woodNeeded": 5,
                "stoneNeeded": 10,
                "bonusValue": 0.1,
                "staminaCost": 10},
            "StoneFactory2":{
                "id": 5,
                "icon": f"{"🗻":<2}",
                "woodNeeded": 15,
                "stoneNeeded": 25,
                "bonusValue": 0.2,
                "staminaCost": 25}
            }
        }


# Variables initialization
player = {"icon": f"{"🧌":<2}",
         "position": (1, 1),
         "maxStamina": 50,
         "maxHp": 25,
         "hp": 25,
         "stamina": 50,
         "woodBats": 0,
         "stoneBats": 0,
         "houseBats": 0,
         "woodRessources": 0,
         "stoneRessources": 0,
         "maxWoodRessources": 100,
         "maxStoneRessources": 100,
         "woodBonus": 1,
         "stoneBonus": 1,
         "lastRest" : 0
         }

map_infos = {"ressources_on_map": 0}
exit = False
turn = 0
post_print_message = ""

def ask_question_to_player(message):
    c = "x"
    while c != "y" and c != "n" and c != "":
        c = input(message).lower()
        if len(c) != 0:
            c = c[-1]
    return c
def add_map_edges():
    map.insert(0, [Fore.RED + "╔"] + ["═══"] * MAP_WIDTH + ["╗"])
    map.append(["╚"] + ["═══"] * MAP_WIDTH + ["╝"])
    
def fill_map():
    y_list = list(range(len(map)))
    random.shuffle(y_list)
    for y in y_list:
        x_list = list(range(len(map[y])))
        random.shuffle(x_list)
        for x in x_list:
            if map_infos["ressources_on_map"] >= MAX_RESSOURCES_ON_MAP:
                break
            if x != 0 and x != MAP_WIDTH + 1 and y != 0 and y != MAP_HEIGHT + 1:
                if  map[y][x] == GROUND_ICON:
                    rndType = random.randint(0, 32)
                    rnd = random.random()
                    match rndType:
                        case 1: # Wood
                            if(rnd <= 0.66):
                                map[y][x] = WOODS["Wood1"]["icon"]
                            else:
                                map[y][x] = WOODS["Wood2"]["icon"]
                            map_infos["ressources_on_map"] += 1
                        case 2: # Stone
                            if(rnd <= 0.66):
                                map[y][x] = STONES["Stone1"]["icon"]
                            else:
                                map[y][x] = STONES["Stone2"]["icon"] 
                            map_infos["ressources_on_map"] += 1
    
def print_post_print_message():
    global post_print_message
    print(Fore.MAGENTA +post_print_message)  
    post_print_message = ""
    
def print_map():
    os.system('cls')
    print(Fore.YELLOW + "Tour: " + str(turn) + Fore.CYAN)
    print('''
"ZQSD" => Déplacer le personnage     |    "B" => Construire un batiument''')
    for y, v in enumerate(map):
        print()
        for x ,val in enumerate(v):
            print(val, end = "")   
    print()
    print_player_status()
    print_post_print_message()
    
def check_next_player_position(x, y):
    global post_print_message 
    
    if map[y][x] == WOODS["Wood1"]["icon"]: 
        player["woodRessources"] += round(WOODS["Wood1"]["value"] * player["woodBonus"])
        map_infos["ressources_on_map"] -= 1
        post_print_message = str(WOODS["Wood1"]["value"]) + " Wood collected!"
        
    elif map[y][x] == WOODS["Wood2"]["icon"]:
        player["woodRessources"] += round(WOODS["Wood2"]["value"] * player["woodBonus"])
        map_infos["ressources_on_map"] -= 1
        post_print_message = str(WOODS["Wood2"]["value"]) + " Wood collected!"
        
    elif map[y][x] == STONES["Stone1"]["icon"]:
        player["stoneRessources"] += round(STONES["Stone1"]["value"] * player["stoneBonus"])
        map_infos["ressources_on_map"] -= 1
        post_print_message = str(STONES["Stone1"]["value"]) + " Stone collected!"
        
    elif map[y][x] == STONES["Stone2"]["icon"]:
        player["stoneRessources"] += round(STONES["Stone2"]["value"] * player["stoneBonus"])
        map_infos["ressources_on_map"] -= 1
        post_print_message = str(STONES["Stone2"]["value"]) + " Stone collected!"
        
    elif map[y][x] in (BATS["Houses"]["House"]["icon"], BATS["Houses"]["House2"]["icon"], BATS["Houses"]["House3"]["icon"]):
        if player["stamina"] < player["maxStamina"]:
            if player["lastRest"] <= 0:
                if map[y][x] == BATS["Houses"]["House"]["icon"]:
                    player["stamina"] += round(player["maxStamina"] * BATS["Houses"]["House"]["staminaRestoreRate"] + 1)
                elif map[y][x] == BATS["Houses"]["House2"]["icon"]:
                    player["stamina"] += round(player["maxStamina"] * BATS["Houses"]["House2"]["staminaRestoreRate"] + 1)
                elif map[y][x] == BATS["Houses"]["House3"]["icon"]:
                    player["stamina"] += round(player["maxStamina"] * BATS["Houses"]["House3"]["staminaRestoreRate"] + 1)
                    
                if player["stamina"] > player["maxStamina"]:
                    player["stamina"] = player["maxStamina"] + 1
                player["lastRest"] = TURNS_BETWEEN_REST
                if len(post_print_message) == 0:
                    post_print_message = "Stamina restored!"
                else:
                    post_print_message += "\nStamina restored!"
            else:
                post_print_message = f"Vous vous êtes déja reposé dans les {TURNS_BETWEEN_REST} derniers tours"   
                
    if player["woodRessources"] > player["maxWoodRessources"]:
        player["woodRessources"] = player["maxWoodRessources"]
        
    if player["stoneRessources"] > player["maxStoneRessources"]:
        player["stoneRessources"] = player["maxStoneRessources"]
        
    else:
        print("Nothing here!")
        
def print_player_status():
    print(f'''{Fore.YELLOW}Hp:      {str('{:02d}'.format(player["hp"]))}/{str('{:02d}'.format(player["maxHp"]))}            |   Bois:   {str('{:02d}'.format(player["woodRessources"]))}/{str('{:02d}'.format(player["maxWoodRessources"]))}
Stamina: {str('{:02d}'.format(player["stamina"]))}/{str('{:02d}'.format(player["maxStamina"]))}            |   Pierre: {str('{:02d}'.format(player["stoneRessources"]))}/{str('{:02d}'.format(player["maxStoneRessources"]))}
''')
    
def move_player(x, y, init=False):
    global post_print_message 
    if 0 < x < MAP_WIDTH + 1 and 0 < y < MAP_HEIGHT + 1: 
        if map[player["position"][1]][player["position"][0]] == player["icon"]:
            map[player["position"][1]][player["position"][0]] = GROUND_ICON
            
        check_next_player_position(x, y)
        player["position"] = (x, y)
        if not init:
            player["stamina"] -= 1
            
            if player["stamina"] == 0:
                post_print_message = "Vous êtes à bout de force. Vous ne pouvez plus vous déplacer sans subir de dégats. (-1 HP/déplacement)"
            elif player["stamina"] < 0:
                post_print_message = "Vous êtes à bout de force. Vous ne pouvez plus vous déplacer sans subir de dégats. (-1 HP/déplacement)"
                player["hp"] -= 1
                player["stamina"] = 0
        
        if not(map[y][x] in (BATS["Woods"]["WoodFactory"]["icon"], BATS["Stones"]["StoneFactory"]["icon"], BATS["Houses"]["House"]["icon"], BATS["Woods"]["WoodFactory2"]["icon"], BATS["Stones"]["StoneFactory2"]["icon"], BATS["Houses"]["House2"]["icon"], BATS["Houses"]["House3"]["icon"])):
            map[player["position"][1]][player["position"][0]] = player["icon"]
 
    else:
       post_print_message = "Vous ne pouvez pas vous déplacer hors de la carte!"
        
def print_construction_menu():
    if map[player["position"][1]][player["position"][0]] not in (BATS["Woods"]["WoodFactory"]["icon"], BATS["Stones"]["StoneFactory"]["icon"], BATS["Houses"]["House"]["icon"], BATS["Woods"]["WoodFactory2"]["icon"], BATS["Stones"]["StoneFactory2"]["icon"], BATS["Houses"]["House2"]["icon"], BATS["Houses"]["House3"]["icon"]):
        isdigit = False
        while not isdigit:
            print(f'''
        Quel type de batiment souhaitez-vous construire?: 
                0. Annuler la construction
                {BATS["Houses"]["House"]["id"]}. House        ({BATS["Houses"]["House"]["woodNeeded"]} Bois, {BATS["Houses"]["House"]["stoneNeeded"]} Pierre, {BATS["Houses"]["House"]["staminaCost"]} Stamina) => Récupération de stamina
                {BATS["Woods"]["WoodFactory"]["id"]}. WoodFactory  ({BATS["Woods"]["WoodFactory"]["woodNeeded"]} Bois, {BATS["Woods"]["WoodFactory"]["stoneNeeded"]} Pierre, {BATS["Woods"]["WoodFactory"]["staminaCost"]} Stamina)  => Génératrion de bois tous les 5 tours
                {BATS["Stones"]["StoneFactory"]["id"]}. StoneFactory ({BATS["Stones"]["StoneFactory"]["woodNeeded"]} Bois, {BATS["Stones"]["StoneFactory"]["stoneNeeded"]} Pierre, {BATS["Stones"]["StoneFactory"]["staminaCost"]} Staminab) => Génératrion de pierre tous les 5 tours
                ''')
            try:
                choix = input("==> ")
                if len(choix) != 0:
                    choix = choix[-1]
                choix = int(choix)
                if choix in (0, BATS["Woods"]["WoodFactory"]["id"], BATS["Stones"]["StoneFactory"]["id"], BATS["Houses"]["House"]["id"]):
                    isdigit = True
            except ValueError:
                print("Veuillez entrer une valeur numérique!")      
        if choix != 0:                       
            build_check_construction(choix)
        else:
            global post_print_message 
            post_print_message = "Construction annulée!"
    else:
        print("Un bâtiment est déja présent.")
        build_check_upgrade()

def build_check_upgrade():
    if map[player["position"][1]][player["position"][0]] == BATS["Woods"]["WoodFactory"]["icon"]:
        c = ask_question_to_player(f"Voulez-vous l'améliorer? ({BATS["Woods"]["WoodFactory2"]["woodNeeded"]} Bois, {BATS["Woods"]["WoodFactory2"]["stoneNeeded"]} Pierre, {BATS["Woods"]["WoodFactory2"]["staminaCost"]} Stamina) (y/N)")
        if c == "y":
            build_construction(BATS["Woods"]["WoodFactory2"])
            
    elif map[player["position"][1]][player["position"][0]] == BATS["Stones"]["StoneFactory"]["icon"]:
        c = ask_question_to_player(f"Voulez-vous l'améliorer? ({BATS["Stones"]["StoneFactory2"]["woodNeeded"]} Bois, {BATS["Stones"]["StoneFactory2"]["stoneNeeded"]} Pierre, {BATS["Stones"]["StoneFactory2"]["staminaCost"]} Stamina) (y/N)")
        if c == "y":
            build_construction(BATS["Stones"]["StoneFactory2"])
    elif map[player["position"][1]][player["position"][0]] == BATS["Houses"]["House"]["icon"]:
        c = ask_question_to_player(f"Voulez-vous l'améliorer? ({BATS["Houses"]["House2"]["woodNeeded"]} Bois, {BATS["Houses"]["House2"]["stoneNeeded"]} Pierre, {BATS["Houses"]["House2"]["staminaCost"]} Stamina) (y/N)")
        if c == "y":
            build_construction(BATS["Houses"]["House2"])
    elif map[player["position"][1]][player["position"][0]] == BATS["Houses"]["House2"]["icon"]:
        c = ask_question_to_player(f"Voulez-vous l'améliorer? ({BATS["Houses"]["House3"]["woodNeeded"]} Bois, {BATS["Houses"]["House3"]["stoneNeeded"]} Pierre, {BATS["Houses"]["House3"]["staminaCost"]} Stamina) (y/N)")
        if c == "y":
            build_construction(BATS["Houses"]["House3"])
    else:
        global post_print_message 
        post_print_message = "Ce batiment à déja attint son niveau maximum!"
        
def build_check_construction(typeConstruction):
    if typeConstruction == BATS["Woods"]["WoodFactory"]["id"]:
        build_construction(BATS["Woods"]["WoodFactory"])
    elif typeConstruction == BATS["Stones"]["StoneFactory"]["id"]:
        build_construction(BATS["Stones"]["StoneFactory"])
    elif typeConstruction == BATS["Houses"]["House"]["id"]:
        build_construction(BATS["Houses"]["House"])
        
def build_construction(typeConstruction):
    global post_print_message 
    if player["woodRessources"] >= typeConstruction["woodNeeded"] and player["stoneRessources"] >= typeConstruction["stoneNeeded"]:
        stamAfterConstruct = player["stamina"] - typeConstruction["staminaCost"]
        if stamAfterConstruct >= 0:
            player["woodRessources"] -= typeConstruction["woodNeeded"]
            player["stoneRessources"] -= typeConstruction["stoneNeeded"]
            player["stamina"] -= typeConstruction["staminaCost"]
            map[player["position"][1]][player["position"][0]] = typeConstruction["icon"]
            
            if typeConstruction in (BATS["Woods"]["WoodFactory"], BATS["Woods"]["WoodFactory2"]):
                player["woodBats"] += 1
            elif typeConstruction in (BATS["Stones"]["StoneFactory"], BATS["Stones"]["StoneFactory2"]):
                player["stoneBats"] += 1
            elif typeConstruction in (BATS["Houses"]["House"], BATS["Houses"]["House2"], BATS["Houses"]["House3"]):
                player["houseBats"] += 1
            
            post_print_message = "Construction effectuée!"
        else:
            if player["hp"] + stamAfterConstruct > 0:
                print(f"Vous n'avez pas assez de stamina! Celà vous coutera {stamAfterConstruct} hp pour le construire quand même!")
                
                c = ask_question_to_player("Voulez-vous le construire maintenant? (y/N)")        
                if c == "y":
                    player["hp"] += stamAfterConstruct
                    player["woodRessources"] -= typeConstruction["woodNeeded"]
                    player["stoneRessources"] -= typeConstruction["stoneNeeded"]
                    player["stamina"] = 0
                    map[player["position"][1]][player["position"][0]] = typeConstruction["icon"]
                    
                    player["woodBats"] += 1
                    
                    post_print_message = "Construction effectuée!"
                elif c == "n" or c == "":
                    post_print_message = "Construction annulée!"
                    
            else:
                post_print_message = "Vous êtes trop épuisé pour construire ce bâtiment!"
    else:
        post_print_message = "Vous n'avez pas assez de ressources!"

    check_next_player_position(player["position"][0], player["position"][1])
    
def save_game(player, map, map_infos, turn):
    save = {
        "player": player,
        "map": map,
        "map_infos": map_infos,
        "turn": turn
    }
    with open('savegame.json', 'w') as jsonFile:
        json.dump(save, jsonFile)
        print("Partie sauvegardée!")

def load_game():
    with open('savegame.json', 'r') as jsonFile:
        save = json.load(jsonFile)
        player = save["player"]
        map = save["map"]
        map_infos = save["map_infos"]
        turn = save["turn"]
    return player, map, map_infos, turn

# row = ["║"] + [' . '] * MAP_WIDTH + ["║"]
# map = [row] * MAP_HEIGHT => error: row multiplicated with always same Reference: 

# Check for saved game
if os.path.exists('savegame.json'):
    c = ask_question_to_player(Fore.YELLOW +"Voulez-vous charger une partie? (Y/n)")        
    if c == "y" or c == "":
        player, map, map_infos, turn = load_game()
    else:
        # Initialise map
        map = [["║"] + [GROUND_ICON] * MAP_WIDTH + ["║"] for _ in range(MAP_HEIGHT)]
        add_map_edges()
        move_player(player["position"][0], player["position"][1], True)
        fill_map()
else: 
    # Initialise map
    map = [["║"] + [GROUND_ICON] * MAP_WIDTH + ["║"] for _ in range(MAP_HEIGHT)]
    add_map_edges()
    move_player(player["position"][0], player["position"][1], True)
    fill_map()
    
print_map()

# Start game

while not exit:
    turn += 1
    player["lastRest"] -= 1
    # refill map every 30 turns
    if turn % 30 == 0:
        fill_map()
    
    # get ressources from bats every 10 turns
    if turn % 10 == 0:
        player["woodRessources"] += player["woodBats"] * 5
        player["stoneRessources"] += player["stoneBats"] * 5
        
    if player["hp"] > 0:
        
        key_pressed = keyboard.read_key().lower()
        if key_pressed == "esc":
            c = ask_question_to_player(Fore.YELLOW + "Voulez-vous sauvegarder la partie? (Y/n)")
                    
            if c == "y" or c == "":
                save_game(player, map, map_infos, turn)
                
            print(Fore.RED + "\nBye bye!" + Style.RESET_ALL)
            exit = True
                
        elif key_pressed == "q":
            move_player(player["position"][0] - 1, player["position"][1])
            print_map()
        elif key_pressed == "d":
            move_player(player["position"][0] + 1, player["position"][1])
            print_map()
        elif key_pressed == "z":
            move_player(player["position"][0], player["position"][1] - 1)
            print_map()
        elif key_pressed == "s":
            move_player(player["position"][0], player["position"][1] + 1)
            print_map()
        elif key_pressed == "b":
            print_construction_menu()
            print_map()
        else:
            turn -= 1
      
        sleep(0.25)
    else:
        print(Fore.RED + "\nVOUS ÊTES MORT!")
        exit = True
    