from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd

options = Options()
options.binary_location = "/usr/lib/firefox/firefox"
driver = webdriver.Firefox(options=options, executable_path="webdriver/geckodriver")

questions = []

for page in range(1, 74):
    driver.get(f'https://****/{page}/')
    topics = driver.find_elements_by_class_name('discussion-link')
    for topic in topics:
        if 'Machine Learning Engineer' in topic.text:
            print(topic.text)
            questions.append([topic.text, topic.get_attribute('href')])


pd.DataFrame(questions, columns=['title', 'link']).to_csv('questions.csv', index=False)
