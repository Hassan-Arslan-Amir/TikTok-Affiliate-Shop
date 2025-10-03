import sys
import re
import os
import logging
from botUK import run_bot_uk
from botUS import run_us_bot

# ✅ Ensure correct base directory whether frozen or not
try:
    base_dir = sys._MEIPASS  # PyInstaller temp folder
except AttributeError:
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# ✅ Insert the root directory at the beginning of sys.path
sys.path.insert(0, base_dir)
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_utils import fetch_shop_by_name

# Assuming BotUS and BotUK are in the same directory as this file
def check_and_run_bot(shop_id, log_callback=None):
    try:
        print("check_and_run_bot called")
        print("shop_id:", shop_id)    
        def log(msg):
            if log_callback:
                log_callback(msg)
            else:
                print(msg)
        log("Enter into check function")
        # Country map based on phone number prefix
        COUNTRY_MAP = {
            "+1": "USA",  # US Country code
            "+44": "UK",  # UK Country code
        }

        # Fetch shop details from the database
        try:
            selected_shop = fetch_shop_by_name(shop_id)
            log("Shop is found in the database")
        except Exception as db_exc:
            logging.error(f"Database error: {db_exc}")
            log(f"Database error: {db_exc}")
            return

        if not selected_shop:
            logging.warning("No shop found with type 'target write' or 'open colab'.")
            log("No shop found with type 'target write' or 'open colab'.")
            return

        # Extract phone number and country code
        try:
            phone_number = selected_shop.get('phone', '')
            match = re.match(r'(\+\d+)', phone_number)
            country_code = match.group(1) if match else ''
            country = COUNTRY_MAP.get(country_code, "Unknown")
        except Exception as parse_exc:
            logging.error(f"Error parsing phone/country: {parse_exc}")
            log(f"Error parsing phone/country: {parse_exc}")
            return

        logging.info(f"Detected country: {country}")

        if sys.platform == "win32":
            try:
                os.system("chcp 65001")  # Set the console to UTF-8 code page
                os.environ["PYTHONIOENCODING"] = "utf-8"
            except Exception as env_exc:
                logging.warning(f"Failed to set encoding: {env_exc}")

        # Based on the detected country, import and run the respective bot
        try:
            if country == 'USA':
                log("Running US Bot")
                run_us_bot()
            elif country == 'UK':
                log("Running UK Bot")
                run_bot_uk()
            else:
                logging.warning("❌ Unknown country. Bot cannot run.")
                log("❌ Unknown country. Bot cannot run.")
        except Exception as bot_exc:
            logging.error(f"Error running bot: {bot_exc}")
            log(f"Error running bot: {bot_exc}")

    except Exception as exc:
        logging.error(f"Unexpected error in check_and_run_bot: {exc}")
        if log_callback:
            log_callback(f"Unexpected error: {exc}")
        else:
            print(f"Unexpected error: {exc}")

if __name__ == "__main__":
    logging.info("Selecting the type of Bot")
    if len(sys.argv) < 2:
        logging.warning("❌ Please provide a shop ID.")
        sys.exit()

    shop_id = sys.argv[1].strip()  # Get the shop ID from command line argument
    print(f"Shop-ID: {shop_id}")
    check_and_run_bot(shop_id)  # Call the function to check country and run the bot
