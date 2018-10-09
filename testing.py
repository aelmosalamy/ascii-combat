import ac_dicts
import combat

ms = []
for i in range(5):
    m = ac_dicts.give_monster('wolf')
    ms.append(m)

for i in ms:
    print(i.name)    