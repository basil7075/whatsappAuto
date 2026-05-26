import os
import json
import time
from dotenv import load_dotenv
from groq import Groq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 

load_dotenv()

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def send_whatsapp(contact,message):

    options = webdriver.ChromeOptions()
    profile_dir = os.path.join(os.getcwd(),"chrome_whatsapp")
    if not os.path.exists(profile_dir):
        os.mkdir(profile_dir)
    options.add_argument(f"user-data-dir={profile_dir}")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver,60)
    driver.get("https://web.whatsapp.com")
    wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="side"]')))
    
    time.sleep(3)

    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL)
    actions.key_down(Keys.ALT)
    actions.send_keys('/')
    actions.key_up(Keys.CONTROL)
    actions.key_up(Keys.ALT)
    actions.perform()

    active = driver.switch_to.active_element
    active.send_keys(contact)
    time.sleep(1)
    active.send_keys(Keys.ENTER)
    time.sleep(1)

    msg_box = driver.switch_to.active_element
    msg_box.send_keys(message)
    time.sleep(1)
    msg_box.send_keys(Keys.ENTER)
    time.sleep(1)

    driver.quit()

PROMPT = """
You are an ai assistant that can send WhatsApp messages.

If the user wants to send a WhatsApp message,
return JSON in this format:
{"action":"send_whatsapp","contact":"NAME","message":"TEXT"}

For normal conversation,
return JSON in this format:
{"action":"chat","reply":"your response"}

Always return valid JSON only, no other text.
"""

def decide_action(user_text):

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        temperature = 0,
        messages=[
            {"role":"system","content":PROMPT},
            {"role":"user","content":user_text}
        ]
    )

    content = response.choices[0].message.content.strip()
    return json.loads(content)

def main():

    print("Hello there..")
    while True:
        user = input("You: ")
        if user.lower() == "exit":
            break

        try:
            action = decide_action(user)
            if action["action"] == "send_whatsapp":
                contact = action["contact"]
                message = action["message"]
                send_whatsapp(contact,message)
                print("Done...")
            else:
                print("Bot: ",action["reply"])

        except json.JSONDecodeError:
            print("invalid json returned")
        except Exception as e:
            print("ERROR: ",e)

if __name__ == "__main__":
    main()
