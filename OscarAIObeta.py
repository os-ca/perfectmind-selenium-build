import platform, json, time, ctypes, sys, threading, asyncio, queue,csv, requests,re,subprocess
from datetime import datetime
from modules import get_eventid,timer

try:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from colorama import init, Fore

except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])

# Initializing Colorama || Utils
version= str(json.load(open("./data/bot_data.json","r"))['version'])
init(convert=True) if platform.system() == "Windows" else init()
ctypes.windll.kernel32.SetConsoleTitleW(f"PERFECTMIND {version} | BETA")
# ----------------------------------------------------------------------------------------------           
# ----------------------------------------------------------------------------------------------  
# Settings 
def inits():
    global use_proxies,headless_setting,timeout,\
        wh_,eventid,threads,delay
    with open("./data/settings.json", "r") as settings:
        data = json.loads(settings.read())
        wh_ = data['webhook']
        threads = data['threads']
        use_proxies = data['use_proxies']
        headless_setting = data["headless_setting"]
        timeout = data['timeout'] *100
        delay = data['delay']

    global queue_
    queue_ = queue.Queue(maxsize=threads)
    global detected,carted,success,failed
    detected,carted,success,failed = 0,0,0,0

def get_profiles(n):
    global username,password,user_sig,cc_num,cc_ccv,cc_strt,cc_city,cc_zip,cc_month,cc_year,cc_name,count
    version= str(json.load(open("./data/bot_data.json","r"))['version'])
    new_list = []
    with open("./data/profiles.csv",'r',newline='',encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_list.extend([[row["username"],row['password'],row['signature'],row['number'],row['ccv'],\
                row['street'],row['city'],row['zip'],row['month'],row['year'],row['fullname']]])
        username,password,user_sig,cc_num,cc_ccv,cc_strt,cc_city,cc_zip,cc_month,cc_year,cc_name = \
            new_list[n][0],new_list[n][1],new_list[n][2],new_list[n][3],new_list[n][4],new_list[n][5],\
            new_list[n][6],new_list[n][7],new_list[n][8],new_list[n][9],new_list[n][10]
        

        ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | Profile(s): {str(profiles)}")

def profile_count():
    global profiles
    with open("./data/profiles.csv",'r',newline='',encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        profiles = int(len(list(reader))-1)
        return profiles

def wh(method,checkout,username):
    if method  == "checkout_link":
        data = {
                    "username" : "Perfectmind"
                }
        data["embeds"] = [
                {
                    "title" : "Successful Checkout",
                    "timestamp": f"{datetime.utcnow()}",
                    "footer": {
                        "icon_url": "https://cdn.discordapp.com/attachments/854247964612493342/854494516269809664/1WlC-_yW_400x400.jpg",
                        "text": f"Perfecetmind {version}"
                    },
                    "fields": [
                        {
                            "name": "Event ID",
                            "value": f"{get_eventid.event_id}",
                            "inline": False
                        },
                        {
                            "name": "Order ID",
                            "value": f"{orderid}",
                            "inline": False
                        },
                        {
                            "name": "Start Date",
                            "value": f"{bdate}",
                            "inline": True
                        },
                        {
                            "name": "Time",
                            "value": f"{btime}",
                            "inline": True
                        },
                        {
                            "name": "Name",
                            "value": f"{name}",
                            "inline": True
                        },
                        {
                            "name": "Mode",
                            "value": f"{method}",
                            "inline": False
                        },
                        {
                            "name": "Checkout Link",
                            "value": f"{checkout}",
                            "inline": False
                        },
                    
                    ]
                    
                }
            ]
    elif method == "full_checkout":
        data = {
                    "username" : "UBC MY BITCH"
                }
        data["embeds"] = [
                {
                    "title" : "Successful Checkout",
                    "timestamp": f"{datetime.utcnow()}",
                    "footer": {
                        "icon_url": "https://cdn.discordapp.com/attachments/854247964612493342/854494516269809664/1WlC-_yW_400x400.jpg",
                        "text": f"oscar bot {version}"
                    },
                    "fields": [
                        {
                            "name": "Event ID",
                            "value": f"{get_eventid.event_id}",
                            "inline": False
                        },
                        {
                            "name": "Order ID",
                            "value": f"{orderid}",
                            "inline": False
                        },
                        {
                            "name": "Start Date",
                            "value": f"{bdate}",
                            "inline": True
                        },
                        {
                            "name": "Time",
                            "value": f"{btime}",
                            "inline": True
                        },
                        {
                            "name": "Name",
                            "value": f"{name}",
                            "inline": True
                        },
                        {
                            "name": "Mode",
                            "value": f"{method}",
                            "inline": False
                        }
                    ]
                    
                }
            ]
    elif method == "checkout_error":
        data = {
                    "username" : "UBC MY BITCH"
                }
        data["embeds"] = [
                {
                    "title" : "Payment Declined",
                    "timestamp": f"{datetime.utcnow()}",
                    "footer": {
                        "icon_url": "https://cdn.discordapp.com/attachments/854247964612493342/854494516269809664/1WlC-_yW_400x400.jpg",
                        "text": f"oscar bot {version}"
                    },
                    "fields": [
                        {
                            "name": "Event ID",
                            "value": f"{get_eventid.event_id}",
                            "inline": False
                        },
                        {
                            "name": "Order ID",
                            "value": f"{orderid}",
                            "inline": False
                        },
                        {
                            "name": "Start Date",
                            "value": f"{bdate}",
                            "inline": True
                        },
                        {
                            "name": "Time",
                            "value": f"{btime}",
                            "inline": True
                        },
                        {
                            "name": "Name",
                            "value": f"{name}",
                            "inline": True
                        },
                        {
                            "name": "Mode",
                            "value": f"{method}",
                            "inline": False
                        }
                    ]
                    
                }
            ]
    elif method  == "cart_hold":

        data = {
                    "username" : "UBC MY BITCH"
                }
        data["embeds"] = [
                {
                    "title" : f"Cart Hold {checkout}",
                    "timestamp": f"{datetime.utcnow()}",
                    "footer": {
                        "icon_url": "https://cdn.discordapp.com/attachments/854247964612493342/854494516269809664/1WlC-_yW_400x400.jpg",
                        "text": f"oscar bot {version}"
                    },
                    "fields": [
                        {
                            "name": "Event ID",
                            "value": f"{get_eventid.event_id}",
                            "inline": False
                        },
                        {
                            "name": "User",
                            "value": f"{username}",
                            "inline": False
                        }
                                
                    ]
                    
                }
            ]
    elif method  == "test_wh":
        data = {
                    "username" : "UBC MY BITCH"
                }
        data["embeds"] = [
                {
                    "title" : f"Test {checkout}",
                    "timestamp": f"{datetime.utcnow()}",
                    "footer": {
                        "icon_url": "https://cdn.discordapp.com/attachments/854247964612493342/854494516269809664/1WlC-_yW_400x400.jpg",
                        "text": f"oscar bot {version}"
                    }
                }           
            ]
                                 
    try:
        result = requests.post(wh_, json = data)   
        result.raise_for_status()   
    except requests.exceptions.HTTPError as e:
        Logger.error(e)
    else:
        pass
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
#-----------------------------------------------------------------------------------------------   
### Task Modules ###
class TaskModule:
    def __init__(self,username,password,user_sig,cc_num,cc_ccv,cc_strt,cc_city,cc_zip,cc_month,cc_year,cc_name):
        options = Options()
        options.headless = headless_setting
        options.add_argument("--window-size=900,1090")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome("./chromedriver.exe", options=options)
        self.username,self.password,self.user_sig,self.cc_num,self.cc_ccv,self.cc_strt,self.cc_city,self.cc_zip,self.cc_month,self.cc_year,self.cc_name = username,password,user_sig,cc_num,cc_ccv,cc_strt,cc_city,cc_zip,cc_month,cc_year,cc_name
        queue_.put(self)
        Logger.normal(f"[{self.username}] Starting Thread...")
        ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
        threading.Thread(target=self.run).start()
    def run(self):
        asyncio.run(self.login_())

    async def login_(self):
        Logger.normal(f"[{self.username}] Logging in...")
        self.driver.get("https://portal.recreation.ubc.ca/index.php?r=public%2Findex")
        Logger.normal(f"[{self.username}] Submitting Login Credentials...")
        self.driver.find_element_by_id("inputEmail").send_keys(username)
        self.driver.find_element_by_id("inputPassword").send_keys(password)
        self.driver.find_element_by_id("btn_login").click()
        try:
            global detected,failed
            WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.CLASS_NAME, "table-second-col")))
            Logger.success(f"[{self.username}] Successfully Logged In")
            detected+=1
            ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
            Logger.normal(f"[{self.username}] Bypass Redirect...")
            self.driver.get(get_eventid.url)
            if timed_event == "y":
                Logger.other(f"Sleeping for: {timer.timer(user_time)} second(s)...")
                await asyncio.sleep(timer.timer(user_time))
                await self.task_module(method)
            elif timed_event == "n":
                await self.task_module(method)
            
        except Exception as e:
            Logger.error(f"[{self.username}] Login Error: {e}")
            self.driver.quit()
            sys.exit()

    async def task_module(self,method):
        global name,orderid,bdate,btime
        try:
            global detected,carted,success,failed
            Logger.normal(f"[{self.username}] Refreshing...")
            self.driver.refresh()
            ## NEXT PAGE
            Logger.normal("ATC...")
            bmbutton = self.driver.find_element_by_xpath('//*[@id="event-attendees"]/div[3]/div/a').get_attribute('class')
            if bmbutton == "bm-button disabled":
                retry=0
                while retry < 3:
                    Logger.error(f'[{self.username}] Error: Full / Not Opened! Retrying [{retry}]...')
                    ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
                    Logger.other(f"[{self.username}] Sleeping... [{delay}s]")
                    time.sleep(int(delay))
                    Logger.normal("Refreshing...")
                    self.driver.refresh()
                    retry=retry+1
                else:
                    Logger.error(f'[{self.username}] Error: Full / Not Opened! Terminating [{retry}]')
                    self.driver.quit()
             
      

            elif bmbutton == "bm-button":
                Logger.success(f"[{self.username}] Successfully Carted!")
                success+=1
                ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
                self.driver.find_element_by_xpath('//*[@id="event-attendees"]/div[3]/div').click()
                time.sleep(0.2)
                ## QUESTIONNAIRE PAGE
                Logger.normal(f"[{self.username}] Submitting Questionnaire...")
                contactid = self.driver.find_element_by_xpath('//*[@id="ContactId"]').get_attribute("value")
                sig = self.driver.find_element_by_id(f"qid_ed47aa42-1934-4f5c-a6c0-31a2185f8d9d_{contactid}_{eventid}")
                sig.clear()
                sig.send_keys(self.user_sig)
                self.driver.find_element_by_xpath(f'//*[@id="frm6f5befe9-91b5-40b8-80e1-266c93dc4f0b_{contactid}_{eventid}"]/div[2]/ul/li[3]/div/fieldset/div/label').click()
                time.sleep(0.2)
                self.driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div[2]/a').click()
                ## FEES & EXTRA PAGEs
                time.sleep(0.2)
                Logger.normal("Redirecting...")
                self.driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[5]/a').click()
                ## REVIEW PAGE
                time.sleep(0.2)
                Logger.normal("Checkout Page...")
                self.driver.find_element_by_class_name('bm-form-checkout').click()
                time.sleep(1.2)

                if method == "checkout_link":
                    co_link = self.driver.current_url
                    src = self.driver.find_element_by_class_name("online-store").get_attribute("src")
                    self.driver.get(src)
                    Logger.normal("Entering SRC Payment Page...")
                    time.sleep(0.2)
                    info = re.split(',|\n',(self.driver.find_element_by_class_name('item-details').text))
                    name,orderid,bdate,btime = info[0],info[1],info[2],info[3]
                    success+=1
                    ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
                    wh("checkout_link",co_link,self.username)
                    self.driver.close()
                    
                elif method == "full_checkout":
                    checkout = "gg"
                    src = self.driver.find_element_by_class_name("online-store").get_attribute("src")
                    self.driver.get(src)
                    Logger.normal(f"[{self.username}] Entering SRC Payment Page...")
                    time.sleep(0.2)
                    info = re.split(',|\n',(self.driver.find_element_by_class_name('item-details').text))
                    name,orderid,bdate,btime = info[0],info[1],info[2],info[3]
                    # fetches unique cc id for xpaths
                    cc_ = (self.driver.find_element_by_xpath("//input[@name='chooseCreditCard'][@type='radio']").get_attribute('aria-labelledby')).split('-')
                    cc_id = int(cc_[3])+1
                    # actual autofill process
                    self.driver.find_element_by_xpath(f'//*[@id="credit-card-holder-name-{cc_id}"]').send_keys(cc_name)
                    self.driver.find_element_by_xpath(f'//*[@id="credit-card-number-{cc_id}"]').send_keys(cc_num)
                    self.driver.find_element_by_xpath(f'//*[@id="cvv-number-{cc_id}"]').send_keys(cc_ccv)
                    self.driver.find_element_by_xpath(f'//*[@id="street-{cc_id}"]').send_keys(cc_strt)
                    self.driver.find_element_by_xpath(f'//*[@id="city-{cc_id}"]').send_keys(cc_city)
                    self.driver.find_element_by_xpath(f'//*[@id="zip-code-{cc_id}"]').send_keys(cc_zip)
                    # drop down menu autofill process
                    self.driver.find_element_by_xpath(f'//*[@id="country-{cc_id}"]/option[@value=38]').click()
                    self.driver.find_element_by_xpath(f'//*[@id="expiry-month-{cc_id}"]/option[@value={cc_month}]').click()
                    self.driver.find_element_by_xpath(f'//*[@id="year-{cc_id}"]/option[@value={cc_year}]').click()
                    self.driver.find_element_by_xpath(f'//*[@id="state-{cc_id}"]/option[@value=515]').click()
                    # Place my order
                    Logger.other(f"[{self.username}] Processing...")
                    self.driver.find_element_by_class_name("process-now").click()
                    time.sleep(2)
                    try: 
                        paid = self.driver.find_element_by_class_name('//*[@id="thank-you-body"]/div[1]/div/h1').get_attribute("innerHTML")
                        if paid == "Thank you!":
                            Logger.success(f"[{self.username}] Checked Out")
                            success+=1
                            ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
                            wh("full_checkout",checkout,self.username)
                            self.driver.close()
                        else:
                            Logger.error(f"[{self.username}] Error")
                            failed+=1
                            ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
                            checkout = "Payment Error"
                            wh("checkout_error",checkout,self.username)
                    except Exception as e:
                        Logger.error(f"[{self.username}] Payment Error!")
                        failed+=1
                        ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
                        checkout = "Payment Error"
                        wh("checkout_error",checkout,self.username)

                    finally:
                        await asyncio.sleep(1.5)
                        queue_.get()
                        queue_.task_done()
                            
        except Exception as e:
            Logger.error(e)
            failed+=1
            ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
            self.driver.quit()

        finally:
            await asyncio.sleep(1.5)
            ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Success: {success} | Failed: {failed}")
            queue_.get()
            queue_.task_done()
