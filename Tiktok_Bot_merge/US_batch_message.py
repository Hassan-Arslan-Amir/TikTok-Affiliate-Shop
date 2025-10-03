import json
import random
import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from random import uniform
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from batch_message_helper import *
from batch_message_xpaths import *
from datetime import datetime
from db_utils import get_cookie_for_shop, insert_cookie, get_processed_users,get_unprocessed_usernames, mark_user_processed, increment_shop_count, get_products_for_shop

with open("c:/Users/Hassan Arslan Amir/Documents/BitBash/First Project/Tiktok_Bot_merge/invite.json", "r", encoding="utf-8") as f:
    invites_data = json.load(f)

def autologin(driver, username, email, password):
    action = ActionChains(driver)
    try:

        email_span = driver.find_element(By.XPATH, "//span[contains(text(), 'Email')]")
        email_span.click()
        emailField = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, loginemailxpath))
        )
        emailField.click()
        clear_input_like_human(emailField)
        print("Typing Email in email field")
        type_like_human(emailField, email)
        time.sleep(uniform(1.5, 2.5))
        if emailField:
            try:
                passwordField = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, loginpswdxpath))
                )
                passwordField.click()
                clear_input_like_human(passwordField)
                print("Typing Password In Password Field")
                time.sleep(uniform(1.5, 2.5))
                type_like_human(passwordField, password)
                time.sleep(uniform(1.5, 2.5))
            except:
                pass
            try:
                loginbtn = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, loginSubmitxpath))
                )
                time.sleep(uniform(1.5, 2.5))
                action.click(loginbtn).perform()
                time.sleep(1)
                captcha = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, loginCaptcha))
                )
                if captcha:
                    input("Please Solve Captcha And Press Enter")
                    otpCode = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.XPATH, otpcodebox))
                    )
                    if otpCode:
                        input("Please Enter the otp code and press enter")
            except:
                pass
    except:
        pass

#---------------------------------- Finding Chrome Driver in the system ------------------------
def find_chrome_driver():
    chrome_exe_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    if os.path.isfile(chrome_exe_path):
        logging.info(f"Found Chrome at: {chrome_exe_path}")
        logging.info("Chrome launched successfully.")
    else:
        logging.error(f"Chrome not found at: {chrome_exe_path}")
        raise FileNotFoundError(f"Chrome executable not found at the specified path: {chrome_exe_path}")

#------------------------------Open Chrome and Log In using Cookies or Manual Login--------------------

def openchrome(username, shop_id, max_retries=2, chrome_driver_path=None):
    logging.basicConfig(level=logging.INFO)
    driver = None

    if not chrome_driver_path:
        try:
            chrome_driver_path = find_chrome_driver()
        except FileNotFoundError as e:
            logging.error(f"{e}")
            raise
    for attempt in range(1, max_retries + 1):
        try:
# ------------- Set up browser options ---
            logging.info(f"Launch attempt {attempt} for shop_id={shop_id}")
            options = Options()
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-ssl-errors")
            options.add_argument("--disable-gpu")
            #service = Service(chrome_driver_path)
            if chrome_driver_path and os.path.isfile(chrome_driver_path):
                service = Service(chrome_driver_path)
                logging.info(f"Using provided chrome driver at: {chrome_driver_path}")
            else:
                service = Service(ChromeDriverManager().install())
                logging.info("Chrome driver path not found, using ChromeDriverManager to install the driver.")

            driver = webdriver.Chrome(service=service, options=options)
            driver.set_window_size(1500, 1000)
            # --- Navigate to TikTok affiliate page ---
            driver.get("https://affiliate-us.tiktok.com/connection/creator?shop_region=US")
            time.sleep(10)
            driver.delete_all_cookies()

