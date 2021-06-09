from functions import initialize_token, fetch_data_calendar, currrent_date, is_token_valid, calendar_data
import time
pincode = "485001"
vaccine = "COAXIN"
min_age_limit = 18
mobile = 8817141845
base_request_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'origin': 'https://selfregistration.cowin.gov.in/',
    'referer': 'https://selfregistration.cowin.gov.in/'
}


def slot_finder(option, pincode, vaccine, min_age_limit, auth_token, header, date):
    if option == 1:
        result = fetch_data_calendar(pincode, date, header, "")

    elif option == 2:
        result = fetch_data_calendar(pincode, date, header, vaccine)

    if result.status_code == 200:
        result = result.json()
    received_data = calendar_data(result, min_age_limit,option)
    if received_data != []:
        for x in received_data:
            print(x)
        return True
    if received_data==[]:
        return False

# to check if the data fetched is correct or not

# option 1 for dose 1 and option 2 for dose 2


def main():
    pincode = input("Pincode")
    vaccine = input("Name of vaccine (Leave blank if no preferrence)").upper()
    min_age_limit = int(input("Min age"))
    option = int(input("Options :\n 1. Dose 1 \n2.Dose 2"))
    delay = int(input("Delay time greater than 5(default = 5)"))
    if(delay<5):
        delay=5
    mobile = int(input("Mobile Number"))
    date = currrent_date()
    header, auth_token = initialize_token(mobile)
    print("Initialized token succesfully")
    istrue = True
    while istrue:
        print(time.ctime(), "\n")
        if time.localtime().tm_mday != date[0]:
            date = currrent_date()
        try:
            is_valid = is_token_valid(auth_token)
            print(is_valid)
            if not is_valid:
                header, auth_token = initialize_token(mobile)
                print("slot")
            else:
                x = slot_finder(option, pincode, vaccine,min_age_limit, auth_token, header, date)
                if x:
                    istrue = False
        except Exception as e:
            print(str(e))
        time.sleep(delay)

