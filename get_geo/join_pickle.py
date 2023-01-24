from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
import pickle


with open(f'street_dicts_all.pkl', 'rb') as f:
    all_data = pickle.load(f)


all_names = [i['street_name'] for i in all_data]

with open(f'street_dicts_t37.pkl', 'rb') as f:
    temp = pickle.load(f)
for item in temp:
    if item['street_name'] not in all_names:
        all_data.append(item.copy())
del temp
print(len(all_names))



all_names = [i['street_name'] for i in all_data]

with open(f'street_dicts_t65.pkl', 'rb') as f:
    temp = pickle.load(f)
for item in temp:
    if item['street_name'] not in all_names:
        all_data.append(item.copy())
del temp
print(len(all_names))



all_names = [i['street_name'] for i in all_data]

with open(f'street_dicts_t70.pkl', 'rb') as f:
    temp = pickle.load(f)
for item in temp:
    if item['street_name'] not in all_names:
        all_data.append(item.copy())
del temp
print(len(all_names))



all_names = [i['street_name'] for i in all_data]

with open(f'street_dicts_t91.pkl', 'rb') as f:
    temp = pickle.load(f)
for item in temp:
    if item['street_name'] not in all_names:
        all_data.append(item.copy())
del temp
print(len(all_names))



all_names = [i['street_name'] for i in all_data]

with open(f'street_dicts_ty3.pkl', 'rb') as f:
    temp = pickle.load(f)
for item in temp:
    if item['street_name'] not in all_names:
        all_data.append(item.copy())
del temp
print(len(all_names))


with open(f'street_dicts_all.pkl', 'wb') as f:
    pickle.dump(all_data, f)