# ---------------- Load cookies from DB --------------------------------------#
            cookies = get_cookie_for_shop(shop_id)
            if isinstance(cookies, list) and all(isinstance(c, dict) for c in cookies):
                logging.info("Valid cookies loaded. Adding to browser...")
                for cookie in cookies:
                    try:
                        cookie.pop("storeId", None)
                        cookie.pop("hostOnly", None)
                        cookie.pop("session", None)
                        if "expiry" in cookie:
                            cookie["expiry"] = int(cookie["expiry"])
                        if "sameSite" not in cookie or cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                            cookie["sameSite"] = "None"
                        cookie["domain"] = ".tiktok.com"
                        driver.add_cookie(cookie)
                    except Exception as ce:
                        logging.warning(f"Skipping malformed cookie: {ce}")
# --------------------- Refresh page after cookies -------------------------#
                driver.get("https://affiliate-us.tiktok.com/connection/creator?shop_region=US")
                time.sleep(10)
                logging.info("Cookies added and page refreshed.")
# ------------------------ Validate successful login ----------------------#
                try:
                    WebDriverWait(driver, 20).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Home') or contains(text(),'Dashboard')]")),
                            EC.url_contains("dashboard"),
                            EC.url_contains("affiliate-us.tiktok.com/platform")
                        )
                    )
                    logging.info("Login confirmed via page element.")
                    return driver
                except TimeoutException:
                    if "login" in driver.current_url:
                        logging.warning("Still on login page. Cookies may be invalid.")
                        raise TimeoutException("Login failed after cookie load.")
# --------------------------- Manual login fallback -----------------------------#
            else:
                logging.warning("Cookies not usable, performing manual login...")
                emailData = input("Enter your email: ")
                passwordData = input("Enter your password: ")
                autologin(driver, username, emailData, passwordData)
                cookies = driver.get_cookies()
                insert_cookie(shop_id, cookies)
                time.sleep(random.randint(5, 7))
                return driver  

        except TimeoutException:
            logging.error("Login failed. Element not found.")
        except Exception as e:
            logging.error(f"Attempt {attempt} failed with error: {e}")
            if driver:
                driver.quit()
                logging.info(" Cleaned up browser session.")

    logging.critical("All login attempts failed.")
    raise RuntimeError("Failed to login or apply cookies after retries.")



def automationstep(driver):
    print("Start Automation...")
    # action = ActionChains(driver)
    try:
        findCreators = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Creator messages']")
            )
        )
        print(findCreators)
        findCreators.click()
        time.sleep(uniform(5, 7))
    except:
        print("test values")
        findCreators = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Creator Messages']")
            )
        )
        print(findCreators)
        findCreators.click()
        time.sleep(uniform(5, 7))
    handlefindcreatorpopup(driver)

def handlechatpopup(driver):
    print("Handling Chat Popup")
    action = ActionChains(driver)
    try:
        xpath1 = "//button[contains(@class, 'arco-btn') and contains(@class, 'arco-btn-primary') and contains(@class, 'arco-btn-size-large') and contains(@class, 'arco-btn-shape-square')]/span[text()='Check rules']"

        try:
            # Wait for the element to be present and clickable
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath1))
            )
            # Click the button
            button.click()
        except Exception as e:
            pass
        try:
            skipbtn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, dashBoardSkip))
            )
            action.move_to_element(skipbtn).click().perform()
            print("Skip button clicked")

        except:
            pass
        # time.sleep(3)
        try:
            okbtn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, chatOK))
            )
            action.move_to_element(okbtn).click().perform()
            print("OK button clicked")
        except:
            pass
        # time.sleep(2)
        try:
            crossicon = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, chatcrossicon))
            )
            action.move_to_element(crossicon).click().perform()
            print("Cross icon clicked")
        except:
            pass
        # time.sleep(2)
        try:
            gotit_1 = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, dashBoardGotIt))
            )
            action.move_to_element(gotit_1).click().perform()
            print("Got it button clicked")
        except:
            pass
        xpath1 = "//button[contains(@class, 'arco-btn') and contains(@class, 'arco-btn-primary') and contains(@class, 'arco-btn-size-large') and contains(@class, 'arco-btn-shape-square')]/span[text()='Check rules']"

        try:
            # Wait for the element to be present and clickable
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath1))
            )
            # Click the button
            button.click()
        except Exception as e:
            pass

    except:
        print("Error in handlechatpopup")

