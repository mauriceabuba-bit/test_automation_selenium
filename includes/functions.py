
from time import perf_counter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver = None


def start_browser():
    global driver

    if driver is None:
        service = Service("drivers/chromedriver-win64/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()

    return {
        "browser": driver.capabilities.get("browserName", "Unknown"),
        "browser_version": driver.capabilities.get(
            "browserVersion", "Unknown"
        ),
    }


def test_click_item(test_url, target_url, itemname):
    start_time = perf_counter()
    actual_url = ""
    error_message = ""

    try:
        driver.get(test_url)
        link_element = driver.find_element(By.LINK_TEXT, itemname)
        link_element.click()

        actual_url = driver.current_url

        assert actual_url == target_url, (
            f"Expected URL: {target_url}; Actual URL: {actual_url}"
        )

        status = "PASS"

    except Exception as err:
        status = "FAIL"
        error_message = str(err)

        if driver is not None:
            actual_url = driver.current_url

    return {
        "status": status,
        "actual_url": actual_url,
        "error": error_message,
        "duration": round(perf_counter() - start_time, 3),
    }


def close_browser():
    global driver

    if driver is not None:
        driver.quit()
        driver = None
