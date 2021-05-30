import requests
import json
import time
from datetime import datetime, date
from hashlib import sha256
import jwt
import copy
pincode = "485001"
vaccine = "COAXIN"
min_age_limit = 18
mobile = 8817141845
BOOKING_URL = "https://cdn-api.co-vin.in/api/v2/appointment/schedule"
URL_PINCODE = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/findByPin"
BENEFICIARIES_URL = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"
CALENDAR_URL_DISTRICT = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"
CALENDAR_URL_PINCODE = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin"
CAPTCHA_URL = "https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha"
OTP_URL = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
VALIDATE_OTP = "https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp"

base_request_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'origin': 'https://selfregistration.cowin.gov.in/',
    'referer': 'https://selfregistration.cowin.gov.in/'
}

# Generate an otp


def generate_otp(mobile, header):
    data = {
        "mobile": mobile,
        # Some sort of secret key
        "secret": "U2FsdGVkX1+z/4Nr9nta+2DrVJSv7KS6VoQUSQ1ZXYDx/CJUkWxFYG6P3iM/VW+6jLQ9RDQVzp/RcZ8kbT41xw==",
    }
    print(f"Requesting OTP with mobile number {mobile}..")
    txn_id = requests.post(
        url=OTP_URL,
        json=data,
        headers=header,
    )
    return txn_id


# Verify that otp
def verify_otp(otp, txn_id, header):
    data = {"otp": sha256(str(otp).encode(
        'utf-8')).hexdigest(), "txn_id": txn_id}
    token = requests.post(
        url=VALIDATE_OTP,
        json=data,
        headers=header)
    return token


def is_token_valid(token):
    payload = jwt.decode(token, options={"verify_signature": False})
    remaining_seconds = payload['iat'] + 600 - int(time.time())
    if remaining_seconds <= 60:
        print("Token is about to expire in next 1 min ...")
    if remaining_seconds <= 1*30:  # 30 secs early before expiry for clock issues
        return False
    return True

# Create header with the authorization token (Bearer Token)


def create_header(auth_token):
    header = copy.deepcopy(base_request_header)
    header["Authorization"] = f"Bearer {auth_token}"
    return header


# get the today's date and make a tuple in format of date,month,year
def currrent_date():
    date = time.localtime()
    return ((date.tm_mday, date.tm_mon, date.tm_year))


def next_date(n):
    from datetime import timedelta, date
    date_t = date.today() + timedelta(n)
    return date_t.day, date_t.month, date_t.year


# Function to fetch data from the cowin api
def fetch_data_calendar(pincode, date, header):
    date_string = '-'.join(str(x) for x in date)
    url = CALENDAR_URL_PINCODE
    data = {"pincode": pincode, "date": date_string}
    result = requests.get(url, params=data, headers=header)
    return result

# Fetch data in realtime


def fetch_data_date(pincode, date, header):
    date_string = '-'.join(str(x) for x in date)
    url = URL_PINCODE
    data = {"pincode": pincode, "date": date_string}
    result = requests.get(url, params=data, headers=header)
    return result

# Fetch data by calendar district


def fetch_data_calendar_district(district_id, date, header):
    date_string = '-'.join(str(x) for x in date)
    url = CALENDAR_URL_DISTRICT
    data = {"district_id": district_id, "date": date_string}
    result = requests.get(url, params=data, headers=header)
    return result

# See all the centers present in that pincode for a particular date


def centers_by_date(data):
    centers_data = []
    for x in data["sessions"]:
        centers_data.append(
            (x["center_id"], x["name"], x["vaccine"], x["available_capacity"]))
    return centers_data

# See all the available centers in next 7 dats


def centers_by_calendar(data):
    centers_data = []
    for x in data["centers"]:
        for j in x["sessions"]:
            centers_data.append(
                (x["center_id"], x["name"],  j["vaccine"], j["available_capacity_dose1"], j["available_capacity_dose2"], j["date"]))
    return centers_data


