from utils import *
from xpaths import *
from helper import *
from datetime import datetime 
from selenium.webdriver.chrome.options import Options
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_utils import (
    fetch_shop_by_name, get_unprocessed_usernames, get_cookie_for_shop, get_products_for_shop, get_invite_details_from_db, insert_cookie,get_products_for_shop, increment_count
)
if len(sys.argv) < 2:
    print("Please provide a shop name.")
    sys.exit()

#----------------------------- Finding the Chrome from the system---------------------

def find_chrome_driver():
    # Path to the Chrome executable
    chrome_exe_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # Check if Chrome exists at the specified location
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
            #service = Service(ChromeDriverManager().install())
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
            driver.get("https://affiliate.tiktok.com/platform/homepage?shop_region=GB")
            time.sleep(random.randint(10, 13))
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
                driver.get("https://affiliate.tiktok.com/platform/homepage?shop_region=GB")
                time.sleep(random.randint(10, 13))
                logging.info("Cookies added and page refreshed.")
# ------------------------ Validate successful login ----------------------#
                try:
                    WebDriverWait(driver, random.randint(20, 25)).until(
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
                logging.info("Cleaned up browser session.")

    logging.critical("All login attempts failed.")
    raise RuntimeError("Failed to login or apply cookies after retries.")

#---------------------------- Getting the number of overlapping Creators-------------------

def get_overlap_count(driver):
    print("Into Overlap function")

    try:
        # Locate the span element that contains the overlap creators' information
        #overlap_text_element = driver.find_element(By.XPATH, "//span[contains(@class, 'text-head-l') and contains(text(), 'invited to collaborate')]")
        overlap_text_element = WebDriverWait(driver, random.randint(20, 25)).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'flex') and contains(@class, 'items-center')]//span[contains(@class, 'text-head-l') and contains(@class, 'text-neutral-text1') and contains(text(), 'invited to collaborate')]")
            )
        )# Extract the text from the element
        overlap_text = overlap_text_element.text.strip()  # Remove extra spaces or newline characters
        print(f"Overlap value = '{overlap_text}'")  # Print to see if there's unexpected formatting
        
        # Use regular expression to find the number in the text
        match = re.search(r'(\d+)', overlap_text)
        
        if match:
            overlap_count = int(match.group(1))  # Return the extracted number as an integer
            print(f"Overlap_count = {overlap_count}")
            return overlap_count
        else:
            print("No number found in overlap text.")
            return 0  # Return 0 if no match is found
    except Exception as e:
        print(f"Error extracting overlap count: {e}")
        return 0  # 

#-------------------------Main Function------------------------------------#
def run_bot_uk():
    print("Running the UK Bot...")
    shop_id = sys.argv[1].strip()
    selected_shop = fetch_shop_by_name(shop_id)

    if not selected_shop:
        print("No shop found with type 'target write' or 'open colab'.")
        exit()
#------------- Set bot_choice based on type
    shop_type = selected_shop['type'].lower()
    if shop_type == 'target write':
        bot_choice = "1"
    elif shop_type == 'open colab':
        bot_choice = "2"
    else:
        print("Unsupported shop type:", shop_type)
        exit()

    selected_key = selected_shop['name']
    selected_data = selected_shop
#------------ In case of open collab
    if bot_choice == "2":
        import traceback
        from UK_batch_message import run_mainfunction_periodically
        try:
            if shop_type == "open colab":
#---------------- Fetch from DB using name
                selected_data = fetch_shop_by_name(shop_id)
                if not selected_data:
                    raise ValueError(f"No shop data found in database for: {shop_id}")  
            else:
                selected_data = selected_shop

            print("Running for shop:", selected_data["name"])
            print("Selected data keys:", selected_data.keys())
            print("Selected data content:", selected_data)

            run_mainfunction_periodically(
                selected_data["email"],
                "hundret333@!",  # Use hardcoded password for now (testing)
                selected_data["name"],  # username
                0,  # follow
                1,  # productstatus
                0,  # limit
                selected_data["message"],
                "byusername",
                "filterdata",
                "usernameaccount",
                1,  # skipduplication
                selected_data["name"],  # using shop type as title
                selected_data["id"]
            )

        except Exception as e:
            print(f"Failed to start batch message bot: {e}")
            traceback.print_exc()
            exit()

        exit()
