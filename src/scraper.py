# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scrape_bin_collection(address):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(
            "https://www.merri-bek.vic.gov.au/living-in-merri-bek/waste-and-recycling/bins-and-collection-services/waste-calendar25/"
        )

        # Enter address
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "address"))
        )
        input_box.clear()
        input_box.send_keys(address)

        time.sleep(2)  # wait for suggestions

        suggestions = driver.find_elements(By.CLASS_NAME, "ui-menu-item-wrapper")
        if suggestions:
            for suggestion in suggestions:
                if suggestion.text.strip().lower() == address.lower():
                    suggestion.click()
                    break
            else:
                raise ValueError("Address not found in suggestions")
        else:
            raise ValueError("No suggestions found")

        time.sleep(1)  # wait for hidden fields

        search_button = driver.find_element(
            By.CSS_SELECTOR, "button.button.is-lg[type='submit']"
        )
        search_button.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nextCollections"))
        )

        bins = {
            "General rubbish bin": ("bin", "class", "wasteBinNext"),
            "Food and garden organics bin": ("fogoBin", "id", "fogoBinNext"),
            "Mixed recycling bin": ("recycleBin", "id", "recycleBinNext"),
            "Glass recycling bin": ("glassBin", "id", "glassBinNext"),
        }

        bin_info = {}

        for bin_name, (freq_id, next_locator_type, next_locator_value) in bins.items():
            freq_element = driver.find_element(By.ID, freq_id)

            if next_locator_type == "id":
                next_element = driver.find_element(By.ID, next_locator_value)
            else:
                next_element = driver.find_element(By.CLASS_NAME, next_locator_value)

            freq_text = freq_element.text.strip()
            next_text = next_element.text.strip()
            bin_info[bin_name] = {"frequency": freq_text, "next_collection": next_text}

        return bin_info

    finally:
        driver.quit()