def process_product_and_send(
    driver,
    productstatus,
    sidebarelements,
    cardInputXpath,
    sendproduct,
    messageArea1,
    messageArea2,
    messageData1,
    cardName,
):
    try:
        if productstatus == 1:
            # Handle sidebar interaction
            try:
                print("line 288: not Max")
                productbtn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, sidebarelements))
                )
                action = ActionChains(driver)
                action.move_to_element(productbtn).perform()
                time.sleep(1)
                productbtn.click()
                time.sleep(2)
                logging.info("Clicked on Sidebar")
            except Exception as e:
                logging.error(f"Error clicking sidebar: {e}")
                time.sleep(2)
                productbtn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, sidebarelements))
                )
                action.move_to_element(productbtn).perform()
                time.sleep(1)
                productbtn.click()
                time.sleep(2)
                logging.info("Clicked on Sidebar (Retry)")
            # Handle dropdown interaction
            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//span[@class="arco-select-view-value" and text()="Name"]',
                        )
                    )
                )
                action.move_to_element(dropdown).perform()
                time.sleep(1)
                dropdown.click()
                time.sleep(2)
                dropdownid = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//li[@class="arco-select-option m4b-select-option"]',
                        )
                    )
                )
                action.move_to_element(dropdownid).perform()
                time.sleep(1)
                dropdownid.click()
                time.sleep(2)
                logging.info("Searching Card")
            except Exception as e:
                logging.error(f"Error with dropdown: {e}")
                return 2

            # Handle card input and send process
            try:
                cardInputData = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, cardInputXpath))
                )
                cardInputData.click()
                time.sleep(2)

                if cardInputData.get_attribute("value"):
                    action.move_to_element(cardInputData).perform()
                    action.key_down(Keys.CONTROL).send_keys("a").key_up(
                        Keys.CONTROL
                    ).send_keys(Keys.BACKSPACE).perform()
                    time.sleep(1)

                print(cardName)
                cardInputData.send_keys(cardName)
                time.sleep(1)
                cardInputData.send_keys(Keys.ENTER)
                time.sleep(3)

                for _ in range(3):
                    logging.info("Finding Product Card and sending")
                    Card = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@data-e2e='ee7482a9-a8f4-7400']")
                        )
                    )
                    if Card:
                        action.move_to_element(Card).perform()
                        sendbutton = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, sendproduct))
                        )
                        sendbutton.click()
                        logging.info("Sent product card")
                        time.sleep(2)
                        break
                    else:
                        logging.info("Retrying....")
                        time.sleep(2)

            except Exception as e:
                logging.error(f"Error adding product card: {e}")
                for _ in range(3):
                    logging.info("Retrying to find and send Product Card")
                    Card = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@data-e2e='ee7482a9-a8f4-7400']")
                        )
                    )
                    if Card:
                        action.move_to_element(Card).perform()
                        sendbutton = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, sendproduct))
                        )
                        sendbutton.click()
                        logging.info("Sent product card")
                        time.sleep(2)
                        break
                    else:
                        logging.info("Retrying....")
                        time.sleep(2)

    except Exception as e:
        logging.error(f"Error in product processing: {e}")

    # Handle message sending
    try:
        for _ in range(2):
            try:
                logging.info("In message section")
                messageArea = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, messageArea1))
                )
                time.sleep(uniform(2, 4))
                messageArea.click()
                logging.info("Clicked on message area")

                script = "document.querySelector('textarea').value += arguments[0];"
                driver.execute_script(script, messageData1)
                time.sleep(uniform(0.8, 1))
                messageArea.send_keys(Keys.ENTER)
                time.sleep(2)
                logging.info("Message sent")
                return 1

            except Exception as e:
                logging.warning(f"Error with message area1: {e}")
                messageArea = WebDriverWait(driver, 150).until(
                    EC.presence_of_element_located((By.XPATH, messageArea2))
                )
                time.sleep(uniform(1, 2))
                messageArea.click()
                time.sleep(uniform(1, 2))
                logging.info("Typing in text area")
                type_like_human(driver, messageData1)
                time.sleep(uniform(1, 2))
                return 1

    except Exception as e:
        logging.error(f"Error in sending messages: {e}")
        time.sleep(1)
        return True