# Vaccine centers for dose 1 regardless of vaccine name but with regard of age
def dose_1_date(data, min_age):
    dose_1_data = []
    for x in data["sessions"]:
        if x["available_capacity"] > 0 and x["min_age_limit"] == min_age:
            dose_1_data.append(
                (x["center_id"], x["name"], x["vaccine"], x["available_capacity"]))
    return dose_1_data

# Vaccien centers for dose 1 for next 7 days


def dose_1_calendar(data, min_age):
    dose_1_data = []
    for x in data["centers"]:
        for j in x["sessions"]:
            if j["available_capacity"] > 0 and j["min_age_limit"] == min_age:
                dose_1_data.append((x["center_id"], x["name"],  j["vaccine"],
                                    j["available_capacity_dose1"], j["available_capacity_dose2"], j["date"]))
    return dose_1_data

# Vaccine centers for dose 2 with regard to vaccine type and age limit


def dose_2_date(data, min_age, vaccine_type):
    dose_2_data = []
    for x in data["sessions"]:
        if(x["min_age_limit"] == min_age and vaccine_type != "" and x["vaccine"] == vaccine_type and x["available_capacity_dose2"] > 0):
            dose_2_data.append(
                (x["center_id"], x["name"], x["vaccine"], x["available_capacity_dose2"]))
    return dose_2_data

# Vaccien centers for dose 2 for next 7 days


def dose_2_calendar(data, min_age, vaccine_type):
    dose_2_data = []
    for x in data["centers"]:
        for j in x["sessions"]:
            if(j["min_age_limit"] == min_age and vaccine_type != "" and j["vaccine"] == vaccine_type and j["available_capacity_dose2"] > 0):
                dose_2_data.append((x["center_id"], x["name"],  j["vaccine"],
                                    j["available_capacity_dose1"], j["available_capacity_dose2"], j["date"]))
    return dose_2_data



def fetch_beneficiaries(header):
    return requests.get(BENEFICIARIES_URL, headers=header)


def initialize_token():
    txn_id = generate_otp(mobile,base_request_header)
    if txn_id is None:
        return txn_id
    otp=int(input())
    t_end = time.time() + 60 * 3  # try to read OTP for atmost 3 minutes
    while time.time() < t_end:
        auth_token=verify_otp(otp,txn_id,base_request_header)
    if not otp:
        return None
    if txn_id.status_code==200:
         txn_id=txn_id.json()["txn_id"]
    if auth_token.status_code==200:
        auth_token=auth_token.json()["token"]
    else:
        txn_id = generate_otp(mobile,base_request_header)
        auth_token=verify_otp(otp,txn_id,base_request_header)
    header = create_header(auth_token)

    return header,auth_token

#to check if the data fetched is correct or not
def check_data(result):
    if result.status_code == 200:
        result = json.loads(result.text)
        return result
    else:
        return False

# option 1 for dose 1 and option 2 for dose 2
def slot_finder(option, delay, auth_token, pincode, vaccine,min_age_limit):

    date = currrent_date()
    header,auth_token = initialize_token()
    result = fetch_data_calendar(pincode, date, header)
    if not is_token_valid(auth_token):
        header,auth_token = initialize_token()
        result = fetch_data_calendar(pincode, date, header)
    istrue = True
    while istrue:

        # prints the current time
        print(time.ctime(), "\n")
        # Updates the data on the change of day
        if not is_token_valid(auth_token):
            header,auth_token = initialize_token()
            result = fetch_data_calendar(pincode, date, header)
        if time.localtime().tm_mday != date[2]:
            date = currrent_date()
            result = fetch_data_calendar(pincode, date, header)
            

        # filters the data on the basis of choice
        if option == 1:
            received_data = dose_1_calendar(result, min_age_limit)
        elif option == 2:
            received_data = dose_2_calendar(result, min_age_limit, vaccine)
            print(received_data)

        time.sleep(delay)

        # If it succesfully receies the data then print it and break the program
        if received_data != []:
            for x in received_data:
                print(x)
            break

        # if no available doses are found then update the data in gap of 5s
        else:
            result = fetch_data_calendar(pincode, date, header)
            result = check_data(result)
            if not result == False:
                pass
            else:
                header,auth_token=initialize_token()
                fetch_data_calendar(pincode,data,header)
