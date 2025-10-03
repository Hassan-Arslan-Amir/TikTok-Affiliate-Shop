from utils import *
from xpaths import *
from helper import *
from db_utils import get_cookie_for_shop, insert_cookie

def openchrome(username):
    cookies_available = False 
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)  
        # driver.maximize_window()
        time.sleep(1)
        driver.get("https://affiliate-us.tiktok.com/platform/homepage?shop_region=US")
        time.sleep(10)
        cookies = get_cookie_for_shop(username)
        if cookies:
            cookies_available=True
        else:
            print ("No cookies present")

        if cookies_available:
            print("Page loaded. Adding cookies to the browser session...")
            for cookie in cookies:
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                if 'sameSite' not in cookie or cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                    cookie['sameSite'] = 'None'  
                cookie['domain'] = '.tiktok.com'
                driver.add_cookie(cookie)
            print("Cookies added successfully.")
            time.sleep(2)
            driver.refresh()
            print("Page refreshed after adding cookies.")
            time.sleep(random.randint(5, 7))
        print("Browser should now be fully operational.")
        return driver
    except Exception as e:
        print(f"An error occurred: {e}")
        if driver is not None:  
            driver.quit()
        raise

username="SAP"

driver = openchrome(username)