def handle_popup_only_when_occur(driver):
    try:
        close_icons = driver.find_elements(
            By.XPATH, "//span[contains(@class, 'arco-modal-close-icon')]"
        )
        if close_icons:
            logging.info("Popup detected. Invoking handler...")
            handleHomepopup(driver)
        else:
            logging.info("No popup detected.")
    except Exception as e:
        logging.error(f"Error while checking for or handling popup: {e}")


def mainfunction(
    email,
    password,
    profile_name,
    follow,
    productstatus,
    limit,
    message,
    byusername,
    filterdata,
    usernameaccount,
    skipduplication,
    title,
    shop_id,
):
    #  time.sleep(100)
    #  start_endpoint = profile_doc.update("start_endpoint")
    while True:
        count = 0
        try:
            try:
                driver=openchrome(title, shop_id)
                # driver = openchrome(driver, shop_id, email, password, filterdata)
                current_url = driver.current_url
                expected_url = (
                    "https://affiliate-us.tiktok.com/connection/creator?shop_region=US"
                )
                if current_url.startswith(expected_url):
                    logging.info("Successfully logged in and on correct URL.")
                else:
                    logging.warning("Unexpected URL after login:", current_url)
            except Exception as e:
                logging.error("Login or cookie injection failed:", e)

            handle_popup_only_when_occur(driver)
            #    try:
            #        automationstep(driver)
            #    except:
            #        pass
            start_time = datetime.now()
            logging.info(f"First iteration started at {start_time}")
            # 🔁 LOAD USERS FROM DATABASE
            saved_users_from_founduser_file = get_processed_users(shop_id)
            #print("Users loaded:", saved_users_from_founduser_file)

            if not saved_users_from_founduser_file:
                    logging.info("No new users to message after filtering.")
                    driver.quit()
                    return

            action = ActionChains(driver)

            for user in saved_users_from_founduser_file:
                #   count=count+1
                if count == 20: # users number to be fetched from the database for process
                    driver.get(
                        "https://affiliate-us.tiktok.com/connection/creator-management?shop_region=US"
                    )
                    try:
                        handle_popup_only_when_occur(driver)
                    except:
                        logging.warning("Error handling creator management popup")
                    #               message= '''
                    # VIRAL CANDIDA GUT CLEANSE - 25% commission \n🚨Huge Opportunity🚨\nWe want YOU to be the next viral affiliate with our brand. \nOur top affiliate has made $25,050 in commissions on ONLY 6 videos!\nI think you would be a PERFECT fit for this product and I see the potential for you to go viral. \nWe will provide you with as many resources as we can and help you along the way. Please request a free sample from the product card so we can get started ASAP!
                    # '''

                    sendbatch(driver, message, title, shop_id)
                    count = 0
                    logging.info("Removing creators from list")
                    #driver.quit()
                    #time.sleep(1)
                    for i in range(20):
                        try:
                            remove_creators(driver)
                        except:
                            logging.info("✅ Creator removed (or already gone)")

                    driver.get(
                        "https://affiliate-us.tiktok.com/connection/creator?shop_region=US"
                    )
                    try:
                        handle_popup_only_when_occur(driver)
                    except:
                        pass
                #   sendbatch(driver,"hello",1234567,"title")
                #   driver.quit()
                #   break
                logging.info(f"Processing user: {user}")
                try:
                    try:
                        check = automationStepsforfindusernames(driver, user)
                        if check == 1:
                            count += 1
                            try_solving_slider_captcha(driver, action)
                            #del_usernames(shop_id, user)
                            #mark_user_processed(shop_id, user)
                            increment_shop_count(shop_id)
                            logging.info(f"{user} marked as processed and deleted from pending list.")
                        else:
                            logging.warning("Couldn't click on user")
                    except Exception as e:
                        logging.error("Error messaging user:", user, e)

                    end_time = datetime.now()
                    duration = end_time - start_time
                    logging.info(f"Iteration ended at {end_time}, duration: {duration}")
                #               message= '''
                # VIRAL CANDIDA GUT CLEANSE - 25% commission \n🚨Huge Opportunity🚨\nWe want YOU to be the next viral affiliate with our brand. \nOur top affiliate has made $25,050 in commissions on ONLY 6 videos!\nI think you would be a PERFECT fit for this product and I see the potential for you to go viral. \nWe will provide you with as many resources as we can and help you along the way. Please request a free sample from the product card so we can get started ASAP!
                # '''
                #   sendbatch(driver,message,1234567,"VIRAL CANDIDA GUT CLEANSE - 25% commission ")
                except:
                    logging.info("Added")
            driver.quit()
        except Exception as e:
            logging.error("Bot crashed due to error:", e)
            driver.quit()


