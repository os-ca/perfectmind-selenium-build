import platform, json, time, ctypes, sys, re
from datetime import datetime
from colorama import init, Fore, Style
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Initializing Colorama || Utils
version= str(json.load(open("./data/bot_data.json","r"))['version'])
init(convert=True) if platform.system() == "Windows" else init()
ctypes.windll.kernel32.SetConsoleTitleW(f"Perfectmind {version}")
# ----------------------------------------------------------------------------------------------           
# ----------------------------------------------------------------------------------------------  
# Settings 
def inits():
    global use_proxies,headless_setting,timeout,queue_,\
        wh_,eventid,startdate,timeevent,threads,driver,delay
    with open("./data/settings.json", "r") as settings:
        data = json.loads(settings.read())
        wh_ = data['webhook']
        threads = data['threads']
        use_proxies = data['use_proxies']
        headless_setting = data["headless_setting"]
        timeout = data['timeout'] *100
        delay = data['delay']
    if use_proxies:
        global proxy_file, proxy_list
        proxy_file = open("./proxies.txt", "r")
        proxy_list = proxy_file.read().split("\n")
        proxy_file.close()
    options = Options()
    options.headless = headless_setting
    options.add_argument("--window-size=900,1090")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome("./chromedriver.exe", options=options)

# ----------------------------------------------------------------------------------------------           
# ----------------------------------------------------------------------------------------------   

cyan = "\033[96m"
lightblue = "\033[94m"
orange = "\033[33m"

class Logger:
    @staticmethod
    def timestamp():
        return str(datetime.now())[11:-3]
    @staticmethod
    def normal(message):
        print(f"{cyan}[{Logger.timestamp()}] {message}")
    @staticmethod
    def other(message):
        print(f"{orange}[{Logger.timestamp()}] {message}")
    @staticmethod
    def error(message):
        print(f"{Fore.RED}[{Logger.timestamp()}] {message}")
    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}[{Logger.timestamp()}] {message}") 
    @staticmethod
    def other2(message):
        print(f"{lightblue}[{Logger.timestamp()}] {message}") 

# ----------------------------------------------------------------------------------------------  
## LOGIN MODULE
def login(username,password):
    Logger.normal("Logging in...")
    login ="https://portal.recreation.ubc.ca/index.php?r=public/index"
    try:
        driver.get(login)
        Logger.normal("Submitting Login Credentials...")
        driver.find_element_by_id("inputEmail").send_keys(username)
        driver.find_element_by_id("inputPassword").send_keys(password)
        driver.find_element_by_id("btn_login").click()
        try:
            WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME, "table-second-col")))
            Logger.success("Successfully Logged In")
         
        except Exception:
            Logger.error(f"Login Error: Invalid Credentials")
            driver.quit()
            return

    except Exception as e:
        Logger.error(f"Login Error: {e}")
        driver.quit()
        return

# ----------------------------------------------------------------------------------------------   
# ---------------------------------------------------------------------------------------------- 
## CART HOLD MODULE
def cart_hold(delay):
    from modules import webhook
    while True:
        driver.refresh()
        bmbutton = driver.find_element_by_xpath('//*[@id="event-attendees"]/div[3]/div/a').get_attribute('class')
        if bmbutton == "bm-button disabled":
            retry=0
            while retry < 3:
                Logger.error(f'Error: Full / Not Opened! Retrying [{retry}]...')
                webhook.wh("cart_hold","Error")
                Logger.other(f"Sleeping... [{delay}]")
                time.sleep(int(delay))
                Logger.normal("Refreshing...")
                driver.refresh()
                retry=retry+1
            else:
                Logger.error(f'Error: Full / Not Opened! Terminating [{retry}]')
                webhook.wh("cart_hold","Error")
                driver.quit()
                return False
        elif bmbutton == "bm-button":
            Logger.success("Successfully Carted!")
            webhook.wh("cart_hold","Success")
            
        Logger.other(f"Sleeping... [{delay}]")
        time.sleep(int(delay))
