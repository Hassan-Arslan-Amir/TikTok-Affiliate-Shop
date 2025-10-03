from time import sleep
from prompt_gemini_captcha import prompt_gemini_captcha
from selenium.webdriver.common.by import By
import random
import logging

def slider_captcha(driver, actions):
    logging.info("Waiting for captcha...")
    for i in range(20):
        captchas = driver.find_elements(By.XPATH, '//div[contains(@class,"captcha_verify_img")]/img')
        if len(captchas) > 0:
            break
        if i >= 19:
            logging.error("No captcha found")
            return False
        sleep(1.2)

    captcha_slider = driver.find_elements(By.XPATH, "//img[contains(@class, 'captcha_verify_img_slide')]")
    if len(captcha_slider) > 0:
       logging.info("Puzzle slider captcha detected!")
       for i in range(1, 11):
            try:
                captcha_elements = driver.find_elements("xpath", '//div[contains(@class,"captcha_verify_img")]/img')
                if len(captcha_elements) > 0:
                    logging.info('Solving captcha (puzzle slider)...')
                    img_element = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_img")]/img')
                    img_location = img_element.location
                    img_size = img_element.size
                    logging.info(f"Image location: {img_location}, size: {img_size}")
                    
                    # Start request solving captcha
                    img_url = img_element.get_attribute("src")
            
                    gemini_response = prompt_gemini_captcha(img_url, 'slider')
                    if gemini_response:
                        shape = gemini_response['coord']
                        
                        offset_x = shape['x'] * img_size['width'] - 30

                        # Find the drag icon element (class contains 'drag-icon')
                        drag_icon = driver.find_element(By.XPATH, "//*[contains(@class, 'drag-icon')]")

                        coordinate_drag = drag_icon.location

                        start_x = coordinate_drag['x'] + 30
                        start_y = coordinate_drag['y'] + 20

                        # Step 1: Use ActionChains to press and hold the mouse on the drag icon
        
                        actions.move_to_element(drag_icon).click_and_hold().perform()

                        # Step 2: Use a Python loop with manual sleep to drag the element with JavaScript
                        steps = 50  # Number of steps for smoother motion
                        step_size = offset_x / steps  # The amount to move the slider in each step

                        random_y = start_y
                        for step in range(steps):
                            # Calculate random y-movement within the range of start_y ± 1
                            random_y += random.uniform(-0.1, 0.1)
                            
                            # Execute JavaScript to shift the mouse over by step_size and introduce random y-movements
                            driver.execute_script("""
                                const locX = arguments[0];
                                const locY = arguments[1];

                                // Dispatch a mousemove event to simulate dragging with random x and y movement
                                const mousemoveEvent = new MouseEvent('mousemove', {
                                    clientX: locX,
                                    clientY: locY,
                                    bubbles: true
                                });
                                document.dispatchEvent(mousemoveEvent);
                            """, start_x + (step * step_size), random_y)  # Move the mouse by step_size and random_y incrementally
                            
                            # Sleep for a random time between 0.01 to 0.05 seconds to simulate human pauses
                            sleep(random.uniform(0.003, 0.013))

                        # Step 3: Release the mouse button using ActionChains
                        actions.release().perform()

                        sleep(10)
                    else:
                        logging.error("No coordinates found in gemini response, refreshing")
                        driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_action")]//span[contains(@class,"secsdk_captcha_refresh--icon")]').click()
                        sleep(5)
                else:
                    logging.info("Captcha successfully solved!")
                    return True
            except:
                continue
    return False


# API_key = "AIzaSyCuYS7VOWYmCeQU3oZ9Ryj6tvDzXkYNVyY"