def remove_creators(driver):
    try:
        time.sleep(1)
        # Step 1: Click the 3-dot dropdown menu
        try:
            batch_button1 = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "(//button[@data-tid='m4b_dropdown_button' and contains(@class, 'arco-btn-text')])[1]"
                ))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", batch_button1)
            batch_button1.click()
            logging.info("Clicked 3-dot menu")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Failed to click 3-dot menu: {e}")
            return

        # Step 2: Click "Remove" from dropdown
        try:
            batch_button2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//div[contains(@class,'arco-dropdown-menu')]//div[@role='menuitem' and text()='Remove']"
                ))
            )
            batch_button2.click()
            logging.info("Clicked 'Remove' from dropdown")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Failed to click 'Remove' from dropdown: {e}")
            return

        # Step 3: Confirm removal in dialog
        try:
            batch_button3 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@class='arco-btn arco-btn-primary arco-btn-size-large arco-btn-shape-square']//span[text()='Remove']"
                ))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", batch_button3)
            batch_button3.click()
            logging.info("Confirmed removal")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Failed to confirm removal: {e}")
            return

        time.sleep(1)
        logging.info("Creators removed successfully.")

    except Exception as e:
        logging.error(f"General exception in remove_creators: {e}")

def sendbatch(driver, message, title, shop_id):
    try:
        time.sleep(5)
        #for i in range(3):
#------------------------ Fetch product data from DB
        products = get_products_for_shop(shop_id)
        if not products:
            logging.warning(f"No products found for shop ID: {shop_id}")
            return
# -------------------------Step 1: Click "Batch message" button
        try:
            batch_button1 = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//button[@id="crm_batch_im"]//span[text()="Batch message"]'))
                    )
            batch_button1.click()
            logging.info("Btach Button Clicked")
        except:
            logging.warning("Batch message button not clicked on attempt:")

        logging.info("Moving to checkbox")
        time.sleep(5)
#------------------------- Step 2: Select main checkbox
        action = ActionChains(driver)
        checkbox = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'arco-table-th-item')]//label[contains(@class, 'arco-checkbox')]//input[@type='checkbox']")
                )
            )
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)
#------------------------- Step 3: Click "Batch message" confirm button
        batch_message_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//button[@data-tid='m4b_button' and @data-e2e='837e365f-24f2-d052' and contains(@class, 'arco-btn-primary') and contains(@class, 'arco-btn-size-default') and contains(@class, 'arco-btn-shape-square') and contains(@class, 'm4b-button') and contains(@class, 'mx-16')]",
                    )
                )
            )
        logging.info("Clicking batch message button...")
        driver.execute_script("arguments[0].scrollIntoView(true);", batch_message_button)
        driver.execute_script("arguments[0].click();", batch_message_button)
        time.sleep(1)
