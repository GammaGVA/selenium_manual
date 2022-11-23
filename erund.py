import json
stroka = 'АССОЦИАЦИЯ ПРОИЗВОДИТЕЛЕЙ МОЛОКА "ВОЛОГОДСКОЕ МОЛОКО":160022 ВОЛОГОДСКАЯ ОБЛАСТЬ, ГОРОД ВОЛОГДА, УЛИЦА ЯРОСЛАВСКАЯ 9 , ОГРН: 1123500000030, Дата присвоения ОГРН: 20.01.2012, ИНН: 3525269455, КПП: 352501001, председатель Ассоциации: Зинин Владимир Леонидович, Дата прекращения деятельности: 19.09.2017'
lst = stroka.split(',')
nme_org = lst[0].split(':')[0]
adress = [lst[0].split(':')[1]]
Dct = {nme_org: {}}
for i in lst[1:]:
    if ':' in i:
        Dct[nme_org][i.split(':')[0].strip()] = i.split(':')[1].strip()
    else:
        adress += [i]
Dct[nme_org]['Адрес'] = ' '.join(adress).replace('  ', ' ').strip()
print(Dct)
with open(f'{nme_org}_ликвид.json', 'a', encoding='utf-8') as file:
    json.dump(Dct, file,indent=4, ensure_ascii=False)
# with open(f'{name_orgs}.text', 'a', encoding='utf-8') as file:
#     for org in all_page:
#         if 'Дата прекращения деятельности' not in org.find("div", class_="res-text").text:
#             file.write(
#                 f'{org.find("a", class_="op-excerpt").text}:{org.find("div", class_="res-text").text}\n{"_" * 100}\n')
#         else:
#             with open(f"ликвид_{name_orgs}.text", "a", encoding="utf-8") as F:
#                 F.write(
#                     f'{org.find("a", class_="op-excerpt").text}:{org.find("div", class_="res-text").text}\n{"_" * 100}\n')