#-----------------------------------------------------------------------------------------------   
#-----------------------------------------------------------------------------------------------   
### Cart Hold Modules ###
class CartHold:
    def __init__(self,username,password):
        options = Options()
        options.headless = headless_setting
        options.add_argument("--window-size=900,1090")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome("./chromedriver.exe", options=options)
        self.username,self.password = username,password
        queue_.put(self)
        Logger.normal(f"[{self.username}] Starting Thread...")
        ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Failed: {failed}")
        threading.Thread(target=self.run).start()

    def run(self):
        asyncio.run(self.login_())        

    async def login_(self):
        Logger.normal(f"[{self.username}] Logging in...")
        self.driver.get("https://portal.recreation.ubc.ca/index.php?r=public/index")
        Logger.normal(f"[{self.username}] Submitting Login Credentials...")
        self.driver.find_element_by_id("inputEmail").send_keys(username)
        self.driver.find_element_by_id("inputPassword").send_keys(password)
        self.driver.find_element_by_id("btn_login").click()
        try:
            global detected, failed
            WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.CLASS_NAME, "table-second-col")))
            Logger.success(f"[{self.username}] Successfully Logged In")
            detected+=1
            ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Failed: {failed}")
            Logger.normal(f"[{self.username}] Bypass Redirect...")
            self.driver.get(get_eventid.url)
            if timed_event == "y":
                Logger.other(f"Sleeping for: {timer.timer(user_time)} second(s)...")
                await asyncio.sleep(timer.timer(user_time))
                await self.cart_hold(delay)
            elif timed_event == "n":
                await self.cart_hold(delay)
            
        except Exception as e:
            Logger.error(f"[{self.username}] Login Error: {e}")
            failed+=1
            ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Failed: {failed}")

        finally:
            await asyncio.sleep(1.5)
            await self.driver.close()
            queue_.get()
            queue_.task_done()

    async def cart_hold(self,delay):
        while True:
            global detected,carted,failed
            self.driver.refresh()
            bmbutton = self.driver.find_element_by_xpath('//*[@id="event-attendees"]/div[3]/div/a').get_attribute('class')
            if bmbutton == "bm-button disabled":
                retry=0
                while retry < 3:
                    Logger.error(f'[{self.username}] Error: Full / Not Opened! Retrying [{retry}]...')
                    failed+1
                    ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Failed: {failed}")
                 
                    Logger.other(f"[{self.username}] Sleeping... [{delay}]")
                    time.sleep(int(delay))
                    Logger.normal(f"[{self.username}] Refreshing...")
                    self.driver.refresh()
                    retry+=1
                else:
                    Logger.error(f'[{self.username}] Error: Full / Not Opened! Terminating [{retry}]')
                    self.driver.quit()
                    return False
            elif bmbutton == "bm-button":
                Logger.success(f"[{self.username}] Successfully Carted!")
                carted+=1
                ctypes.windll.kernel32.SetConsoleTitleW(f"OSCAR BOT {version} | BETA  | Profile(s): {profiles} | Detected: {detected} | Carted: {carted} | Failed: {failed}")
                wh("cart_hold","Success",self.username)
            Logger.other(f"[{self.username}] Sleeping... [{delay}]")
            time.sleep(int(delay))  