#------------------- In case of target collab  
    elif bot_choice == "1":  
        print("Running Target Invite Bot with:", selected_key)
    else:
        print("Invalid choice. Please enter a valid number.")

    csv_module = "1"
    runtype = ""
    if csv_module in ["1", "2"]:
        if csv_module == "1":
            runtype = "csv"
        else:
            runtype = "scroll"
            scrape_users = input(
                f"How many user You want to Scrape Maximum Users 1000 and Minimum 10\n"
            )
        print("You Selected", csv_module)
    else:
        print("Wrong Input")

    username = selected_key # shop name
    shop_id = selected_data["id"] # from database shop record
    freesamplefun = False
    while True:
        freesamplereq = "1"
        if freesamplereq in ["1", "2"]:
            if freesamplereq == "1":
                state = "1"
                freesamplefun = True
            break
        else:
            print("Please select only 1 or 2.")
    usernames = get_unprocessed_usernames(shop_id)
    if not usernames:
        print("No unprocessed users found in database. Please add more users.")
        exit()
    else:
        print(f"Found {len(usernames)} unprocessed users in the database for shop: {username}")
#----------------------------- Open the driver 
    scrape_check = True
    count1 = 0
    user_count = 0
    while True:
        driver=None
        try:
            driver = openchrome(username, shop_id)
            print("WebDriver launched successfully.")
            print("Browser should now be fully operational.")
            handleHomepopup(driver)
            time.sleep(random.randint(2, 4))
        except FileNotFoundError as e:
            print(f"{e}. Terminating the process.")
            exit(1)  # Immediately exit the script, or you can choose other clean-up logic here.
        except Exception as e:
            print(f"An error occurred: {e}. Please check your internet or cookies.")
            exit(1)
        try :
            while True:
                start_time = datetime.now()
                print(f"Iteration {count1 + 1} started at {start_time.strftime('%H:%M:%S')}")
                invitesend = True
                if count1 == 550:
                    break
                try:
                    action = ActionChains(driver)
                    # print("Browser should now be fully operational.")
                    # handleHomepopup(driver)
                    driver.get(
                        "https://affiliate.tiktok.com/connection/target-invitation?shop_region=GB&tab=1"
                    )
                    original_tab=driver.current_window_handle
        #-------------------------- Finding the creator
                    print("Now Start Save Creator Process")
                    if runtype == "csv":
                        time.sleep(random.randint(5, 7))
                        try:
                            handlefindcreatorpopup(driver)
                            time.sleep(random.randint(1, 3))
                        except:
                            pass
                        time.sleep(random.randint(1, 3))
                        colabtbn = WebDriverWait(driver, random.randint(10, 13)).until(
                            EC.presence_of_element_located((By.XPATH, colabbtn_xpath))
                        )
                        action.move_to_element(colabtbn).perform()
                        colabtbn.click()
                        time.sleep(random.randint(2, 5))
                        try:
                            create_invitation_btn = WebDriverWait(driver, random.randint(10, 13)).until(
                                EC.presence_of_element_located((By.XPATH, create_invitation_btn_xpath))
                            )
                            action.move_to_element(create_invitation_btn).perform()
                            create_invitation_btn.click()
                            print("Create invitation button is clicked.")
                            time.sleep(random.randint(2, 5))
                        except:
                            pass

        #----------------------------- Adding Products -------------------------------------#

                        try:
                            choseproductbtn = WebDriverWait(driver, random.randint(15, 18)).until(
                                EC.presence_of_element_located((By.XPATH, choseproduct_xpath))
                            )
                            action.move_to_element(choseproductbtn).perform()
                            choseproductbtn.click()
                            time.sleep(random.randint(1, 3))
                        except:
                            print("Not CLicked on the Add product button")

                        print(f"Loading product list from DB for shop_id: {shop_id}")
                        productlist = get_products_for_shop(shop_id)
                        time.sleep(random.randint(1, 3))
                        add_products_with_commission(driver, action, productlist, addproduct_xpath, addproduct2_xpath, ADDBTN_xpath, commsioninput_xpath)
                        print("Products added successfully.")
                        time.sleep(random.randint(1, 3))

        #-------------------------------------- Free sample option handling -------------------------------------------

                        print("Into Free Sample Option Handling")
                        print(f"freesamplefun before check: {freesamplefun}")
                        try:
                            #if freesamplefun:
                            time.sleep(random.randint(5,7))
                            handle_free_sample_option(driver, action, setupfresample_xpath, state, autobtn_xpath, okbtn_xpath)
                        except Exception as e:
                            print(f"Free sample option handling failed: {e}")
                            #print("Sample NOt Added ", e)
                        time.sleep(random.uniform(1, 3))

        #--------------------------------------------------------------------------------#
                        try:
                            # choseproductbtn = WebDriverWait(driver, 10).until(
                            #     EC.presence_of_element_located((By.XPATH, choseproduct_xpath))
                            # )
                            # action.move_to_element(choseproductbtn).perform()
                            # choseproductbtn.click()
                            # time.sleep(1)
                            # action.send_keys(Keys.PAGE_UP).perform()
                            time.sleep(random.randint(2, 4))
                            print("Click on Choose Creators")
                            xpathforchoorcreator = f'//div[text()="Choose creators"]'
                            colabtbn = WebDriverWait(driver, random.randint(20, 23)).until(
                                EC.presence_of_element_located((By.XPATH, xpathforchoorcreator))
                            )
                            action.move_to_element(colabtbn).perform()
                            colabtbn.click()
                        except:
                            print("Not Clicked")
                            print("Click on Choose Creators")
                            xpathforchoorcreator = f'//div[text()="Select creators"]'
                            colabtbn = WebDriverWait(driver, random.randint(20, 23)).until(
                                EC.presence_of_element_located((By.XPATH, xpathforchoorcreator))
                            )
                            action.move_to_element(colabtbn).perform()
                            time.sleep(random.randint(2, 5))
                            pass
                        print("after choose creators")
                        existing_users = []
                        try:
                            existing_users = get_unprocessed_usernames(shop_id)
                        except:
                            pass
                        namelist = []
                        try:
                            namelist = existing_users
                        except:
                            pass
                        print("Total Users: ", len(namelist))
                        if len(namelist) == 0:
                            driver.quit()
                            break
                        try:
                            print("in save creator mode")
                            savecreator(driver, namelist, shop_id)
                            user_count = user_count + 50
                        except Exception as e:
                            print(f"Error in save creator mode: {e}")
                            if "No users were selected" in str(e):
                                print("No users were selected, likely all users have been processed.")
                                driver.quit()
                                break
                            else:
                                print("Running Again")
                    else:
                        try:
                            findcreatorbtn = WebDriverWait(driver, random.randint(10, 13)).until(
                                EC.presence_of_element_located((By.XPATH, findcreator_xpath))
                            )
                            action.move_to_element(findcreatorbtn).click().perform()
                            time.sleep(random.randint(5, 7))
                            handlefindcreatorpopup(driver)
                        except Exception as e:
                            logging.error(f"Failed to click Find Creator: {e}")

                        if scrape_check:
                            try:
                                scroll_and_get_user(driver, username, scrape_users)
                                scrape_check = False
                            except Exception as e:
                                logging.warning(f"Failed to scrape users: {e}")
                        print("Time to save creators")

                        try:
                            existing_users = get_unprocessed_usernames(shop_id)
                        except Exception as e:
                            logging.error(f"Failed to fetch unprocessed users: {e}")
                            existing_users = []

                        if len(existing_users) == 0:
                            print("No unprocessed users found. Exiting")
                            driver.quit()
                            break
                        print(existing_users, "Existing Users")

                        try:
                            findcreatorbtn = WebDriverWait(driver, random.randint(5, 7)).until(
                                EC.presence_of_element_located((By.XPATH, invitation_xpath))
                            )
                            action.move_to_element(findcreatorbtn).click().perform()
                            time.sleep(random.randint(5, 7))
                            handlefindcreatorpopup(driver)
                            time.sleep(random.uniform(0.5, 1.5))
                        except Exception as e:
                            logging.warning(f"Error opening invitation tab: {e}")
        #----------------------------------------Open collaboration interface------------------------------#             
                        try:
                            colabtbn = WebDriverWait(driver, random.randint(10, 13)).until(
                                EC.presence_of_element_located((By.XPATH, colabbtn_xpath))
                            )
                            action.move_to_element(colabtbn).perform()
                            #time.sleep(0.5)
                            colabtbn.click()
                        except Exception as e:
                            logging.error(f" Failed to open collaboration panel: {e}")
        #---------------------------------------------------------------------------------#
                    print("Choose Creators Successfully")
                    try:
                        xpathforchoorcreator = f'//div[text()="Choose creators"]'
                        colabtbn = WebDriverWait(driver, random.randint(20, 23)).until(
                            EC.presence_of_element_located((By.XPATH, xpathforchoorcreator))
                        )
                        action.move_to_element(colabtbn).perform()
                        colabtbn.click()
                    except:
                        print("Not Clicked")
                    print("Now Start Add Product Process")
                    creators_deleted = False

        # #-------------------------------------- Free sample option handling -------------------------------------------

        #             print("Into Free Sample Option Handling")
        #             print(f"freesamplefun before check: {freesamplefun}")
        #             try:
        #                 #if freesamplefun:
        #                 time.sleep(random.randint(5,7))
        #                 handle_free_sample_option(driver, action, setupfresample_xpath, state, autobtn_xpath, okbtn_xpath)
        #             except Exception as e:
        #                 print(f"Free sample option handling failed: {e}")
        #                 #print("Sample NOt Added ", e)
        #             time.sleep(random.uniform(1, 3))

        #-------------------------------------------------------------------------------------------------#  
                    
                    print("Now Start Create Invitaion")
                    createinvitebtn = WebDriverWait(driver, random.randint(10, 13)).until(
                        EC.presence_of_element_located((By.XPATH, createinvitation_xpath))
                    )
                    action.move_to_element(createinvitebtn).perform()
                    createinvitebtn.click()
                    time.sleep(random.uniform(2, 4))
                    invite_status = True
                    try:
                        invitation_name, email_address, phone_number, message, valid_until = get_invite_details_from_db(shop_id)
                        logging.info(f"Invite details loaded: Name={invitation_name}, Email={email_address}")
        #----------- Remove country code from phone number (e.g., '+1 222222' → '222222')
                        parts = phone_number.split(' ', 1) 
                        if len(parts) == 2:
                            country_code = parts[0]       
                            stripped_phone = parts[1]     
                        else:
                            country_code = ""
                            stripped_phone = phone_number  
                        print("Country code:", country_code)
                        print("Phone number:", stripped_phone)
                        phone_xpath = '//input[@placeholder="Please enter a WhatsApp account number"]'
                        createinvite(
                            driver,
                            action,
                            invitation_name,
                            email_address,
                            stripped_phone,
                            message,
                            valid_until,
                            phone_xpath,
                        )
                        time.sleep(random.uniform(1, 3))
                    except Exception as e:
                        logging.warning(f" No invite data found or error occurred: {e}")

                    if invite_status:
                        try:
        #------------------ Step 1: Click Send
                            sendbtn = WebDriverWait(driver, random.randint(10, 13)).until(
                                EC.element_to_be_clickable((By.XPATH, sendbtn_xpath))
                            )
                            print("Send button found")
                            action.move_to_element(sendbtn).perform()
                            time.sleep(random.uniform(1, 3))
                            sendbtn.click()
                            print("Send button clicked")
                            time.sleep(random.uniform(2, 4))
                            try:
                                MAX_RETRIES = get_overlap_count(driver)
        # Loop to try clicking the buttons multiple times
                                for _ in range(MAX_RETRIES):
                                    try:
                                        resolve_btn = WebDriverWait(driver, random.randint(10, 13)).until(
                                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'arco-btn') and text()='Resolve']"))
                                        )
                                        resolve_btn.click()
                                        time.sleep(random.uniform(2, 4))
                                        move_btn = WebDriverWait(driver, random.randint(10, 13)).until(
                                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'arco-btn') and text()='Move']"))
                                        )
                                        move_btn.click()
                                    
                                    except:
                                        resolve_btn = WebDriverWait(driver, random.randint(10, 13)).until(
                                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'arco-btn-primary') and text()='Resolve']"))
                                    )
                                        resolve_btn.click()
                                        time.sleep(random.uniform(2, 4))
                                        move_btn = WebDriverWait(driver, random.randint(10, 13)).until(
                                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'arco-btn') and text()='Move']"))
                                    )
                                        move_btn.click()
                                    # action.move_to_element(sendbtn).perform()
                                    # sendbtn.click()
                                    count1 = count1 + 1
                                    # try:
                                    #     report(username, user_count)
                                    # except:
                                    #     print("")
                                    # time.sleep(8)
                                    print("send")
                                    # driver.quit()
                                    # time.sleep(5)
                            except:
                                print("Button Not Cliked")
                                #count1 += 1
                        except Exception as e:
                            print(" Send not clicked:", str(e))

                        try:
        #------------------ Step 2: Click Message
                            time.sleep(1)
                            invitebtn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, messagebtn_xpath))
                            )
                            print("Message button found")
                            action.move_to_element(invitebtn).perform()
                            time.sleep(1)
                            invitebtn.click()
                            print("Message button clicked")
                        except Exception as e:
                            print("Message click failed:", str(e))

                        try:
        #------------------- Step 3: Switch to new tab
                            time.sleep(5)
                            if len(driver.window_handles) > 1:
                                # original_tab = driver.current_window_handle
                                driver.switch_to.window(driver.window_handles[-1])
                                print("Switched to new tab")
                            else:
                                raise Exception("New tab not detected")
                            time.sleep(3)
                            #print(driver.page_source)  # to get the creators names from the pop up 
        #------------------- Clicking the share button ont the pop up.
                            sharebtn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, sharebtn_xpath))
                            )
                            print("Share button found")

                            if sharebtn.is_displayed() and sharebtn.is_enabled():
                                driver.execute_script("arguments[0].scrollIntoView(true);", sharebtn)
                                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, sharebtn_xpath)))
                                action.move_to_element(sharebtn).perform()
                                time.sleep(1)
                                try: 
                                    element = driver.find_element(By.XPATH, "//span[@data-e2e='5ea18d74-5ed3-d3c5']")
                                    number = int(element.text)  # Returns "3"
                                    print(f"Number of selected creators: {number}")
                                    increment_count(shop_id, number)
                                    sharebtn = WebDriverWait(driver, 10).until(
                                        EC.element_to_be_clickable((By.XPATH, sharebtn_xpath))
                                    )
                                    print("Share button found")
                                    time.sleep(1)  # Let the DOM settle
                                    sharebtn.click()
                                    print("Share button clicked using .click()")
                                    time.sleep(10)
                                except Exception:
                                    print(".click() failed — trying JavaScript click")
                                    try:
                                        driver.execute_script("arguments[0].click();", sharebtn)
                                        print("Share button clicked using JavaScript")
                                        time.sleep(10)
                                    except Exception as js_e:
                                        print("Even JavaScript click failed:", str(js_e))
        #------------------ Wait for popup to disappear (indicating messages were sent)
                                try:
                                    WebDriverWait(driver, 30).until(
                                        EC.invisibility_of_element_located((By.XPATH, sharebtn_xpath))
                                    )
                                    print("Share popup closed — messages likely sent")
                                except:
                                    print("Share popup still visible after 30 seconds — messages may not be fully sent")
                                time.sleep(50)
        #------------------ Switch back to original tab (do NOT close share tab)
                                driver.switch_to.window(original_tab)
                                print("Switched back to original tab — Share tab remains open")
                                time.sleep(5)  # Small delay before next user
                            else:
                                print("Share button not visible or not enabled")

                        except Exception as e:
                            print("Still failed to find/click Share button:", str(e))
                            import traceback
                            traceback.print_exc()
        #------------------- Recovery: Return to main tab if not already
                            if len(driver.window_handles) > 0:
                                driver.switch_to.window(driver.window_handles[0])
                            print("Recovered and continuing to next user...")

        #-----------------------------------------------------------------------#
                        invitesend = True
                        end_time = datetime.now()
                        duration = end_time - start_time
                        print(f"Iteration {count1} ended at {end_time.strftime('%H:%M:%S')} - Duration: {duration}")  
                        time.sleep(10)     
                        
                        if invitesend:
                            namelist = get_unprocessed_usernames(shop_id)
                            if len(namelist) == 0:
                                print("All Creators Invited Successfully")
                                driver.quit()
                                break
                            else:
                                print("Unprocessed users remain, restarting after 10 minutes")
                                driver.quit()
                                time.sleep(600)  # Wait 10 minutes
                                break  # Break inner loop to restart outer loop
                                # time.sleep(15)
                                # print("Now Again Start")
                        # else:
                        #     if driver:
                        #         time.sleep(15)
                        #         print("Now Again Start...")
                        #     clear_terminal()
                        #     continue
                    else:
                        print(
                            "Invites Not Sent Please Add the data for the Invites in the invite.json file"
                        )
                except Exception as e:
                    print(f"Error in Profile: {e}")
                    if driver is not None:
                        driver.quit()
            if len(namelist) == 0:
                    print("All Creators Invited Successfully")
                    break
        except Exception as e:
                print(f"Critical error in main loop: {e}")
                driver.quit()
                break

