import json
import os
from re import search
dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, "../raw/expansions.json"), "r") as f:
    expansions = json.load(f)
with open(os.path.join(dirname, "../raw/cards-light.json"), "r") as f:
    src_cards = json.load(f)["cards"]
with open(os.path.join(dirname, "../raw/cards-dark.json"), "r") as f:
    src_cards = src_cards + json.load(f)["cards"]

answers_training_data = []
search_training_data = []
fine_tune_training_data = []

for card in src_cards:
    card_facts = []

    title = card["front"]["title"].replace('•', '').replace('<>', '')
    if title.endswith(" (AI)"):
        card_facts.append({"text": f'{title.replace(" (AI)", "")} has an alternate image.', "metadata": title})
        continue
    side = card["side"]
    rarity = card["rarity"]
    set_number = card["set"]
    type = card["front"]["type"]
    sub_type = card["front"].get("subType")
    uniqueness = card["front"].get("uniqueness")
    lore = card["front"].get("lore")
    gametext = card["front"].get("gametext")
    icons = card["front"].get("icons", [])
    characteristics = card["front"].get("characteristics", [])
    
    attributes = {}
    attributes["destiny"] = card["front"].get("destiny")
    attributes["power"] = card["front"].get("power")
    attributes["ability"] = card["front"].get("ability")
    attributes["maneuver"] = card["front"].get("manuever")
    attributes["armor"] = card["front"].get("armor")
    attributes["hyperspeed"] = card["front"].get("hyperspeed")
    attributes["landspeed"] = card["front"].get("landspeed")
    attributes["deploy"] = card["front"].get("deploy")
    attributes["forfeit"] = card["front"].get("forfeit")
    attributes["extra_text"] = card["front"].get("extra_text")

    two_sided = False
    if card.get("back"):
        two_sided = True
        gametext = f'FRONT:\n{gametext}\nBACK:\n{card["back"]["gametext"]}'
        if attributes.get("destiny") and card["back"].get("destiny"):
            attributes["destiny"] = f'{attributes["destiny"]} / {card["back"]["destiny"]}'

    set_name = expansions[set_number]
    full_type = f'{type} - {sub_type}' if sub_type else type
    non_null_attributes = attributes
    attributes_strings = [f'{k.lower()} {v}' for k, v in attributes.items() if v]

    card_facts.append(f'{title} is a {side} Side card from expansion set {set_name}.')
    card_facts.append(f'{title} is rarity {rarity}.')
    card_facts.append(f'{title} is a {type}.')
    card_facts.append(f'{title} is a {full_type}.')
    if uniqueness:
        card_facts.append(f'{title} has uniqueness symbol {uniqueness}.')
    if lore and lore != "Blank.":
        card_facts.append(f'{title} has lore of "{lore}".')
    card_facts.append(f'{title} has gametext "{gametext}".')
    for attribute_string in attributes_strings:
        card_facts.append(f'{title} is {attribute_string}.')
    for icon in icons:
        card_facts.append(f'{title} has the {icon} icon.')
        card_facts.append(f'{title} is a {icon} {type}.')
    for characteristic in characteristics:
        card_facts.append(f'{title} is a {characteristic}.')
        card_facts.append(f'{title} has the characteristic {characteristic}.')

    if uniqueness == "*":
        card_facts.append(f'{title} is a unique {type}.')
    if uniqueness == None:
        card_facts.append(f'{title} is a non-unique {type}.')
    if two_sided:
        card_facts.append(f'{title} is a two-sided card.')
    
    # Each datum is a single sentence about the card.
    search_training_data.append({"text": "\n".join(card_facts), "metadata": title})

    # Each datum is a single statement about the card.
    for card_fact in card_facts:
        answers_training_data.append({"text": card_fact, "metadata": title})
        fine_tune_training_data.append({"prompt": f'{title} ->', "completion": card_fact.replace(title, "")})

output_file = os.path.join(dirname, '../data/answers.jsonl')
f = open(output_file, "w")
f.writelines('\n'.join(map(json.dumps, answers_training_data)))
f.close()

output_file = os.path.join(dirname, '../data/search.jsonl')
f = open(output_file, "w")
f.writelines('\n'.join(map(json.dumps, search_training_data)))
f.close()

output_file = os.path.join(dirname, '../data/fine_tune.jsonl')
f = open(output_file, "w")
f.writelines('\n'.join(map(json.dumps, fine_tune_training_data)))
f.close()

# TODO: For fine-tune, try organizing data as completions, eg: Prompt: Darth Vader's power is. Answer: 6.
