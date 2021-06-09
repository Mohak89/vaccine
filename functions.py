import requests
import json
import time
from datetime import datetime, date
from hashlib import sha256
import jwt
import re
import copy
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
        "secret": "U2FsdGVkX1+z/4Nr9nta+2DrVJSv7KS6VoQUSQ1ZXYDx/CJUkWxFYG6P3iM/VW+6jLQ9RDQVzp/RcZ8kbT41xw=="
    }
    print(f"Requesting OTP with mobile number {mobile}..")
    txnid = requests.post(url=OTP_URL, json=data, headers=header)
    if txnid.status_code == 200:
        txnid = txnid.json()["txnId"]
        return txnid
    else:
        return None


# Verify that otp
def verify_otp(txnid, header):
    # t_end = time.time() + 60 * 3  # try to read OTP for atmost 3 minutes
    # while time.time() < t_end:
    #     response = requests.get(storage_url)
    #     if response.status_code == 200:
    #         print("OTP SMS is:" + response.text)

    #         OTP = response.text
    #         OTP = re.findall("[0-9]{6}",OTP)[0]
    #         if not OTP:
    #             time.sleep(5)
    #             continue
    #         break
    #     else:
    #         # Hope it won't 500 a little later
    #         print("error fetching OTP API:" + response.text)
    #         time.sleep(5)

    # if not OTP:
    #     return None
    otp = int(input())
    data = {"otp": sha256(str(otp).encode(
        'utf-8')).hexdigest(), "txnId": txnid}
    token = requests.post(url=VALIDATE_OTP, json=data, headers=header)
    if token.status_code == 200:
        return token.json()["token"]
    else:
        return None


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
    return (date.tm_mday, date.tm_mon, date.tm_year)


def next_date(n):
    from datetime import timedelta, date
    date_t = date.today() + timedelta(n)
    return date_t.day, date_t.month, date_t.year


# Function to fetch data from the cowin api
def fetch_data_calendar(pincode, date, header, vaccine_type):
    date_string = '-'.join(str(x) for x in date)
    url = CALENDAR_URL_PINCODE
    if vaccine_type != " ":
        data = {"pincode": pincode, "date": date_string, "vaccine": vaccine_type}
    else:
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
                (x["center_id"], x["name"], x["vaccine"], x["available_capacity_dose1"]))
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


def calendar_data(data, min_age, option):
    cal_data = []
    for x in data["centers"]:
        for j in x["sessions"]:
            if(j["min_age_limit"] == min_age):
                if option == 2 and j["available_capacity_dose2"] > 0:
                    cal_data.append(
                        (x["center_id"], x["name"],  j["vaccine"], j["available_capacity_dose2"], j["date"]))
                elif option == 1 and j["available_capacity_dose1"] > 0:
                    cal_data.append(
                        (x["center_id"], x["name"],  j["vaccine"], j["available_capacity_dose1"], j["date"]))

    return cal_data


def fetch_beneficiaries(header):
    return requests.get(BENEFICIARIES_URL, headers=header)


def initialize_token(mobile):
    txnid = None
    while txnid is None:
        try:
            txnid = generate_otp(mobile, base_request_header)
            print("Otp generated:")
        except Exception as e:
            print(str(e))
            print('OTP Retrying in 5 seconds')
            time.sleep(5)

    auth_token = None
    while auth_token is None:
        try:
            auth_token = verify_otp(txnid, base_request_header)
        except Exception as e:
            print(str(e))
            print('OTP Retrying in 5 seconds')
            time.sleep(5)

    header = create_header(auth_token)
    return header, auth_token