def handle_free_sample_option(driver, action, setupfresample_xpath, state, autobtn_xpath, okbtn_xpath):
    """
    Handles clicking the free sample button and selecting the appropriate radio button.
    """
    try:
        try:
            freesamplebtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, setupfresample_xpath))
            )
            action.move_to_element(freesamplebtn).perform()
            freesamplebtn.click()
            print("free sample was clicked")
        except TimeoutException:
            print(f"TimeoutException: Free sample button not found using XPath: {setupfresample_xpath}")
        time.sleep(1)
        radiobtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".flex.flex-1.space-x-12.p-16.rounded-4.h-full.bg-neutral-bg2 .arco-radio-mask",
                )
            )
        )
        radio_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            ".flex.flex-1.space-x-12.p-16.rounded-4.h-full.bg-neutral-bg2 .arco-radio-mask",
        )
#------------------ Click the second radio button
        if len(radio_buttons) >= 2:
            radio_buttons[1].click()
            print("radio button was clicked")
        else:
            print("There are not enough radio buttons on the page")
        time.sleep(1)
        if state == "1":
            pass
        else:
            autobtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, autobtn_xpath))
            )
            action.move_to_element(autobtn).click().perform()
            time.sleep(1)
            okbtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, okbtn_xpath))
            )
            action.move_to_element(okbtn).click().perform()
    except Exception as e:
        print("Sample NOt Added ", e)

