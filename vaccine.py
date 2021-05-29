import requests
import json
import time
pincode = "485001"
vaccine = "COVISHIELD"
min_age_limit = 45
delay_time = 5

#get the today's date and make a tuple in format of date,month,year
def cur_date():
    date = time.localtime()
    return ((date.tm_mday, date.tm_mon, date.tm_year))


#Function to fetch data from the cowin api
def fetch_data(pincode, date):
    date_string = '-'.join(str(x) for x in date)
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + \
        pincode+"&date="+date_string
    result = requests.get(url)
    result = json.loads(result.text)
    return result





# See all the centers present in that pincode
def centers(data):
    centers_data = []
    for x in data["sessions"]:
        centers_data.append(
            (x["center_id"], x["name"], x["vaccine"], x["available_capacity"]))
    return centers_data


# Vaccine centers for dose 1 regardless of vaccine name but with regard of age
def dose_1(data, min_age):
    dose_1_data = []
    for x in data["sessions"]:
        if x["available_capacity"] > 0 and x["min_age_limit"] == min_age:
            dose_1_data.append(
                (x["center_id"], x["name"], x["vaccine"], x["available_capacity"]))
    return dose_1_data


# Vaccine centers for dose 2 with regard to vaccine type and age limit
def dose_2(data, min_age, vaccine_type):
    dose_2_data = []
    for x in data["sessions"]:
        if(x["min_age_limit"] == min_age and vaccine_type != "" and x["vaccine"] == vaccine_type and x["available_capacity_dose2"] > 0):
            dose_2_data.append(
                (x["center_id"], x["name"], x["vaccine"], x["available_capacity_dose2"]))
    return dose_2_data

def slot_finder(option,delay): #option 1 for dose 1 and option 2 for dose 2

    date = cur_date()
    result = fetch_data(pincode, date)
    istrue = True
    while istrue:

        #prints the current time
        print(time.ctime(), "\n")
        #Updates the data on the change of day
        if time.localtime().tm_mday != date[2]:
            date = cur_date()
            result = fetch_data(pincode, date)
        
        
        #filters the data on the basis of choice
        if option==1:
            received_data = dose_1(result, min_age_limit)
        elif option==2:
            received_data = dose_2(result,min_age_limit,vaccine)

        time.sleep(delay)


        #If it succesfully receies the data then print it and break the program
        if received_data != []:
            for x in received_data:
                print(x)
            break

        #if no available doses are found then update the data in gap of 5s
        else:
            result = fetch_data(pincode, date)
