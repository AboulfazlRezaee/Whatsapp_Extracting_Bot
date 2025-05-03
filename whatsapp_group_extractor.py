from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import pandas as pd
import re

# ------------------------
chrome_driver_path = "chromedriver.exe"
# ------------------------

# chrome driver path
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get("https://web.whatsapp.com")


print("🔄 Please scan the QR code to log in...")

# wait for login
try:
    WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="grid"]'))
    )
    print("✅ Loged in successfully")
except:
    print("❌ Login failed or timeout")
    driver.quit()
    exit()


# get list of chats/groups
print("\n⏳ Loading chats...")
time.sleep(5)
groups_elements = driver.find_elements(By.XPATH, '//span[@dir="auto" and @title]')
group_names = sorted(list(set([elem.get_attribute("title") for elem in groups_elements])))

print("\n>>> list of groups:")
print("==========================================")
for idx, name in enumerate(group_names):
    print(f"{idx+1}. {name}")

selected_index = int(input("\n>>>Eenter the number of the group you want to check: ")) - 1
selected_group = group_names[selected_index]
print(f"\n>>> Group Selected: {selected_group}")


# serch for the group
print("\n⏳ Searching for the group...")
def clean_text(text):
    return re.sub(r'[^\u0000-\uFFFF]', '', text)

search_box = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @role="textbox"]'))
)
search_box.click()
search_box.clear()
search_box.send_keys(clean_text(selected_group))
search_box.send_keys(Keys.ENTER)
time.sleep(3)


#open group info
print("\n⏳ Opening group info...")
group_header = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//header'))
)
group_header.click()
time.sleep(2)


try:
    members_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header/div[2]'))
    )
    members_button.click()
    print("✅ Group info opened")
except:
    print("❌ could not find group info button.")
    driver.quit()
    exit()


#  scroll down to load all members
print("\n⏳ Scrolling members list...")
try:
    # Wait for the scroll area to load
    scroll_area = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[5]/span/div/span/div/div/div'))
    )
    time.sleep(2)  # Wait for the scroll area to load
    
    # Scroll down to load all members
    for _ in range(1):  # Adjust the range for more or fewer scrolls
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_area)
        time.sleep(2)
        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_area)
        # print("✅ Scrolling Done")

    time.sleep(3)

except Exception as e:
    print("\n❌ could not scroll participants area:", e)

    exit()


try:
    print("\n⏳ Loading more members...")
    view_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "View all")]'))
    )
    view_all_button.click()
    # print("\n✅ 'View all' button clicked.")
    time.sleep(3)
except Exception as e:
    print("\n❌ Failed to click 'View all' button:", e)
    driver.quit()
    exit()


# Scroll to load all members
try:

    print("\n⏳ Scrolling to load members...")
    scroll_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]'))
    )
    last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)

    # Scroll down to load all members
    for _ in range(1):  # Adjust the range for more or fewer scrolls
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(2)
        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
        # print("\n✅ Scrolling Done")
        time.sleep(2)

except Exception as e:
    print("\n❌ Failed to scroll:", e)
    driver.quit()
    exit()

time.sleep(5)

print("\n⏳ Extracting members...")
# execute JavaScript to get phone numbers starting with +98
js_code = """
const allSpans = document.querySelectorAll("span[dir='auto']");
const numbers = [];

allSpans.forEach(span => {
  const text = span.textContent.trim();
  if (text.startsWith("+98")) {
    numbers.push(text);
  }
});

return [...new Set(numbers)];
"""

numbers = driver.execute_script(js_code)

if not numbers:
    print("❌ No numbers found.")
else:
    print(f"✅ Extracted {len(numbers)} phone numbers.")

    # Save to Excel
    df = pd.DataFrame(numbers, columns=["Phone"])
    TodaysDate = time.strftime("%d_%m_%Y")
    excel_filename = f"group_{TodaysDate}.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"✅ Phone numbers saved to {excel_filename}")

time.sleep(3)
# Close the browser
print("\n⏳ Closing the browser...")
driver.quit()

