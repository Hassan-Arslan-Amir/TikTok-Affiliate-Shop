from utils import *
from xpaths import *
from slider_captcha import *
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_utils import (
    mark_user_processed, get_unprocessed_usernames, insert_new_usernames, increment_shop_count
)

def try_solving_slider_captcha(driver, action):
    try:
        captchas = driver.find_elements(By.XPATH, '//div[contains(@class,"captcha_verify_img")]/img')
        if captchas:
            solved = slider_captcha(driver, action)
            if solved:
                logging.info("Captcha solved successfully.")
                return True
            else:
                logging.warning("Captcha was detected but not solved.")
                return False
        else:  
            logging.info("No captcha detected, moving on.")
            return False
    except Exception as e:
        logging.error(f"Captcha solving failed: {e}")
        return False

def type_like_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1,0.3))

def clear_input_like_human(element):
    input_text = element.get_attribute("value")
    for _ in range(len(input_text)):
        element.send_keys(Keys.BACKSPACE)

def clear_input_like_human1(element):
    input_text = element.get_attribute("value")
    text_to_keep = input_text[:4]

    for _ in range(3):
        time.sleep(random.randint(1,3))
        element.send_keys(Keys.BACKSPACE)

def autologin(driver, username, email, password):
    action = ActionChains(driver)

def handleHomepopup(driver):
    print("Handling Home Popup")
    action = ActionChains(driver)
    try:
        try:
            gotit_1 = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, dashBoardGotIt))
            )
            action.move_to_element(gotit_1).click().perform()
            print("Got it 1 button clicked")
        except:
            pass
        try:
            closebtn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, closeBtnXpath))
            )
            action.move_to_element(closebtn).click().perform()
            print("Close button clicked")
        except:
            pass
        try:
            skipbtn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, dashBoardSkip))
            )
            action.move_to_element(skipbtn).click().perform()
            print("Skip button clicked")
        except:
            pass
        try:
            gotit_2 = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, dashBoardGotIt))
            )
            action.move_to_element(gotit_2).click().perform()
            print("Got it 2 button clicked")
        except:
            pass
    except:
        print("Error in handleHomepopup")

def handleinvitepopup(driver):
    print("Handling invitation page Popup")
    action = ActionChains(driver)
    try:
        try:
            closebtn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, closeBtnXpath))
            )
            action.move_to_element(closebtn).click().perform()
            print("Close button clicked")
        except:
            pass
    except:
        print("Error in invitation page Popup")

def handlefindcreatorpopup(driver):
    print("Handling Find Creator Popup")
    action = ActionChains(driver)
    try:
        try:
            closebtn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, closeBtnXpath))
            )
            action.move_to_element(closebtn).click().perform()
            print("Close button clicked...")
        except:
            pass
        try:
            closebtn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//span[@class='arco-icon-hover arco-modal-close-icon' and @role='button' and @aria-label='Close']",
                    )
                )
            )
            action.move_to_element(closebtn).click().perform()
            print("Close button clicked")
        except:
            pass
    except:
        print("Error in handlefindcreatorpopup")

def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def savecreator(driver, username, shop_id):
    print("Saving Creator")
    action = ActionChains(driver)
    import random
    count = 0
    max_creators = random.randint(25, 35)
    selected_any = False
    for userName in username:
        print(userName)
        if count == max_creators:
            break
        try:
            print("search box test")
            searchboxbtn = WebDriverWait(driver, random.randint(2,5)).until(
                EC.presence_of_element_located((By.XPATH, searchBox))
            )
            action.move_to_element(searchboxbtn).click().perform()
            print("Values in Search Box")
            try:
                if searchboxbtn.get_attribute("value"):
                    clear_input_like_human(searchboxbtn)
                #time.sleep(random.randint(2,5))
                type_like_human(searchboxbtn, userName)
                time.sleep(random.randint(2,5))

            except:
                type_like_human(searchboxbtn, userName)
                time.sleep(random.randint(2,5))

            # searchboxbtn = WebDriverWait(driver, 5).until(
            #     EC.presence_of_element_located((By.XPATH, searchBox))
            # )
            # action.move_to_element(searchboxbtn).click().perform()
            # print("Click search box after typing username")
            # time.sleep(2)
