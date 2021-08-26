import json

with open("../raw/expansions.json", "r") as f:
    expansions = json.load(f)
with open("../raw/cards-light.json", "r") as f:
    src_cards = json.load(f)["cards"]
with open("../raw/cards-dark.json", "r") as f:
    src_cards = src_cards + json.load(f)["cards"]

card_facts = []

for card in src_cards:
    title = card["front"]["title"].replace('•', '').replace('<>', '')
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

    card_facts.append({
        "text": f'{title} is a {side} Side card from expansion set {set_name}.',
        "metadata": title
    })
    card_facts.append({
        "text": f'{title} is rarity {rarity}.',
        "metadata": title
    })
    card_facts.append({
        "text": f'{title} is a {side} Side {full_type} card.',
        "metadata": title
    })
    card_facts.append({
        "text": f'{title} is a {full_type}.',
        "metadata": title
    })
    if uniqueness:
        card_facts.append({
            "text": f'{title} has uniqueness symbol {uniqueness}.',
            "metadata": title
        })
    if lore and lore != "Blank.":
        card_facts.append({
            "text": f'The lore for {title} is "{lore}".',
            "metadata": title
        })
    card_facts.append({
        "text": f'{title} has gametext that says "{gametext}".',
        "metadata": title
    })
    for attribute_string in attributes_strings:
        card_facts.append({
            "text": f'{title} has {attribute_string}.',
            "metadata": title
        })
    for icon in icons:
        card_facts.append({
            "text": f'{title} has the icon {icon}.',
            "metadata": title
        })
        card_facts.append({
            "text": f'{title} is a {icon} {type}.',
            "metadata": title
        })
    for characteristic in characteristics:
        card_facts.append({
            "text": f'{title} is a {characteristic}.',
            "metadata": title
        })
        card_facts.append({
            "text": f'{title} has the characteristic {characteristic}.',
            "metadata": title
        })

    if uniqueness == "*":
        card_facts.append({"text": f'{title} is unique.', "metadata": title})
    if uniqueness == None:
        card_facts.append({"text": f'{title} is non-unique.', "metadata": title})
    if two_sided:
        card_facts.append({"text": f'{title} is a two-sided card.', "metadata": title})

f = open("../data/cards.jsonl", "w")
f.writelines('\n'.join(map(json.dumps, card_facts)))
f.close()