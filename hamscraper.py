from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import re

def hamcaster_scraper(fid):
    try:
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--window-size=1920x1080")  # Set the window size

        # Set up Selenium with WebDriver Manager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        # Step 2: Load the webpage with Selenium
        url = f'https://hamcaster.com/token/{fid}'
        driver.get(url)

        # Optional: Wait for the page to fully load, especially if content is dynamically rendered
        time.sleep(3)  # Adjust the wait time based on the website's load time

        # Step 3: Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Step 7: Close the Selenium browser
        driver.quit()

        # step 4 : finding token name and farcaster id and ham rank
        token_tag = soup.find('div',class_="bg-white rounded-full text-black font-bold py-1 px-3")
        token_name = token_tag.text.strip()

        fid_tag = soup.find('p',class_="text-[1.375rem] condensed font-medium uppercase !text-[1.8rem] text-white")
        fid_id_tag = fid_tag.find_next_sibling('p')
        fid_name = fid_id_tag.text.strip()

        rank_tag = soup.find('span',string="Ham Rank")
        rank = rank_tag.find_next_sibling("span")
        rank_name = rank.text.strip()

        # step 5 : finding all requiered numbers 

        voting_power_tag = soup.find('p', string="Total voting power")
        Locked = voting_power_tag.find_next_sibling('p')
        Locked_num = Locked.text.strip()

        totall_stake_tag = soup.find("span",string="Total staked tokens")
        stake = totall_stake_tag.find_next_sibling("span")
        stake_num = stake.text.strip()

        Staker_allo_reward_tag = soup.find("span",string="% of daily allocation rewarded to stakers")
        staker_allo_reward = Staker_allo_reward_tag.find_next_sibling("span")
        stake_allo_reward_num = staker_allo_reward.text.strip()

        staker_tip_reward_tag = soup.find("span",string="% of daily tips given to stakers")
        staker_tip_reward = staker_tip_reward_tag.find_next_sibling("span")
        stake_tip_reward_num = staker_tip_reward.text.strip()

        Ham_allocationn_tag = soup.find("span",string="Latest $HAM allocation")
        Ham_allocation = Ham_allocationn_tag.find_next_sibling("span")
        Ham_allocation_num = Ham_allocation.text.strip()

        # step 6 : market cap and token price 

        token_price_tag = soup.find("span",string="Token price")
        token_price = token_price_tag.find_next_sibling("span")
        token_price_num = token_price.text.strip()

        market_cap_tag = soup.find("span",string="Market cap")
        market_cap = market_cap_tag.find_next_sibling("span")
        market_cap_num = market_cap.text.strip()


        def resufinaler (num):
            reclean = re.match(r'\$?([0-9,]+)\.', num)
            result = reclean.group(1)
            return result
        #step 8 : making json file out of the data

        casterdic = {"FID":str(fid),
                    "Username":fid_name,
                    "token":token_name,
                    "rank":rank_name,
                    "totall locked":resufinaler(Locked_num),
                    "totall staked":resufinaler(stake_num),
                    "shared allocation":stake_allo_reward_num,
                    "share tip":stake_tip_reward_num,
                    "last ham allocation":resufinaler(Ham_allocation_num),
                    "market cap":f"${resufinaler(market_cap_num)}",
                    "token price":token_price_num }
        return casterdic
    
    except:
        return {"error":f"there was a problem exctracting data from fid:{fid}! maybe they haven't set create their caster token yet !"}


    # return print(f"""
    #   fid = {fid}
    #   username = {fid_name}
    #   token = {token_name}
    #   ham rank = {rank_name}
    #   totall locked token = {resufinaler(Locked_num)}
    #   totall staked = {resufinaler(stake_num)}
    #   shared allocation = {stake_allo_reward_num}
    #   shared tip = {stake_tip_reward_num}
    #   last ham allocation = {resufinaler(Ham_allocation_num)}
    #   market cap = ${resufinaler(market_cap_num)}
    #   token price = {token_price_num}
    #   """)    