#################################################################################
            # searchboxbtn.send_keys(Keys.ENTER)
            # print("Press ENter")
            # time.sleep(5)
            # print("after ENter")
            userxpathh = f"//div[contains(@class, 'flex items-center text-neutral-text1 text-body-m-regular')]//span[contains(text(), '{userName}')]"
            try:
                # userxpathh = f"//div[contains(@class, 'flex items-center text-neutral-text1 text-body-m-regular')]//span[contains(text(), '{userName}')]"
                searchboxbtn1 = WebDriverWait(driver, random.randint(2,5)).until(
                    EC.presence_of_element_located((By.XPATH, userxpathh))
                )
                action.move_to_element(searchboxbtn1).click().perform()
                print("Click username")
                # --------------captcha handling inside savecreator-------------
                if try_solving_slider_captcha(driver, action):
                    print("captcha solved")
            except:
                searchboxbtn = WebDriverWait(driver, random.randint(2,5)).until(
                    EC.presence_of_element_located((By.XPATH, searchBox))
                )
                action.move_to_element(searchboxbtn).click().perform()
                print("Click search box after typing username")
                try:
                    searchboxbtn1 = WebDriverWait(driver, random.randint(2,5)).until(
                        EC.presence_of_element_located((By.XPATH, userxpathh))
                    )
                    action.move_to_element(searchboxbtn1).click().perform()
                    print("Click username")
                    # --------------captcha handling inside savecreator-------------
                    if try_solving_slider_captcha(driver, action):
                        print("captcha solved")
                except:
                    print(f"Not found {userName} with full name, trying first 4 letters")
                    clear_input_like_human1(searchboxbtn)
                    # time.sleep(1)
                    userxpathh = f"//div[contains(@class, 'flex items-center text-neutral-text1 text-body-m-regular')][1]"
                    searchboxbtn1 = WebDriverWait(driver, random.randint(2,5)).until(
                        EC.presence_of_element_located((By.XPATH, userxpathh))
                    )
                    action.move_to_element(searchboxbtn1).click().perform()
                    print("Click username")
                    # --------------captcha handling inside savecreator-------------
                    if try_solving_slider_captcha(driver, action):
                        print("captcha solved")
            try:
                print("Check ok")
                # time.sleep(2)
                checkbtn = WebDriverWait(driver, random.randint(2,5)).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[contains(@class, 'arco-btn-primary') and span[text()='OK']]",
                        )
                    )
                )
                action.move_to_element(checkbtn).click().perform()
            except:
                pass
            mark_user_processed(shop_id, userName)
            #increment_shop_count(shop_id)
            count += 1
            selected_any = True
            print("one cycle done")
            print(f"Processed {count} users")

        except Exception as e:
            print(f"Error in searchbox: {e}")
            print(f"Skipping user {userName} due to error.")
            continue
    if not selected_any:
        raise Exception("No users were selected. Please check the usernames and try again.")
    
def savecreator_scroll(driver, username, shop_id):
    print("Saving Creator")
    action = ActionChains(driver)
    count = 0

    for userName in username:
        if count == 1:
            break
        print(userName)
        try:
            searchboxbtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, searchBox))
            )
            action.move_to_element(searchboxbtn).click().perform()

            if searchboxbtn.get_attribute("value"):
                clear_input_like_human(searchboxbtn)
            type_like_human(searchboxbtn, userName)

            searchboxbtn.send_keys(Keys.ENTER)
            # time.sleep(1)
            try:
                #   print(userName)
                userxpathh = f"//div[contains(@class, 'flex items-center text-neutral-text1 text-body-m-regular')]//span[contains(text(), '{userName}')]"
                searchboxbtn1 = WebDriverWait(driver, 2).until(     
                    EC.presence_of_element_located((By.XPATH, userxpathh))
                ) 
                action.move_to_element(searchboxbtn1).click().perform()

            except:
                pass

            try:
                # time.sleep(2)
                checkbtn = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[contains(@class, 'arco-btn-primary') and span[text()='OK']]",
                        )
                    )
                )
                action.move_to_element(checkbtn).click().perform()
            except:
                pass
            mark_user_processed(shop_id, userName)
            #increment_shop_count(shop_id)
            count += 1

        except Exception as e:
            print(f"Error in searchbox: {e}")

