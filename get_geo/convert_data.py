from tqdm import tqdm
import pickle
import pandas as pd



with open(f'street_dicts_all.pkl', 'rb') as f:
    street_dicts = pickle.load(f)


excels = []

for idx, row in enumerate(street_dicts):
    excel = {}
    for sidx, srow in row.items():
        if sidx in ('street_url', 'street_name'):
            excel[sidx] = srow
        else:
            is_number = list(srow.values())[0].isnumeric()
            if is_number:
                excel['{}:{}'.format(sidx, 'total')] = sum([float(i) for i in srow.values() if is_number])

            for midx, mrow in srow.items():
                if is_number:
                    excel['{}:{}'.format(sidx, midx)] = int(float(mrow)*100/excel['{}:{}'.format(sidx, 'total')])
                else:
                    excel['{}:{}'.format(sidx, midx)] = mrow
    excels.append(excel)

excels_ = pd.DataFrame(excels)

excels_['ex_1'] = excels_['housing_tenure:Rented: From Council']/excels_['housing_tenure:total']
excels_['ex_2'] = (excels_['ethnic_group:Bangladeshi'] + excels_['ethnic_group:Black African'] + excels_['ethnic_group:Black Caribbean'] + excels_['ethnic_group:Indian'] + excels_['ethnic_group:Other Black/African/Caribbean'] + excels_['ethnic_group:Pakistani'])/excels_['ethnic_group:total']
excels_['ex_3'] = excels_['religion:Muslim']/excels_['religion:total']
excels_['ex_4'] = excels_['economic_activity:Unemployed']/excels_['economic_activity:total']
excels_['ex_5'] = (excels_['housing_types:Detached'] + excels_['housing_types:Semi-Detached'] + excels_['housing_types:Terraced'])/excels_['housing_types:total']
excels_['ex_6'] = excels_['ethnic_group:White']/excels_['ethnic_group:total']



excels_ = excels_[
       (excels_['ex_1'] < 0.25) &
       (excels_['ex_2'] < 0.3) &
       (excels_['ex_3'] < 0.3) &
       (excels_['ex_4'] < 0.3) &
       (excels_['ex_5'] > 0.7) &
       (excels_['ex_6'] < 0.7)
      ].reset_index()

print(len(excels_))

target_columns = [
'street_name','street_url','social_grade:AB - Higher and intermediate managerial, administrative, or professional positions','social_grade:C1 - Supervisory, clerical, and junior managerial/administrative/professional positions','social_grade:C2 - Skilled manual workers','social_grade:DE - Semi-skilled and unskilled manual workers; those on state benefit/unemployed, & lowest grade workers','social_grade:total','country_of_birth:European Union','country_of_birth:Other','country_of_birth:total','economic_activity:Long-Term Sick or Disabled','economic_activity:Other','economic_activity:Unemployed','economic_activity:total','ex_4','ethnic_group:total','ethnic_group:Chinese','ex_2','housing_tenure:Rented: From Council','housing_tenure:Rented: Other Social\ninc. charities and housing associations','housing_tenure:total','ex_1','religion:Muslim','religion:total','ex_3'
]

size = 1999

i = 0
while True:
    _ = excels_.loc[i*size:(i+1)*size, target_columns]
    if _.size == 0:
        break
    _.to_csv(f'streetcheck_{i}.csv', index=False)
    i += 1

