#-----------------------------------------------------------------------------------------------   
# ----------------------------------------------------------------------------------------------   
# MENU INTERFACE
if __name__ == '__main__':
    while True:
        print("[1] Checkout Link Mode\n[2] Full Checkout\n[3] Cart Hold\n[4] Settings\n[5] Fetch EventId\n[6] Exit\n")
        selection = input("Input: ")
        print("\n")
        # CHECKOUT LINK
        if selection == "1":
            print("Checkout Link Mode\n")
            eventid = input("Input Event ID: ")
            get_eventid.get_eventid(eventid)
            profile_count()
            timed_event = input("Timed Event? [Y] | [N]: ").lower()
            method = "checkout_link" 
            inits()
            if timed_event == "y":
                user_time = input("Input Time [HH:MM:SS]: ")
                timer.timer(user_time)
                for i in range(profiles):
                    get_profiles(i)
                    TaskModule(username,password,user_sig,cc_num,cc_ccv,cc_strt,cc_city,cc_zip,cc_month,cc_year,cc_name)
                queue_.join()
            elif timed_event == "n":  
                for i in range(profiles):
                    get_profiles(i)
                    TaskModule(username,password,user_sig,cc_num,cc_ccv,cc_strt,cc_city,cc_zip,cc_month,cc_year,cc_name)
                queue_.join()
            else:
                pass

        # CHECKOUT MODE
        elif selection == "2":
            print("Full Checkout Mode\n")
            eventid = input("Input Event ID: ")
            get_eventid.get_eventid(eventid)
            profile_count()
            timed_event = input("Timed Event? [Y] | [N]: ").lower()
            method = "full_checkout" 
            inits()
            if timed_event == "y":
                user_time = input("Input Time [HH:MM:SS]: ")
                timer.timer(user_time)
                for i in range(profiles):
                    get_profiles(i)
                    TaskModule(username,password,user_sig,cc_num,cc_ccv,cc_strt,cc_city,cc_zip,cc_month,cc_year,cc_name)
                queue_.join()
            elif timed_event == "n":  
                for i in range(profiles):
                    get_profiles(i)
                    TaskModule(username,password,user_sig,cc_num,cc_ccv,cc_strt,cc_city,cc_zip,cc_month,cc_year,cc_name)
                queue_.join()
            else:
                pass

        # CART HOLD
        elif selection == "3": 
            print("Cart Hold Mode")
            eventid = input("Input Event ID: ")
            get_eventid.get_eventid(eventid)
            profile_count()
            timed_event = input("Timed Event? [Y] | [N]: ").lower() 
            inits()
            if timed_event == "y":
                user_time = input("Input Time [HH:MM:SS]: ")
                timer.timer(user_time)
                for i in range(profiles):
                    get_profiles(i)
                    CartHold(username,password)
                queue_.join()
              
            if timed_event == "n":
                for i in range(profiles):
                    get_profiles(i)
                    CartHold(username,password)
                queue_.join()

        # VIEW SETTINGS
        elif selection == "4":
            print("View Settings\n")
            setting_list=[]
            with open("./data/settings.json", "r+") as settings:
                data = json.load(settings)
                for index,key in enumerate(data,start=1):
                    setting_list.append(key)
                    print(f"[{index}] {key}: {data[key]}")
                print(f"[{index+1}] Test Webhook\n[{index+2}] Go Back")  
                edit_settings = input("\nInput: ")
                if edit_settings == f'{index-5}':
                    edit_ = input(f"\n{setting_list[index-6]}: ")
                    data[setting_list[index-6]] = int(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)
                elif edit_settings == f'{index-4}':
                    edit_ = input(f"\n{setting_list[index-5]}: ").lower()
                    data[setting_list[index-5]] = bool(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)
                elif edit_settings == f'{index-3}':
                    edit_ = input(f"\n{setting_list[index-4]}: ").lower()
                    data[setting_list[index-4]] = bool(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)
                elif edit_settings == f'{index-2}':
                    edit_ = input(f"\n{setting_list[index-3]}: ")
                    data[setting_list[index-3]] = str(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)
                elif edit_settings == f'{index-1}':
                    edit_ = input(f"\n{setting_list[index-2]}: ")
                    data[setting_list[index-2]] = int(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)    
                elif edit_settings == f'{index}':
                    edit_ = input(f"\n{key}: ")
                    data[setting_list[index-1]] = int(edit_)
                    settings.seek(0)
                    settings.truncate()
                    json.dump(data, settings,indent=4)    
                elif edit_settings == f'{index+1}':
                    with open("./data/settings.json", "r") as settings:
                        data = json.loads(settings.read())
                        wh_ = data['webhook']
                    wh("test_wh","Success","200")
                elif edit_settings == f'{index+2}':
                    continue
                else:
                    pass
        
        # PARSE EVENTID
        elif selection == "5":
            url = input(str("Input URL: "))
            id = re.split('classId=|&occurrenceDate',url)[1]
            print("\n"+id+"\n")
            pass 

        # SYS EXIT
        elif selection == "6":
            print("Exiting...")
            time.sleep(0.1)
            sys.exit()
                 
        else:
            pass