def delete_creator(driver, shop_id):
    action = ActionChains(driver)
    namelist = get_unprocessed_usernames(shop_id)
    try:
        paginationxpath = "//div[@class='arco-pagination-option']"
        pageselectxpath = (
            "//span[@class='arco-select-option-content-wrapper' and text()='50/Page']"
        )
        print("Deleting Creator")

        try:
            pagebtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, paginationxpath))
            )
            action.move_to_element(pagebtn).perform()
            pagebtn.click()
            time.sleep(3)

            pageselectbtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, pageselectxpath))
            )
            action.move_to_element(pageselectbtn).perform()
            pageselectbtn.click()
            print("Clicked On the Button and Select the 50 Users")
            time.sleep(1)
        except:
            print("⚠️ Error selecting 50/page pagination")
    except:
        print("⚠️ Could not initiate pagination")

    for name in namelist:
        print(name)
        name = name.strip("@")
        print(name)
        try:
            xpathfordelete = (
                f"//tr[@class='arco-table-tr'][contains(@data-e2e, '25e149be-38bd-c830')]"
                f"//div[@class='text-neutral-text1 text-body-m-medium cursor-pointer' and" 
                f"div[@class='arco-typography' and contains(text(), '{name}')]]"
                f"/ancestor::tr/td[@class='arco-table-td'][2]//button[@class='arco-btn arco-btn-primary arco-btn-size-default arco-btn-shape-square m4b-button m4b-button-link']"
            )
            deletebtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpathfordelete))
            )
            action.move_to_element(deletebtn).click().perform()
            time.sleep(1)
        except Exception as e:
            print(f"Error in deleting: {e}")

def addcreators(driver, userName):
    print("Adding Saved Creator")
    action = ActionChains(driver)
    try:
        searchboxbtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, searchBox))
        )

        action.move_to_element(searchboxbtn).click().perform()

        if searchboxbtn.get_attribute("value"):
            clear_input_like_human(searchboxbtn)
        type_like_human(searchboxbtn, userName)

        searchboxbtn.send_keys(Keys.ENTER)
        time.sleep(2)

        firstusername_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, firstusername))
        )
        if firstusername_text.text == userName:
            print(f"profile {firstusername_text.text } is Successfully found.")
            time.sleep(1)
            Xpathforclick = f"//span[text()='{userName}']/ancestor::tr//button[@data-e2e='d610879c-a3e6-6f81']"
            try:
                saveicon = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, Xpathforclick))
                )
            #   action.move_to_element(saveicon).click().perform()
            except:
                Xpathforclick = f"//span[text()='{userName}']/ancestor::tr//button[@data-e2e='3ae7a02c-0a1b-60bb']"

                saveicon = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, Xpathforclick))
                )
                action.move_to_element(saveicon).click().perform()

    except Exception as e:
        print(f"Error in searchbox: {e}")

