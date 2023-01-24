from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
import pickle

options = Options()
options.binary_location = "/usr/lib/firefox/firefox"
driver = webdriver.Firefox(options=options, executable_path="webdriver/geckodriver")

target_postcode = []
url = 'https://***'
batch_name = '***'
session_dict = {
    'Housing Types': 'housing_types',
    'Housing Tenure': 'housing_tenure',
    'Housing Occupancy': 'housing_occupancy',
    'Social Grade': 'social_grade',
    'Age Groups': 'age_group',
    'Relationship Status': 'relationship_status',
    'Health': 'health',
    'Education & Qualifications': 'education',
    'Ethnic Group': 'ethnic_group',
    'Country of Birth': 'country_of_birth',
    'Passport(s) Held': 'passports',
    'Religion': 'religion',
    'Economic Activity': 'economic_activity',
    'Employment Industry': 'employment_industry',
    'Broadband in': 'broadband_speed',
}


def get_session_table(session):
    session_table = {}
    for tr in session.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'):
        tds = tr.find_elements_by_tag_name('td')
        session_table[tds[0].text] = tds[1].text
    return session_table

# street_dicts = []
with open(f'street_dicts_{batch_name}.pkl', 'rb') as f:
    street_dicts = pickle.load(f)
k = 0

driver.get(url)
districts = driver.find_element_by_xpath('/html/body/section/div/div[5]').find_elements_by_tag_name('a')
districts = [i.get_attribute('href') for i in districts]

for district in tqdm(districts):
    if district.split('/')[-1] not in target_postcode:
        continue
    driver.get(district)
    
    streets = driver.find_element_by_xpath('/html/body/section/div/div[6]').find_elements_by_tag_name('a')
    street_names = [i.text for i in streets]
    streets = [i.get_attribute('href') for i in streets]
    for street, street_name in zip(streets, street_names):
        if street_name in [i['street_name'] for i in street_dicts]:
            continue
        street_dict = {}
        street_dict['street_url'] = street
        street_dict['street_name'] = street_name
        driver.get(street_dict['street_url'])

        # street_dict = {'street_url': 'https://***',
        #                'street_name': '***'}
        buttons = driver.find_element_by_id('postcodeTabs').find_elements_by_tag_name('a')
        for button in buttons:
            # Get housing information
            if button.get_attribute('href') == street_dict['street_url'] + '#housing' or \
                    button.get_attribute('href') == street_dict['street_url'] + '#people' or \
                    button.get_attribute('href') == street_dict['street_url'] + '#culture' or \
                    button.get_attribute('href') == street_dict['street_url'] + '#employment' or \
                    button.get_attribute('href') == street_dict['street_url'] + '#services':
                button.click()

                sessions = driver.find_elements_by_class_name('info-piece')
                for session in sessions:
                    try:
                        session_title = session.find_element_by_tag_name('h3').text
                    except NoSuchElementException:
                        session_title = ''

                    for _title, _key in session_dict.items():
                        if _title in session_title:
                            street_dict[_key] = get_session_table(session)
                            break

        street_dicts.append(street_dict)
        k += 1
        if k % 15 == 0:
            with open(f'street_dicts_{batch_name}.pkl', 'wb') as f:
                pickle.dump(street_dicts, f)
