from bs4 import BeautifulSoup
import requests
import re
from more_itertools import chunked

r = requests.get("http://oldschoolrunescape.wikia.com/wiki/Treasure_Trails/Guide/Anagrams")

soup = BeautifulSoup(r.text, "lxml")

data = []
unique_data = []

splitted_list = []

tables = soup.findAll(attrs = {"class" : "wikitable"})

text_array = []
strings = []
file_strings = []
unique_strings = []

for table in tables:
    text = table.get_text()
    text = re.sub("\([^()]*\)", '', text)
    text_array.append(text)

for table in text_array:
    splitted_table = table.split("\n")
    for item in splitted_table:
        if(item != '' and item[:4] != 'Note'):
            splitted_list.append(item)


chunked_list = chunked(splitted_list, 5)
header = next(chunked_list)

for item in chunked_list:
    item_dict = dict(zip(header, item))
    data.append(item_dict)
for x in range(len(data)):
    if(data[x]["Anagram"] == "Anagram"):
        continue
    # fp.write()

    string = ("\"This anagram reveals who to speak to next: " + data[x]["Anagram"] + '"').lower()
    strings.append(string)

with open("comp", "r") as fp:
    file_strings = fp.readlines()

anagrams = []
for s in file_strings:
    s = s.split(',')[0].lower()
    anagrams.append(s)

for s in strings:
    if s.lower() not in anagrams:
        unique_strings.append(s.lower()[44:].replace('"', ''))

for s in unique_strings:
    print(s + "\n")


clue_number = 540

with open("unique", "w") as fp:
    for d in data:
        if(d["Anagram"].lower() in unique_strings):
            print("found: " + d["Anagram"])
            string_to_write = "CLUE" + str(clue_number) + "(\"This anagram reveals who to speak to next: " + d["Anagram"].capitalize() + "\", \"" + d["Solution"] + "\", \"" + d["Location"] + "\", \"" + d["Challenge answer"] + "\", ANAGRAM),\n"

            fp.write(string_to_write)
            clue_number+=1




