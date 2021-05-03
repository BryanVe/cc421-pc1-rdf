import json

from scrapper.character_details import get_character_details

BASE_URL = 'https://onepiece.fandom.com/wiki/'

characters = [
    "Monkey D. Luffy",
    "Roronoa Zoro",
    "Nami",
    "Usopp",
    "Sanji",
    "Tony Tony Chopper",
    "Nico Robin",
    "Franky",
    "Brook",
    "Jinbe",
    "Nefertari Vivi",
    "Kaido",
    "King",
    "Jack",
    "X Drake",
    "Basil Hawkins",
    "Yamato",
    "Scratchmen Apoo",
    "Donquixote Doflamingo",
    "Trebol",
    "Diamante",
    "Pica ",
    "Charlotte Katakuri",
    "Vergo",
    "Donquixote Rosinante",
    "Bellamy",
    "Marshall D. Teach",
    "Trafalgar D. Water Law",
    "Eustass Kid",
    "Killer",
    "Capone Bege",
    "Jewelry Bonney",
    "Urouge",
    "Dracule Mihawk",
    "Marco",
    "Bartholomew Kuma",
    "Emporio Ivankov",
    "Boa Hancock",
    "Raizo",
    "Kanjuro ",
    "Arlong",
    "Crocodile",
    "Sakazuki",
    "Kozuki Toki",
    "Kizaru ",
    "Fujitora",
    "Ashura Doji",
    "Sabo",
    "Monkey D. Dragon",
    "Kinemon",
    "Bepo",
    "Momonosuke",
    "Portgas D. Ace",
    "Monkey D. Garp",
    "Koby",
    "Tashigi",
    "Sengoku",
    "Lucky Roux",
    "Edward Newgate",
    "Marco ",
    "Sentomaru",
    "Aokiji ",
    "Gol D. Roger",
    "Silvers Rayleigh",
    "Crocus",
    "Buggy",
    "Galdino",
    "Shanks",
    "Bentham",
    "Nekomamushi",
    "Inuarashi",
    "Kozuki Oden"
]

characters = [character.replace(" ", "_") for character in characters]
c = []

count = 0

for character in characters:
    c.append(get_character_details(BASE_URL + character))

print(json.dumps(c, indent=4))