def addproduct(driver, productlist, checkboxvalue):
    dropdown = False
    print("Adding Product")
    action = ActionChains(driver)
    productID = str(productlist[0])
    logging.info(f"🔢 Product ID: {productID}")
    try:
            try:
                dropdownbtn = WebDriverWait(driver, random.randint(10,13)).until(
                    EC.presence_of_element_located((By.XPATH, dropdown_XPath))
                )
                action.move_to_element(dropdownbtn).click().perform()
                dropdown = True
                time.sleep(random.uniform(2,5))
                logging.info("🔽 Dropdown clicked")
            except Exception:
                logging.warning("⚠️ Dropdown button not found or skipped")
            if dropdown:
                try:
                    IDoption = WebDriverWait(driver, random.randint(10,13)).until(
                        EC.presence_of_element_located((By.XPATH, IDoption_xpath))
                    )
                    action.move_to_element(IDoption).click().perform()
                    time.sleep(random.randint(2,5))
                    logging.info("✅ ID Option selected")
                except Exception as e:
                    logging.warning(f"⚠️ Failed to select ID Option: {e}")
            cardcheck_xpath = ""
            if checkboxvalue == 1:
                cardcheck_xpath = '(//label[@class="arco-checkbox"])[1]'
            if checkboxvalue == 2:
                cardcheck_xpath = '(//label[@class="arco-checkbox"])[2]'
            if checkboxvalue == 3:
                cardcheck_xpath = '(//label[@class="arco-checkbox"])[3]'
            if checkboxvalue == 4:
                cardcheck_xpath = '(//label[@class="arco-checkbox"])[4]'
            if checkboxvalue == 5:
                cardcheck_xpath = '(//label[@class="arco-checkbox"])[5]'
            # cardInput_Xpath = '(//label[@class="arco-checkbox"]/input)[2]'
            cardInput = WebDriverWait(driver, random.randint(10,13)).until(
                EC.presence_of_element_located((By.XPATH, cardInput_Xpath))
            )
            action.move_to_element(cardInput).click().perform()
            if cardInput.get_attribute("value"):
                action.key_down(Keys.COMMAND).send_keys("a").key_up(
                    Keys.COMMAND
                ).perform()
                action.send_keys(Keys.BACKSPACE).perform()
            for char in productID:
                cardInput.send_keys(char)
                logging.debug(f"➡️ Typing: {char}")

            time.sleep(random.uniform(2,5))
            cardInput.send_keys(Keys.ENTER)
            logging.info("📩 Product ID entered and submitted")
            time.sleep(random.uniform(2,5))
            try:
                checkbtn = WebDriverWait(driver, random.randint(20,25)).until(
                    # EC.presence_of_element_located((By.XPATH, '(//label[@class="arco-checkbox"])/input)[1]'))
                    EC.element_to_be_clickable((By.XPATH, cardcheck_xpath))
                )
                action.move_to_element(checkbtn).click().perform()
                time.sleep(random.uniform(1,3))
                logging.info("✅ Product checkbox selected")
            except Exception:
                try:
                    checkbtn = WebDriverWait(driver, random.randint(10, 13)).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//button[contains(@class, 'arco-btn-primary') and span[text()='OK']]",
                            )
                        )
                    )
                    action.move_to_element(checkbtn).click().perform()
                    logging.info("✅ Fallback OK button clicked")
                    time.sleep(random.uniform(2,5))
                except Exception as e:
                    logging.error(f"❌ Failed to select product checkbox or fallback button: {e}")
    except Exception as e:
            logging.error(f"❌ Exception in addproduct: {e}")

def createinvite(
    driver, action, invitation_name, email_address, phone_number, message, valid_until,p_XPATH
):
    try:
        print(invitation_name, valid_until)
        invitationbtn = WebDriverWait(driver, random.randint(10, 13)).until(
            EC.presence_of_element_located((By.XPATH, invitationname_xpath))
        )
        action.move_to_element(invitationbtn).click().perform()
        time.sleep(random.uniform(1, 3))
        for char in invitation_name:
            invitationbtn.send_keys(char)
        time.sleep(random.uniform(2, 5))
#------------------- valid date
        validbtn = WebDriverWait(driver, random.randint(10, 13)).until(
            EC.presence_of_element_located((By.XPATH, date_xpath))
        )
        action.move_to_element(validbtn).click().perform()
        time.sleep(random.uniform(1, 3))
        validbtn.send_keys(valid_until)
        time.sleep(random.uniform(1, 3))
        validbtn.send_keys(Keys.ENTER)
        time.sleep(random.uniform(1, 3))
        # action.send_keys(Keys.PAGE_DOWN).perform()
        # time.sleep(2)