def add_products_with_commission(driver, action, productlist, addproduct_xpath, addproduct2_xpath, ADDBTN_xpath, commsioninput_xpath):
    """
    Iterates through the product list, adds each product, and sets the commission.
    """
    checkboxvalue = 2
    print(f"Loaded products: {productlist}")
    for i in range(len(productlist)):
        try:
            if len(productlist[i]) < 2:
                print(f"Skipping incomplete product entry: {productlist[i]}")
                continue
            print(f"Handling product[{i}]: {productlist[i]}")
            product_id, commission = productlist[i]
            print(f"Adding product #{i + 1}: ID={product_id}, Commission={commission}")
            # Use different XPath for 1st vs subsequent products
            btn_xpath = addproduct_xpath if i == 0 else addproduct2_xpath
            # Clicking the add product button 
            addproductbtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, btn_xpath))
            )
            action.move_to_element(addproductbtn).click().perform()
            time.sleep(3)
            try:
                addproduct(driver, [product_id], checkboxvalue)
            except Exception as e:
                print(f"Error adding product: {e}")
            checkboxvalue += 1
            # Clicking the add btn after selecting the product 
            try:
                ADDBTN = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ADDBTN_xpath))
                )
                action.move_to_element(ADDBTN).click().perform()
            except Exception as e:
                print(f"Fallback click on ADDBTN: {e}")
                ADDBTN = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, ADDBTN_xpath))
                )
                time.sleep(random.randint(0.5, 1.5))
                action.move_to_element(ADDBTN).click().perform()
            time.sleep(2)
            # Clicking and Adding the commission
            commsioninputs = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, commsioninput_xpath))
            )
            try:
                print("Adding commission values...")
                for inputs in commsioninputs:
                    action.move_to_element(inputs).click().perform()
                    time.sleep(1)
                    inputs.send_keys(commission)
                    time.sleep(1)
            except Exception as e:
                print(f"Error adding commission: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"Error during product loop: {e}")