# ----------------------------------------------------------------------------------------------   
# ----------------------------------------------------------------------------------------------   
## PRESET MODULE        
def task_module(method):
    from modules import get_order
    global name,orderid,bdate,btime
    try:
        Logger.normal("Refreshing...")
        driver.refresh()
        ## NEXT PAGE
        Logger.normal("ATC...")
        bmbutton = driver.find_element_by_xpath('//*[@id="event-attendees"]/div[3]/div/a').get_attribute('class')
        if bmbutton == "bm-button disabled":
            retry=0
            while retry < 3:
                Logger.error(f'Error: Full / Not Opened! Retrying [{retry}]...')
                Logger.other(f"Sleeping... [{delay}s]")
                time.sleep(int(delay))
                Logger.normal("Refreshing...")
                driver.refresh()
                retry=retry+1
            else:
                Logger.error(f'Error: Full / Not Opened! Terminating [{retry}]')
                driver.quit()
                return False
        elif bmbutton == "bm-button":
            Logger.success("Successfully Carted!")
            driver.find_element_by_xpath('//*[@id="event-attendees"]/div[3]/div').click()
            time.sleep(0.2)
            ## QUESTIONNAIRE PAGE
            Logger.normal("Submitting Questionnaire...")
            contactid = driver.find_element_by_xpath('//*[@id="ContactId"]').get_attribute("value")
            sig = driver.find_element_by_id(f"qid_ed47aa42-1934-4f5c-a6c0-31a2185f8d9d_{contactid}_{eventid}")
            sig.clear()
            sig.send_keys(get_profile.user_sig)
            driver.find_element_by_xpath(f'//*[@id="frm6f5befe9-91b5-40b8-80e1-266c93dc4f0b_{contactid}_{eventid}"]/div[2]/ul/li[3]/div/fieldset/div/label').click()
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div[2]/a').click()
            ## FEES & EXTRA PAGEs
            time.sleep(0.2)
            Logger.normal("Redirecting...")
            driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[5]/a').click()
            ## REVIEW PAGE
            time.sleep(0.2)
            Logger.normal("Checkout Page...")
            driver.find_element_by_class_name('bm-form-checkout').click()
            time.sleep(1.2)

            if method == "checkout_link":
                co_link = driver.current_url
                src = driver.find_element_by_class_name("online-store").get_attribute("src")
                driver.get(src)
                Logger.normal("Entering SRC Payment Page...")
                time.sleep(0.2)
                info = re.split(',|\n',(driver.find_element_by_class_name('item-details').text))
                name,orderid,bdate,btime = info[0],info[1],info[2],info[3]
                get_order.get_order(name,orderid,bdate,btime)
                webhook.wh("checkout_link",co_link)
                driver.close()
                
            elif method == "full_checkout":
                checkout = "gg"
                src = driver.find_element_by_class_name("online-store").get_attribute("src")
                driver.get(src)
                Logger.normal("Entering SRC Payment Page...")
                time.sleep(0.2)
                info = re.split(',|\n',(driver.find_element_by_class_name('item-details').text))
                name,orderid,bdate,btime = info[0],info[1],info[2],info[3]
                get_order.get_order(name,orderid,bdate,btime)
                # fetches unique cc id for xpaths
                cc_ = (driver.find_element_by_xpath("//input[@name='chooseCreditCard'][@type='radio']").get_attribute('aria-labelledby')).split('-')
                cc_id = int(cc_[3])+1
                # actual autofill process
                driver.find_element_by_xpath(f'//*[@id="credit-card-holder-name-{cc_id}"]').send_keys(get_profile.cc_name)
                driver.find_element_by_xpath(f'//*[@id="credit-card-number-{cc_id}"]').send_keys(get_profile.cc_num)
                driver.find_element_by_xpath(f'//*[@id="cvv-number-{cc_id}"]').send_keys(get_profile.cc_ccv)
                driver.find_element_by_xpath(f'//*[@id="street-{cc_id}"]').send_keys(get_profile.cc_strt)
                driver.find_element_by_xpath(f'//*[@id="city-{cc_id}"]').send_keys(get_profile.cc_city)
                driver.find_element_by_xpath(f'//*[@id="zip-code-{cc_id}"]').send_keys(get_profile.cc_zip)
                # drop down menu autofill process
                driver.find_element_by_xpath(f'//*[@id="country-{cc_id}"]/option[@value=38]').click()
                driver.find_element_by_xpath(f'//*[@id="expiry-month-{cc_id}"]/option[@value={get_profile.cc_month}]').click()
                driver.find_element_by_xpath(f'//*[@id="year-{cc_id}"]/option[@value={get_profile.cc_year}]').click()
                driver.find_element_by_xpath(f'//*[@id="state-{cc_id}"]/option[@value=515]').click()
                # Place my order
                Logger.other("Processing...")
                driver.find_element_by_class_name("process-now").click()
                time.sleep(2)
                try: 
                    paid = driver.find_element_by_class_name('//*[@id="thank-you-body"]/div[1]/div/h1').get_attribute("innerHTML")
                    if paid == "Thank you!":
                        Logger.success("Checked Out")
                        webhook.wh("full_checkout",checkout)
                        driver.close()
                    else:
                        Logger.error("Error")
                        checkout = "Payment Error"
                        webhook.wh("checkout_error",checkout)
                except Exception as e:
                    Logger.error(f"Payment Error!")
                    checkout = "Payment Error"
                    webhook.wh("checkout_error",checkout)
                    
        
    except Exception as e:
        Logger.error(e)
        driver.quit()