#---------------------- EMAIL FEILD -----------------------------
        emailbtn = WebDriverWait(driver, random.randint(10, 13)).until(
            EC.presence_of_element_located((By.XPATH, email_xpath))
        )
        action.move_to_element(emailbtn).click().perform()
        time.sleep(random.uniform(1, 3))
        if emailbtn.get_attribute("value"):
            action.key_down(Keys.CONTROL).send_keys("a").key_up(
                Keys.CONTROL
            ).perform()  # Corrected to use CONTROL instead of COMMAND
            action.send_keys(Keys.BACKSPACE).perform()
            time.sleep(random.uniform(1, 3))
        for char in email_address:
            emailbtn.send_keys(char)
        time.sleep(random.uniform(2, 5))
#------------------------ PHONE FIELD ----------------------       
        phonebtn = WebDriverWait(driver, random.randint(10, 13)).until(
            EC.presence_of_element_located((By.XPATH, p_XPATH))
        )
        action.move_to_element(phonebtn).click().perform()
        time.sleep(random.uniform(1, 3))
        if phonebtn.get_attribute("value"):
            action.key_down(Keys.CONTROL).send_keys("a").key_up(
                Keys.CONTROL
            ).perform()  # Corrected to use CONTROL instead of COMMAND
            action.send_keys(Keys.BACKSPACE).perform()
            time.sleep(random.uniform(1, 3))
        for char in phone_number:
            phonebtn.send_keys(char)
        time.sleep(random.uniform(2, 5))
#------------------------ MESSAGE FEILD -------------------------------
        messagebtn = WebDriverWait(driver, random.randint(10, 13)).until(
            EC.presence_of_element_located((By.XPATH, messagearea_xpath))
        )
        action.move_to_element(messagebtn).click().perform()
        time.sleep(random.uniform(1, 3))
        if messagebtn.get_attribute("value"):
            action.key_down(Keys.CONTROL).send_keys("a").key_up(
                Keys.CONTROL
            ).perform()  # Corrected to use CONTROL instead of COMMAND
            action.send_keys(Keys.BACKSPACE).perform()
            time.sleep(random.uniform(1, 3))
        for char in message:
            messagebtn.send_keys(char)
            # time.sleep(0.1)
        time.sleep(random.uniform(2, 5))
        print("All data Entered Successfully.")

    except Exception as E:
        print(f"Error in Create invite: {E}")

def scroll_and_get_user(driver, shop_id, scrape_users):
    print("📥 Start scraping usernames...")
    cards_increment = 11
    loop_count = 0
    card_count = 0
    action = ActionChains(driver)
    exception_count = 0
    handlefindcreatorpopup(driver)

    scrape_users = int(scrape_users)
    while True:

        if loop_count > scrape_users:
            break

        current_xpath = f'//*[@id="content-container"]/main/div/div/div/div/div[5]/div/div/div/div/div[2]/div/div/div/div/div/div[2]/table/tbody/div[{card_count + cards_increment}]/div'
        try:
            try:
                element = WebDriverWait(driver, random.randint(10, 13)).until(
                    EC.presence_of_element_located((By.XPATH, current_xpath))
                )

                driver.execute_script("arguments[0].scrollIntoView(true);", element)

            except:
                time.sleep(random.uniform(1, 3))
            card_count += cards_increment

            xpath_selector = "//span[@data-e2e='2a4d0b67-9339-05c0']/span[@data-e2e='fbc99397-6043-1b37']"
            WebDriverWait(driver, random.randint(10, 13)).until(
                EC.presence_of_element_located((By.XPATH, xpath_selector))
            )
            element = driver.find_elements(By.XPATH, xpath_selector)
            # Load from DB
            scraped_usernames = [el.text.strip() for el in element]
            existing_usernames = get_unprocessed_usernames(shop_id)
            set1 = set(scraped_usernames)
            set2 = set(existing_usernames)

            new_usernames = list(set1 - set2)
            insert_new_usernames(shop_id, new_usernames)

            user_count = len(new_usernames)
            loop_count += user_count
            exception_count = 0
        except Exception as e:
            print(f"❌ Error while scraping users: {e}")
            card_count -= 2
            exception_count += 1
            if exception_count > 3:
                print("⚠️ Too many consecutive scroll failures. Stopping.")
                break
