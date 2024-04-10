import json
import random

words_counter = {}
with open('data/version_v2/new_profession.json', 'r', encoding='utf-8') as json_file:
    words = json.load(json_file)

for i, j in words.items():
    if j in words_counter:
        words_counter[j].append(i)
    else:
        words_counter[j] = [i]

for i, j in words_counter.items():
    print(f'{i}: {len(j)}')

new_worker = []
counter = 0
while True:
    if counter == 200:
        break

    new = random.choice(words_counter["Рабочий"])
    if new not in new_worker:
        new_worker.append(new)
        counter += 1

words_counter["Рабочий"] = new_worker

for i, j in words_counter.items():
    print(f'{i}: {len(j)}')

expanded = {}
for i, j in words_counter.items():
    for az in j:
        expanded[az] = i

print(expanded)

with open('data/version_v3/new_profession_v2.json', 'w', encoding='utf-8') as f:
    json.dump(expanded, f, ensure_ascii=False, indent=4)