#------------------------ Step 4: Click "Add product" button
        for productid, _ in products:  # Only using productid for now
            logging.info(f"Processing product ID: {productid}")
            if productid == products[0][0]:  # first product
                add_product_xpath = "//button[@data-tid='m4b_button' and @data-e2e='5b7c3496-6daf-d90c' and text()='Add product']"
            else:  # subsequent products
                add_product_xpath = "//button[@data-tid='m4b_button' and @data-e2e='eac967c9-98cb-9572' and contains(text(),'Add products')]"
            add_product_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,add_product_xpath
                    )
                )
            )
            logging.info("Add product dialog found")
            time.sleep(1)
            add_product_button.click()
            time.sleep(1)
#------------------------- Step 5: Select "Product ID" from dropdown
            dropdown_button_3 = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//span[@class="arco-select-view-value" and text()="Product name"]',
                        )
                    )
                )
            driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button_3)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", dropdown_button_3)
            logging.info("Product name dropdown clicked")
            dropdown_button_4 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//li[@role="option" and @class="arco-select-option m4b-select-option" and text()="Product ID"]',
                        )
                    )
                )
            dropdown_button_4.click()
            time.sleep(1)
            logging.info(f"Searching for product ID: {productid}")
#---------------------- Step 6: Input product ID and submit
            card_input_data = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//input[@data-tid="m4b_input_search" and @placeholder="Search by product ID"]',
                        )
                    )
                )

            card_input_data.click()
            type_like_human(card_input_data, productid)
            card_input_data.send_keys(Keys.ENTER)
            logging.info(f"Entered and submitted product ID: {productid}")
#--------------------- Step 7: Select the matching product checkbox
            checkbox_selector = "//label[@data-tid='m4b_checkbox' and contains(@class, 'arco-checkbox')]/input[@type='checkbox']"
            checkbox = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, checkbox_selector))
                    )
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            time.sleep(1) 
            driver.execute_script("arguments[0].click();", checkbox)
            logging.info("Product checkbox found and clicked.")
#--------------------- Step 8: Clicking the add button
            try:
                time.sleep(1)
                add_button = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//button[span/text()="Add"]'))
                )
                add_button.click()

            except Exception as e:
                logging.error("Error clicking Add button:", e)

    except Exception as e:
            logging.error(f"Error in sendbatch (product section): {e}")
#------------------------ Handling the second input for adding a message
    try:
        title_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                "//input[@placeholder='Write a concise title that captures the essence of your message.']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", title_input)
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, -150);")
        driver.execute_script("arguments[0].focus();", title_input)
        clear_input_like_human(title_input)
        type_like_human(title_input, title)  # No fancy send_keys logic
        logging.info(f"Entered title: {title}")
    except Exception as e:
        logging.error(f"Failed to enter title: {e}")
    # Handling the dropdown buttons for message body
    try:
        dropdown_btn_66 = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//textarea[@placeholder='You could start with an introduction, explain the details of the collaboration, and end with an invitation to talk more.']",
                )
            )
        )
        dropdown_btn_77 = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//textarea[@placeholder='You could start with an introduction, explain the details of the collaboration, and end with an invitation to talk more.']",
                )
            )
        )

        if dropdown_btn_66:
            try:
                dropdown_btn_66.click()
                clear_input_like_human(dropdown_btn_66)
                type_like_human(dropdown_btn_66, message)
            except:
                dropdown_btn_66[0].click()
        elif dropdown_btn_77:
            try:
                dropdown_btn_77.click()
                time.sleep(1)
                script = "document.querySelector('textarea').value += arguments[0];"
                driver.execute_script(script, message)
                dropdown_btn_77.send_keys("a")
                time.sleep(uniform(1, 3))
                dropdown_btn_77.send_keys(Keys.BACK_SPACE)
                time.sleep(2)
            except:
                dropdown_btn_77[0].click()
        else:
            logging.warning("Neither dropdown button found.")
    except Exception as e:
        logging.error(f"Error entering message body: {e}")
