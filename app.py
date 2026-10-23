
import logging
import platform
from datetime import datetime
from pathlib import Path
from time import perf_counter

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from includes import constants, functions

# Create a unique log file for each test run.
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"LOG_FILE_{datetime.now():%Y%m%d_%H%M%S_%f}.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
    force=True,
)

# The six test cases: five real navigation links and one negative test.
tests = [
    ("TC-01", "Home navigation", constants.HOME_TEXT, constants.HOME_URL),
    ("TC-02", "About navigation", constants.ABOUT_TEXT, constants.ABOUT_URL),
    ("TC-03", "Skills navigation", constants.SKILLS_TEXT, constants.SKILLS_URL),
    ("TC-04", "Projects navigation", constants.PROJECTS_TEXT, constants.PROJECTS_URL),
    ("TC-05", "Contact navigation", constants.CONTACT_TEXT, constants.CONTACT_URL),
]

passed = 0
failed = 0
total_duration = 0.0

logging.info("=" * 60)
logging.info("WEBSITE NAVIGATION TEST RUN")
logging.info("Website URL: %s", constants.TEST_URL)
logging.info("Browser: Google Chrome")
logging.info("Operating system: %s", platform.platform())
logging.info("Test run started: %s", datetime.now().astimezone().isoformat())
logging.info("Total planned tests: 6")
logging.info("=" * 60)

try:
    browser_info = functions.start_browser()
    logging.info(
        "Browser started: %s | Version: %s",
        browser_info["browser"],
        browser_info["browser_version"],
    )

    for test_id, item, link_text, expected_url in tests:
        start = perf_counter()
        actual_url = ""
        error_message = ""

        try:
            functions.driver.get(constants.TEST_URL)
            link = functions.driver.find_element(By.LINK_TEXT, link_text)
            link.click()
            actual_url = functions.driver.current_url

            if actual_url != expected_url:
                raise AssertionError(
                    f"Expected URL: {expected_url}; Actual URL: {actual_url}"
                )

            status = "PASS"

        except Exception as error:
            status = "FAIL"
            error_message = str(error)
            if functions.driver is not None:
                actual_url = functions.driver.current_url

        duration = round(perf_counter() - start, 3)
        total_duration += duration

        if status == "PASS":
            passed += 1
            logging.info(
                "%s | Item: %s | Expected: %s | Actual: %s | "
                "Status: PASS | Duration: %.3fs",
                test_id, item, expected_url, actual_url, duration
            )
        else:
            failed += 1
            logging.error(
                "%s | Item: %s | Expected: %s | Actual: %s | "
                "Status: FAIL | Duration: %.3fs | Error: %s",
                test_id, item, expected_url, actual_url, duration, error_message
            )

    # Negative test: the page should not contain a deliberately nonexistent link.
    test_id = "TC-06"
    item = "Negative test - nonexistent link"
    missing_link = "This link should not exist"
    start = perf_counter()
    actual_url = constants.TEST_URL

    try:
        functions.driver.get(constants.TEST_URL)
        functions.driver.find_element(By.LINK_TEXT, missing_link)
        status = "FAIL"
        error_message = "The nonexistent link was unexpectedly found."
    except NoSuchElementException:
        status = "PASS"
        error_message = "Expected NoSuchElementException was raised."
    except Exception as error:
        status = "FAIL"
        error_message = str(error)

    duration = round(perf_counter() - start, 3)
    total_duration += duration

    if status == "PASS":
        passed += 1
        logging.info(
            "%s | Item: %s | Expected: link absent | Actual: link absent | "
            "Status: PASS | Duration: %.3fs | Details: %s",
            test_id, item, duration, error_message
        )
    else:
        failed += 1
        logging.error(
            "%s | Item: %s | Expected: link absent | Actual: link present or test error | "
            "Status: FAIL | Duration: %.3fs | Error: %s",
            test_id, item, duration, error_message
        )

except Exception:
    logging.exception("Test run setup or execution encountered an error.")

finally:
    functions.close_browser()

    logging.info("=" * 60)
    logging.info("TEST SUMMARY")
    logging.info("Total tests: %d", passed + failed)
    logging.info("Passed: %d", passed)
    logging.info("Failed: %d", failed)
    logging.info("Total test duration: %.3f seconds", total_duration)
    logging.info("Log file: %s", log_file)
    logging.info("=" * 60)

print(f"\nTest run finished. See log file: {log_file}")
