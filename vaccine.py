import requests
import json
import time
pincode = "485001"
vaccine_type = ""
min_age_limit = 45
dose_num = 2


def cur_date():
    date = time.localtime()
    return ((date.tm_mday, date.tm_mon, date.tm_year))


def fetch_data(pincode, date):
    date_string = '-'.join(str(x) for x in date)
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + \
        pincode+"&date="+date_string
    result = requests.get(url)
    result = json.loads(result.text)
    return result


date = cur_date()
result = fetch_data(pincode, date)
# See all the centers present in that pincode


def centers(data):
    centers_data = []
    for x in result["sessions"]:
        centers_data.append(
            (x["center_id"], x["name"], x["vaccine"], x["available_capacity"]))
    return centers_data


# Vaccine centers for dose 1 regardless of vaccine name but with regard of age
def dose_1(data, min_age):
    dose_1_data = []
    for x in result["sessions"]:
        if x["available_capacity"] > 0 and x["min_age_limit"] == min_age:
            dose_1_data.append(
                (x["center_id"], x["name"], x["vaccine"], x["available_capacity"]))
    return dose_1_data


# Vaccine centers for dose 2 with regard to vaccine type and age limit
def dose_2(data, min_age, vaccine_type):
    dose_2_data = []
    for x in result["sessions"]:
        if(x["min_age_limit"] == min_age_limit):
            if x["vaccine"] == vaccine_type:
                if x["available_capacity_dose2"] > 0:
                    dose_2_data.append(
                        (x["center_id"], x["name"], x["vaccine"], x["available_capacity_dose2"]))
    return dose_2_data


iteration = 1
istrue = True
while istrue:
    print(iteration, "\n")
    if time.localtime().tm_mday != date[2]:
        date = cur_date()
        result = fetch_data(pincode, date)
    received_data = centers(result)
    if received_data != []:
        for x in received_data:
            print(x)
        break
    time.sleep(5)
    iteration += 1