#------------------------- Handling the final send message button
    try:
        time.sleep(1)
        send_message_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@data-tid='m4b_button' and @data-e2e='7c807b3b-fcf4-6c97' and text()='Send message']",
                )
            )
        )
        try:
            send_message_button.click()
        except:
            send_message_button[0].click()
    except:
        logging.warning("Error occurred while clicking Send message button")
    try:
        time.sleep(1)
        send_message_button1 = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@class='arco-btn arco-btn-primary arco-btn-size-large arco-btn-shape-square' and @type='button']/span[text()='Send']",
                )
            )
        )
        try:

            send_message_button1.click()
        except:

            send_message_button1[0].click()
        time.sleep(5)
        try:
            send_message_button12 = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//button[contains(., 'OK')]",
                    )
                )
            )
            try:

                send_message_button12.click()
            except:

                send_message_button12[0].click()
        except:
            pass
        time.sleep(15)
    except:
        logging.error("Error occurred while clicking Send message button")

def automationStepsforfindusernames(driver, name):
    from time import time
    firstusername = f"//div[@class='arco-menu-inner']//div[@class='arco-menu-group m4b-dropdown-menu-item-group']//div[@class='flex py-8 rounded-4']//span[@class='leading-20 text-body-m-medium']/span[.='{name}']"
    # firstuser_gmv = "(//span[contains(text(), '$')])[1]"
    # print(firstusername)
    start=time()
    try:
        action = ActionChains(driver)
        print("Looking for search input box...")
        searchUser = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, searchBox))
        )
        logging.info("Search input box found!")
        driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            searchUser,
        )
        logging.info("Scrolled to search input.")
        searchUser.click()
        logging.info("Clicked on the search input.")

        input_value = searchUser.get_attribute("value")
        logging.info(f"Current value in search box: '{input_value}'")

        if input_value:
            logging.info("Clearing old input...")
            clear_input_like_human(searchUser)

        userName = name
        logging.info(f"Typing '{userName}' into the search box...")
        type_like_human(searchUser, userName)

        # time.sleep(2)
        logging.info("Pressing Enter...")
        searchUser.send_keys(Keys.ENTER)
        
        #time.sleep(3)

        userfound = f"//tr[contains(@class, 'cursor-pointer')]//span[contains(@class, 'text-body-m-medium') and text()='{name}']/ancestor::tr//button[@data-tid='m4b_button' and @data-e2e='d610879c-a3e6-6f81']"
        logging.info(f"Waiting for action button for user '{name}'...")
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, userfound))
        )
        logging.info(f"Clicking the button for '{name}'...")
        button.click()
        logging.info(f"Clicked on '{name}' in {round(time() - start, 2)}s")
        return 1
    except Exception as e:
        logging.warning("Error during automation:")
        logging.warning(f"    - Step: {e.__class__.__name__}")
        logging.warning(f"    - Message: {e}")
        logging.warning(f"    - Failed while trying to click or type into the search bar or button for '{name}'")
        return 0

def run_mainfunction_periodically(
    email,
    password,
    username,
    follow,
    productstatus,
    limit,
    message,
    byusername,
    filterdata,
    usernameaccount,
    skipduplication,
    title,
    shop_id
):
    # start_time = time.time()
    # interval_seconds = interval_minutes * 60
    # run_duration_seconds = run_duration_minutes * 60

    # while (time.time() - start_time) < run_duration_seconds:
    mainfunction(
        email,
        password,
        username,
        follow,
        productstatus,
        limit,
        message,
        byusername,
        filterdata,
        usernameaccount,
        skipduplication,
        title,
        shop_id
    )
    # time.sleep(interval_seconds)  # Wait for the specified interval before running again