"""


age_group:0-4
age_group:10-14
age_group:15
age_group:16-17
age_group:18-19
age_group:20-24
age_group:25-29
age_group:30-44
age_group:45-59
age_group:5-7
age_group:60-64
age_group:65-74
age_group:75-84
age_group:8-9
age_group:85-89
age_group:90+
age_group:total
broadband_speed:Average Download Speed
broadband_speed:Average Upload Speed
broadband_speed:Gigabit (1,000Mbps+) Internet Available
broadband_speed:Maximum Download Speed Reported
broadband_speed:Maximum Upload Speed Reported
broadband_speed:Superfast Broadband Available
broadband_speed:Ultrafast (300Mbps+) Broadband Available
country_of_birth:England
country_of_birth:European Union
country_of_birth:Northern Ireland
country_of_birth:Other
country_of_birth:Republic of Ireland
country_of_birth:Scotland
country_of_birth:Wales
country_of_birth:total
economic_activity:Full-Time Employee
economic_activity:Full-Time Student
(with or without job)
economic_activity:Long-Term Sick or Disabled
economic_activity:Looking After Home or Family
economic_activity:Other
economic_activity:Part-Time Employee
(defined as 30 hours or less per week)
economic_activity:Retired
economic_activity:Self Employed
economic_activity:Unemployed
economic_activity:total
education:1-4 GCSEs or Equivalent
education:5+ GCSEs, an A-Level or 1-2 AS Levels
education:Apprenticeship
education:Degree or Similar
e.g. professional qualification (accountancy etc)
education:HNC, HND or 2+ A Levels
education:No GCSEs or Equivalent
education:Other
education:total
employment_industry:Accommodation and Food
employment_industry:Administration
employment_industry:Agriculture
Inc. Forestry and Fishing
employment_industry:Construction
employment_industry:Education
employment_industry:Energy Supply
Inc. Electric, Gas, Steam, Air Conditioning etc.
employment_industry:Financial Services
Inc. Insurance
employment_industry:Health
Inc. Social Work
employment_industry:Information and Communication
employment_industry:Manufacturing
employment_industry:Mining/Quarrying
employment_industry:Other
Inc. Arts, Recreation etc.
employment_industry:Professional, Scientific and Technical
employment_industry:Public Administration and Defence
employment_industry:Real Estate
employment_industry:Retail
Inc. Wholesale
employment_industry:Transportation
Inc. Storage and Logistics
employment_industry:Water Supply
Inc. Sewage and Waste Management
employment_industry:total
ethnic_group:Bangladeshi
ethnic_group:Black African
ethnic_group:Black Caribbean
ethnic_group:Chinese
ethnic_group:Indian
ethnic_group:Mixed Ethnicity
ethnic_group:Other
ethnic_group:Other Asian
ethnic_group:Other Black/African/Caribbean
ethnic_group:Pakistani
ethnic_group:White
ethnic_group:total
ex_1
ex_2
ex_3
ex_4
health:Bad
health:Fair
health:Good
health:Very Bad
health:Very Good
health:total
housing_occupancy:8+ People
housing_occupancy:Five People
housing_occupancy:Four People
housing_occupancy:One Person
housing_occupancy:Seven People
housing_occupancy:Six People
housing_occupancy:Three People
housing_occupancy:Two People
housing_occupancy:total
housing_tenure:Owned Outright
housing_tenure:Owned with Mortgage
housing_tenure:Rent Free
housing_tenure:Rented: From Council
housing_tenure:Rented: Other
housing_tenure:Rented: Other Social
inc. charities and housing associations
housing_tenure:Rented: Private Landlord
inc. letting agents
housing_tenure:Shared Ownership
housing_tenure:total
housing_types:Caravan/Park/Temporary
housing_types:Detached
housing_types:Flat (Converted)
housing_types:Flat (Purpose-Built)
housing_types:Residence in Commercial Building
housing_types:Semi-Detached
housing_types:Terraced
housing_types:total
passports:African Countries
passports:Central America
passports:Europe (including European Union)
passports:Middle East or Asia
passports:None
passports:North America or Caribbean
passports:Oceania
(Australia, New Zealand, Indonesia and nearby islands)
passports:Republic of Ireland
passports:South America
passports:United Kingdom
passports:total
relationship_status:Divorced
relationship_status:Married
relationship_status:Same Sex
relationship_status:Separated
relationship_status:Single
relationship_status:Widowed
relationship_status:total
religion:Buddhist
religion:Christian
religion:Hindu
religion:Jewish
religion:Muslim
religion:No Religion
religion:Not Stated
religion:Other Religion
religion:Sikh
religion:total
social_grade:AB - Higher and intermediate managerial, administrative, or professional positions
social_grade:C1 - Supervisory, clerical, and junior managerial/administrative/professional positions
social_grade:C2 - Skilled manual workers
social_grade:DE - Semi-skilled and unskilled manual workers; those on state benefit/unemployed, & lowest grade workers
social_grade:total
street_name
street_url
"""