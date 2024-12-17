import subprocess
import pyperclip  # To copy text to clipboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Step 1: Launch Chrome with Remote Debugging
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Adjust path if necessary

print("Launching Chrome with remote debugging...")
subprocess.Popen([
    chrome_path,
    "--remote-debugging-port=9222",
    "--user-data-dir=C:/Users/RAHEEM/AppData/Local/Google/Chrome/User Data"
])

# Wait for Chrome to launch properly
time.sleep(5)

# Step 2: Connect Selenium to the Running Chrome Instance
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9222")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)

# Step 3: Define and Open Multiple Scanners in Separate Tabs
scanners = [
    "https://chartink.com/screener/copy-20-day-breakout-stocks-4884",
    "https://chartink.com/screener/copy-swingking-intraday-momentum-scanner-499",
    "https://chartink.com/screener/copy-swingking-trendline-breakout-235"
]

all_symbols = []  # To store symbols from all scanners

for index, scanner_url in enumerate(scanners):
    if index == 0:
        driver.get(scanner_url)
    else:
        driver.execute_script(f"window.open('{scanner_url}', '_blank');")

# Step 4: Process Each Scanner Tab to Sort and Extract Symbols
for tab_index in range(len(scanners)):
    driver.switch_to.window(driver.window_handles[tab_index])
    print(f"Processing tab {tab_index + 1} for scanner.")

    # Run the scan
    try:
        run_scan_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Run Scan')]")))
        run_scan_button.click()
    except Exception as e:
        print(f"Could not find the 'Run Scan' button in tab {tab_index + 1}: {e}")

    # Wait for results to load and sort by volume
    try:
        wait.until(EC.presence_of_element_located((By.ID, "DataTables_Table_0")))

        # Click Volume header twice to sort in descending order
        volume_header = wait.until(EC.element_to_be_clickable((By.XPATH, "//th[contains(text(), 'Volume')]")))
        actions.move_to_element(volume_header).click(volume_header).perform()
        time.sleep(1)
        actions.move_to_element(volume_header).click(volume_header).perform()
        time.sleep(1)
    except Exception as e:
        print(f"Error sorting by Volume in tab {tab_index + 1}: {e}")

    # Extract up to 5 symbols from the sorted results
    try:
        symbol_elements = driver.find_elements(By.XPATH, "//*[@id='DataTables_Table_0']//tr/td[3]")[:5]
        symbols = [symbol.text for symbol in symbol_elements]
        all_symbols.extend(symbols)
        print(f"Extracted symbols from tab {tab_index + 1}: {symbols}")
    except Exception as e:
        print(f"Error extracting symbols in tab {tab_index + 1}: {e}")

# Step 5: Open TradingView and Add Symbols
tradingview_url = "https://in.tradingview.com/chart/xyjAl3v7/"
print(f"Opening TradingView with URL: {tradingview_url}")
driver.get(tradingview_url)

try:
    # Ensure 'Swing Analysis' is selected in TradingView
    list_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]/button/span/div")))
    list_button.click()
    current_selection = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]/button/span/div/span[1]"))).text

    if current_selection.lower() != "swing analysis":
        swing_analysis_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="red"]/span[1]/span')))
        swing_analysis_option.click()
        print("Switched to 'Swing Analysis'.")
    else:
        print("'Swing Analysis' is already selected.")
except Exception as e:
    print(f"Error selecting 'Swing Analysis': {e}")
    driver.quit()
    exit()

# Step 6: Add Each Symbol to the Watchlist
try:
    # Click the "+" Button to Open Symbol Input Dialog
    add_icon_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-name="add-symbol-button"]')))
    add_icon_button.click()

    for symbol in all_symbols:
        print(f"Adding '{symbol}' to the watchlist...")
        symbol_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input.search-ZXzPWcCf.upperCase-ZXzPWcCf[placeholder="Search"]')))
        symbol_input.clear()
        symbol_input.send_keys(symbol)
        time.sleep(0.5)  # Small delay to ensure correct symbol appears

        second_add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.button-w6lVe_oI.addAction-oRSs8UQo')))
        second_add_button.click()
        print(f"Successfully added '{symbol}' to the watchlist.")
        time.sleep(0.5)  # Delay between additions

except Exception as e:
    print(f"Error adding symbols to TradingView: {e}")

# Step 7: Close Browser After Test
input("Press Enter to close the browser...")
driver.quit()
