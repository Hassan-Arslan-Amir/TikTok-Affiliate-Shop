from utils import *
from batch_message_xpaths import *
from xpaths import *
import logging
from slider_captcha import slider_captcha

def export_cookies(driver, username):
    # Retrieve cookies from the browser session
    cookies = driver.get_cookies()

    # Write cookies to the specified file in JSON format
    import os
    os.makedirs("cookies", exist_ok=True)
    file_path = f"./cookies/cookies-{username}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(cookies, file, ensure_ascii=False, indent=4)

    print(f"Cookies exported successfully to {file_path}")

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


def clear_input_like_human(element):
    """
    Clears the input field in a human-like manner.

    :param element: The input WebElement to be cleared.
    """
    input_text = element.get_attribute("value")
    for _ in range(len(input_text)):
        element.send_keys(Keys.BACKSPACE)


def type_like_human(element, text):
    for char in text:
        element.send_keys(char)

def handleHomepopup(driver):
    print("Handling Home Popup")
    action = ActionChains(driver)
    try:
        try:
            close_icons = driver.find_elements(
                By.XPATH, "//span[contains(@class, 'arco-modal-close-icon')]"
            )
            for icon in close_icons:
                icon.click()
                time.sleep(2)
        except:
            pass
        try:
            close_icons = driver.find_elements(
                By.XPATH, "//span[contains(@class, 'arco-modal-close-icon')]"
            )
            for icon in close_icons:
                icon.click()
                time.sleep(2)
        except:
            pass
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
            time.sleep(2)
            skipbtn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, dashBoardSkip))
            )
            action.move_to_element(skipbtn).click().perform()
            print("Skip button clicked")
        except:
            pass
        try:
            time.sleep(1)
            gotit_2 = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, dashBoardGotIt))
            )
            action.move_to_element(gotit_2).click().perform()
            print("Got it 2 button clicked")
        except:
            pass
    except:
        print("Error in handleHomepopup")


def handlefindcreatorpopup(driver):
    print("Handling Find Creator Popup")
    action = ActionChains(driver)
    try:
        try:
            close_icons = driver.find_elements(
                By.XPATH, "//span[contains(@class, 'arco-modal-close-icon')]"
            )
            for icon in close_icons:
                icon.click()
                time.sleep(2)
        except:
            pass
        try:
            close_icons = driver.find_elements(
                By.XPATH, "//span[contains(@class, 'arco-modal-close-icon')]"
            )
            for icon in close_icons:
                icon.click()
                time.sleep(2)
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
    except:
        print("Error in handlefindcreatorpopup")

def send_message(
    driver,
    cardFlag,
    cardName,
    messageData1,
    original_tab,
    action,
    profilename,
    productstatus,
):
    try:
        if productstatus == 1:
            try:
                print("line 288: not Max")
                try:
                    productbtn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, sidebarelements))
                    )
                    action.move_to_element(productbtn).perform()
                    time.sleep(1)
                    productbtn.click()
                    time.sleep(2)
                    print("Click on Side bar")
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    time.sleep(2)
                    productbtn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, sidebarelements))
                    )
                    action.move_to_element(productbtn).perform()
                    time.sleep(1)
                    productbtn.click()
                    time.sleep(2)
                    print("Click on Side bar1")

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
                print("Searching Card")

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
                            print("Finding Product Card and sending")
                            Card = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//div[@data-e2e='ee7482a9-a8f4-7400']")
                                )
                            )
                            if Card:
                                action.move_to_element(Card).perform()
                                sendbutton = WebDriverWait(driver, 3).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, sendproduct)
                                    )
                                )
                                sendbutton.click()
                                print("Send product card")
                                time.sleep(2)
                                break
                            else:
                                print("Retrying....")
                                time.sleep(2)
                    else:
                        cardInputData.send_keys(cardName)
                        time.sleep(1)
                        cardInputData.send_keys(Keys.ENTER)

                        for _ in range(3):
                            print("Finding Product Card and sending")
                            Card = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//div[@data-e2e='ee7482a9-a8f4-7400']")
                                )
                            )
                            if Card:
                                action.move_to_element(Card).perform()
                                sendbutton = WebDriverWait(driver, 3).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, sendproduct)
                                    )
                                )
                                sendbutton.click()
                                print("Send product card")
                                time.sleep(2)
                                break
                            else:
                                print("Retrying....")

                except Exception as e:
                    print(f"Product Card Not Added: {e}")
                    time.sleep(3)
                    for _ in range(3):
                        print("Finding Product Card and sending")
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
                            print("Send product card")
                            time.sleep(2)
                            break
                        else:
                            print("Retrying....")

            except Exception as e:
                print(f"Error occurred: {e}")
                return 2

    except Exception as e:
        print(f"Card Not Sending issue is there: {e}")

    try:
        for _ in range(2):
            try:
                print("In message section")
                messageArea = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, messageArea1))
                )
                time.sleep(uniform(2, 4))
                messageArea.click()
                print("Click on message area")

                containsNewline = "\n" in messageData1
                script = "document.querySelector('textarea').value += arguments[0];"
                driver.execute_script(script, messageData1)
                time.sleep(uniform(0.8, 1))
                messageArea.send_keys("a")
                time.sleep(uniform(0.8, 1))
                messageArea.send_keys(Keys.BACK_SPACE)
                time.sleep(1)
                print("Going to click msg btn")
                messageArea.send_keys(Keys.ENTER)
                time.sleep(2)
                print("Messages Sent")
                return 1

            except Exception as e:
                print(f"Exception occurred: {e}")
                messageArea = WebDriverWait(driver, 150).until(
                    EC.presence_of_element_located((By.XPATH, messageArea2))
                )
                time.sleep(uniform(1, 2))
                messageArea.click()
                time.sleep(uniform(1, 2))
                print("Typing in text area")
                type_like_human(driver, messageData1)
                time.sleep(uniform(1, 2))
                return 1

    except Exception as e:
        print(f"Error in Sending messages: {e}")

    return True
