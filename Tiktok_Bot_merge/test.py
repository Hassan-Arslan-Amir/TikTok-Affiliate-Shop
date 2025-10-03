# from helper import get_product_from_csv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# product_file_path = f"./nameofcreator/{username}/productname.csv"
# productlist = get_product_from_csv(product_file_path)
# for i in range(len(productlist)-1):
#     print(productlist[i+1])
#     test=productlist[i+1]
#     print(test[0])
# # print(productlist)

from utils import *
from xpaths import *
from helper import *
import os

from selenium.webdriver.chrome.options import Options


def is_csv_empty(file_path):
    """
    Checks if a CSV file is empty. A file is considered empty if it has no data rows, possibly only containing headers.

    Args:
    file_path (str): The path to the CSV file.

    Returns:
    bool: True if the file is empty, False otherwise.
    """
    # Check if the file exists and has a size greater than zero
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return True  # File does not exist or is empty

    # Check for any data rows in the file
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(
                reader, None
            )  # Skip the header if there is one, safely handle missing header
            # Check if there is at least one row of data
            for row in reader:
                if row:  # If there's at least one non-empty row, the file isn't empty
                    return False
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return True  # Assume empty if cannot read (optional, depending on your error handling preference)

    return True  # If no rows were found, the file is empty


def openchrome(username):
    cookies_available = False
    try:
        print("1")
        options = Options()
        options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
        options.add_argument("--ignore-ssl-errors")  # Ignore SSL errors
        options.add_argument("--disable-gpu")  # (Optional) Helps in headless mode
        # options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        print("1")
        driver = webdriver.Chrome(service=service, options=options)
        options = webdriver.ChromeOptions()
        print("1")

        # options.add_argument("--start-maximized")  # Maximize the browser window
        # options.add_argument("--disable-infobars")
        # driver.maximize_window()
        driver.set_window_size(1300, 900)  # Width = 1200 pixels, Height = 800 pixels

        time.sleep(1)
        driver.get("https://affiliate-us.tiktok.com/platform/homepage?shop_region=US")
        time.sleep(10)
        cookie_file = f"./cookies/cookies-{username}.json"
        if os.path.isfile(cookie_file):
            cookies_available = True
            with open(cookie_file, "r", encoding="utf-8") as file:
                cookies = json.load(file)
        else:
            emailData = input("Enter your email: ")
            passwordData = input("Enter your password: ")
            autologin(driver, username, emailData, passwordData)
            print("Successfully logged in.")
            #export_cookies(driver, username)
            time.sleep(random.randint(5, 7))
        if cookies_available:
            print("Page loaded. Adding cookies to the browser session...")
            for cookie in cookies:
                if "expiry" in cookie:
                    cookie["expiry"] = int(cookie["expiry"])
                if "sameSite" not in cookie or cookie["sameSite"] not in [
                    "Strict",
                    "Lax",
                    "None",
                ]:
                    cookie["sameSite"] = "None"
                cookie["domain"] = ".tiktok.com"
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


def get_data(choice, data):
    """
    Retrieves data and its key name from the JSON file based on user choice.

    Args:
        choice: An integer representing the desired object (1 for first, etc.).

    Returns:
        A tuple containing the key name (string) and the requested data (dictionary).
    """

    # Validate user input
    if choice < 1 or choice > len(data):
        return "Invalid choice. Please enter a number between 1 and {}".format(
            len(data)
        )

    # Access data and key name based on choice (array index starts from 0)
    selected_key = list(data.keys())[choice - 1]
    return selected_key, data[selected_key][0]


def get_all_keys(data):
    """
    Retrieves all the keys from the JSON data.

    Returns:
        A list containing all the key names (strings) in the JSON data.
    """
    return list(data.keys())


import discord
from discord.ext import commands


def report(username, user_count):

    # Create a new instance of the bot
    intents = discord.Intents.default()
    intents.message_content = (
        True  # Enable the message content intent if you need to read message contents
    )

    # Create a new instance of the bot with intents
    bot = commands.Bot(command_prefix="!", intents=intents)

    # Get Discord bot token from environment variable
    TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')

    @bot.event
    async def on_ready():
        print(f"Bot is ready. Logged in as {bot.user.name}")
        profiles = [
            {
                "profile_name": username,
                "num_creators": user_count,
            }
        ]

        report_message = "Profile Report:\n"
        for profile in profiles:
            report_message += (
                f"Profile Name: {profile['profile_name']}\n"
                f"Number of Creators Search: {profile['num_creators']}\n"
            )

        channel = bot.get_channel(1131877636331798590)
        if channel:
            # Send the report message to the specified Discord channel
            await channel.send(report_message)

    bot.run(TOKEN)