# ----------------------------------------------------------------------------------------------   
# ----------------------------------------------------------------------------------------------     
# MENU INTERFACE
if __name__ == '__main__':
    from modules import timer, get_profile,get_eventid,webhook
    while True:
        print(f"{Fore.CYAN}{Style.BRIGHT}OSCAR AIO {version}\n")
        global headless_setting
        print("[1] Checkout Link\n[2] Full Checkout\n[3] Cart Hold\n[4] View Settings\n[5] Exit\n")
        selection = input("Input: ")
        print("\n")
        # CHECKOUT LINK
        if selection == "1": 
            print("Checkout Link Mode\n")
            n = int(input("Profile: "))
            eventid = input("Input Event ID: ")
            get_profile.get_profile(n)
            get_eventid.get_eventid(eventid)
            timed_event = input("Timed Event? [Y] | [N]: ").lower()
            inits()
            if timed_event == "y":
                user_time = input("Input Time [HH:MM:SS]: ")
                login(get_profile.username,get_profile.password)
                Logger.normal("Bypass Redirect...")
                driver.get(get_eventid.url)
                timer.timer(user_time)
                Logger.other(f"Sleeping for: {timer.timer(user_time)} second(s)...")
                time.sleep(timer.timer(user_time))
                task_module("checkout_link")
                driver.quit()
            elif timed_event == "n":  
                login(get_profile.username,get_profile.password)
                Logger.normal("Bypass Redirect...")
                driver.get(get_eventid.url)
                task_module("checkout_link")
                driver.quit()
            else:
                pass

        # FULL CHECKOUT
        elif selection == "2":
            print("Full Checkout Mode\n")  
            n = int(input("Profile: "))
            eventid = input("Input Event ID: ")
            get_profile.get_profile(n)
            get_eventid.get_eventid(eventid)
            timed_event = input("Timed Event? [Y] | [N]: ").lower()
            inits()
            if timed_event == "y":
                user_time = input("Input Time [HH:MM:SS]: ")
                login(get_profile.username,get_profile.password)
                Logger.normal("Bypass Redirect...")
                driver.get(get_eventid.url)
                timer.timer(user_time)
                Logger.other(f"Sleeping for: {timer.timer(user_time)} second(s)...")
                time.sleep(timer.timer(user_time))
                task_module("full_checkout")
                driver.quit()
            elif timed_event == "n":
                login(get_profile.username,get_profile.password)
                Logger.normal("Bypass Redirect...")
                driver.get(get_eventid.url)
                task_module("full_checkout")
                driver.quit()
            else:
                pass

        # CART HOLD
        elif selection == "3": 
            print("Cart Hold Mode\n")
            n = int(input("Profile: "))
            eventid = input("Input Event ID: ")
            get_profile.get_profile(n)
            get_eventid.get_eventid(eventid)
            timed_event = input("Timed Event? [Y] | [N]: ").lower()   
            inits()
            if timed_event == "y":
                user_time = input("Input Time [HH:MM:SS]: ")
                login(get_profile.username,get_profile.password)
                Logger.normal("Bypass Redirect...")
                driver.get(get_eventid.url)
                Logger.other(f"Sleeping for: {timer.timer(user_time)} second(s)...")
                time.sleep(timer.timer(user_time))
                cart_hold(delay)   

            elif timed_event == "n":
                login(get_profile.username,get_profile.password)
                Logger.normal("Bypass Redirect...")
                driver.get(get_eventid.url)
                cart_hold(delay)

        # VIEW SETTINGS
        elif selection == "4":
            print("View Settings\n")
            with open("./data/settings.json", "r+") as settings:
                data = json.load(settings)
                for index,key in enumerate(data,start=1):
                    print(f"[{index}] {key}: {data[key]}")
                print(f"[{index+1}] Test Webhook\n[{index+2}] Go Back")  
                edit_settings = input("\nInput: ")
                if edit_settings == f'{index-5}':
                    edit_ = input(f"\nThread: ")
                    data["threads"] = int(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)
                elif edit_settings == f'{index-4}':
                    edit_ = input(f"\nUse Proxies: ").lower()
                    data["use_proxies"] = bool(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)
                elif edit_settings == f'{index-3}':
                    edit_ = input(f"\nHeadless: ").lower()
                    data["headless_setting"] = bool(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)
                elif edit_settings == f'{index-2}':
                    edit_ = input(f"\nWebhook: ")
                    data["webhook"] = str(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)
                elif edit_settings == f'{index-1}':
                    edit_ = input(f"\nTimeout: ")
                    data["timeout"] = int(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)    
                elif edit_settings == f'{index}':
                    edit_ = input(f"\nDelay: ")
                    data["delay"] = int(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)    
                elif edit_settings == f'{index+1}':
                    from modules import webhook
                    with open("./data/settings.json", "r") as settings:
                        data = json.loads(settings.read())
                        wh_ = data['webhook']
                    webhook.wh("test_wh","Success")
                elif edit_settings == f'{index+2}':
                    continue
                else:
                    pass
        
        # SYS EXIT
        elif selection == "5":
            print("Exiting...")
            time.sleep(0.1)
            sys.exit()
        
        # DEVELOPMENT
        elif selection == "6":
            n = int(input("Profile: "))
            #eventid = input("Input Event ID: ")
            get_profile.get_profile(n)
            #get_eventid.get_eventid(eventid)
            inits()
            
            
        else:
            pass
