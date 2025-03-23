import os
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from logger_config import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

# LinkedIn credentials from environment variables
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
LINKEDIN_PAGE_URL = "https://www.linkedin.com/company/106607818/admin/"


class LinkedInAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Initializes the WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--enable-javascript")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        logger.info("🔹 WebDriver initialized.")

    def teardown_driver(self):
        """Closes the WebDriver."""
        if self.driver:
            self.driver.quit()
            logger.info("🔹 WebDriver closed.")

    def login(self):
        """Logs into LinkedIn using provided credentials."""
        logger.info("🔹 Opening LinkedIn Login Page...")
        self.driver.get("https://www.linkedin.com/login")

        username = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = self.driver.find_element(By.ID, "password")

        username.send_keys(LINKEDIN_EMAIL)
        password.send_keys(LINKEDIN_PASSWORD)
        password.send_keys(Keys.RETURN)

        time.sleep(5)
        logger.info("✅ Logged into LinkedIn!")

    def navigate_to_company_page(self):
        """Navigates to the LinkedIn company admin page."""
        logger.info(f"🔹 Navigating to {LINKEDIN_PAGE_URL}...")
        self.driver.get(LINKEDIN_PAGE_URL)
        time.sleep(3)

    def close_popups(self):
        """Closes any LinkedIn overlays or chat popups."""
        try:
            overlay = self.driver.find_element(
                By.CLASS_NAME, "msg-overlay-bubble-header__details"
            )
            self.driver.execute_script("arguments[0].style.display = 'none';", overlay)
            logger.info("✔ Overlay removed successfully.")
        except Exception:
            logger.info("✔ No overlay detected.")

    #    def click_create_button(self):
    #        """Finds and clicks the 'Create' button."""
    #        logger.info("🔹 Finding 'Create' button...")
    #        create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'org-organizational-page-admin-navigation__cta')]")))
    #
    #        self.driver.execute_script("arguments[0].scrollIntoView();", create_button)
    #        time.sleep(8)

    #        logger.info("🔹 Clicking 'Create' button using JavaScript...")
    #        self.driver.execute_script("arguments[0].click();", create_button)
    #        time.sleep(3)
    #        logger.info("✅ 'Create' button clicked!")

    def click_create_button(self):
        """Finds and clicks the 'Create' button."""
        logger.info("🔹 Finding 'Create' button...")

        try:
            # Wait for the button to be clickable
            create_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(@class, 'org-organizational-page-admin-navigation__cta')]",
                    )
                )
            )

            # Debugging: Log button state
            logger.info(f"Button visible: {create_button.is_displayed()}")
            logger.info(f"Button enabled: {create_button.is_enabled()}")

            # Scroll the button into view
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", create_button
            )
            time.sleep(2)  # Allow time for scrolling

            # Debugging: Take a screenshot before clicking
            self.driver.save_screenshot("before_create_button.png")

            # Click the button using JavaScript
            logger.info("🔹 Clicking 'Create' button using JavaScript...")
            self.driver.execute_script("arguments[0].click();", create_button)
            time.sleep(3)  # Allow time for the click to register

            # Debugging: Take a screenshot after clicking
            self.driver.save_screenshot("after_create_button.png")

            logger.info("✅ 'Create' button clicked!")
        except Exception as e:
            logger.exception(f"❌ Failed to click the 'Create' button: {e}")
            raise

    def click_start_a_post(self):
        """Finds and clicks the 'Start a Post' button."""
        logger.info("🔹 Finding 'Start a Post' button...")
        start_post_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "org-menu-POSTS"))
        )

        self.driver.execute_script("arguments[0].scrollIntoView();", start_post_button)
        time.sleep(5)

        logger.info("🔹 Clicking 'Start a Post' button...")
        self.driver.execute_script("arguments[0].click();", start_post_button)
        time.sleep(5)

        self.driver.switch_to.window(self.driver.window_handles[-1])
        logger.info("✅ 'Start a Post' button clicked!")

    def enter_post_content(self, content):
        """Enters text content into the LinkedIn post box and verifies it."""
        logger.info("🔹 Entering post content...")

        try:
            # Locate the post editor
            text_area = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "ql-editor"))
            )
            text_area.click()  # Focus on the editor
            time.sleep(1)  # Wait for the editor to be ready

            # Insert the content directly using JavaScript
            self.driver.execute_script(
                "arguments[0].innerText = arguments[1];", text_area, content
            )
            time.sleep(2)  # Allow time for the content to be inserted

            # Retrieve the pasted content using JavaScript
            pasted_content = self.driver.execute_script(
                "return arguments[0].innerText;", text_area
            )
            logger.info(f"🔹 Pasted content: {pasted_content}")

            # Debugging: Take a screenshot of the editor
            self.driver.save_screenshot("editor_content.png")

            # Verify if the pasted content matches the original content
            # if pasted_content.strip() == content.strip():
            #     logger.info("✅ Content pasted successfully!")
            # else:
            #     logger.error("❌ Content not pasted correctly!")
            #     raise ValueError("Content not pasted correctly!")
        except Exception as e:
            logger.exception(f"❌ Failed to enter post content: {e}")
            raise  # Re-raise the exception to stop further execution

    def click_post_button(self):
        """Finds and clicks the 'Post' button to publish content."""
        logger.info("🔹 Finding 'Post' button...")

        try:
            # Wait for the button to be clickable
            post_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(@class, 'share-actions__primary-action')]",
                    )
                )
            )

            # Scroll the button into view
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", post_button
            )
            time.sleep(1)  # Allow time for scrolling

            # Debugging: Log button state
            logger.info(f"Button visible: {post_button.is_displayed()}")
            logger.info(f"Button enabled: {post_button.is_enabled()}")

            # Debugging: Take a screenshot before clicking
            self.driver.save_screenshot("before_click.png")

            # Click the button using JavaScript
            logger.info("🔹 Clicking 'Post' button using JavaScript...")
            self.driver.execute_script("arguments[0].click();", post_button)
            time.sleep(2)  # Allow time for the click to register

            # Debugging: Take a screenshot after clicking
            self.driver.save_screenshot("after_click.png")

            logger.info("✅ Post published successfully!")
        except Exception as e:
            logger.exception(f"❌ Failed to click the 'Post' button: {e}")
            raise  # Re-raise the exception to stop further execution

    def post_content(self, content):
        """Automates the process of posting content to LinkedIn."""
        try:
            self.setup_driver()
            self.login()
            self.navigate_to_company_page()
            self.close_popups()
            self.click_create_button()
            self.click_start_a_post()
            self.enter_post_content(content)
            self.click_post_button()
        except Exception as e:
            logger.exception(f"❌ An error occurred: {e}")
        finally:
            time.sleep(5)
            self.teardown_driver()
