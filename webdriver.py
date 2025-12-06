import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import URL

class BrowserBot:
    def __init__(self):
        # Configure Standard Chrome Options
        options = Options()

        # set up auto-download for pdf
        download_dir = os.path.join(os.getcwd(), "downloaded_files")
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,  # Disable download prompt
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True  # Key setting for PDFs
        }
        options.add_experimental_option("prefs", prefs)
        
        # Persistent user profile to prevent cloudflare pop up
        profile_path = os.path.join(os.getcwd(), "chrome_profile")
        options.add_argument(f"--user-data-dir={profile_path}")
        
        # Hide that we're automated from chrome
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        
        # Initialize Standard Chrome driver
        self.driver = webdriver.Chrome(options=options)
        
        # Execute CDP command to further hide webdriver property
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
        })

        # App shell locator: the left-nav "Squad Health" text
        self.APP_READY_LOCATOR = (
            By.XPATH,
            "//div[normalize-space()='Squad Health']"
        )

        # wait method
        self.wait = WebDriverWait(self.driver, 30)
    
    def wait_for_app(self):
        try:
            elem = self.wait.until(
                EC.visibility_of_element_located(self.APP_READY_LOCATOR)
            )
            return elem
        except:
            return
    
    def find_print_pdf(self):
        # try to find the button in the current document
        try:
            btn = self.driver.find_element(
                By.XPATH,
                "//button[normalize-space()='Print PDF']"
            )
            return btn
        except:
            pass

        # not here, so search all iframes in this document
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        for frame in frames:
            try:
                self.driver.switch_to.frame(frame)
                btn = self.find_print_pdf()
                if btn is not None:
                    # leave driver inside the frame where we found it
                    return btn
                # not found in this frame subtree, go back up
                self.driver.switch_to.parent_frame()
            except:
                # if switching or searching fails, try the next frame
                try:
                    self.driver.switch_to.parent_frame()
                except:
                    pass

        return None
    

    def start_session(self):
        self.driver.get(URL)

        self.wait_for_app()
        print("waited")
        btn = None
        while btn is None:
            btn = self.find_print_pdf()
        btn.click()

        time.sleep(30)



    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    bot = BrowserBot()
    try:
        bot.start_session()
        
        # Keep browser open for inspection if needed
        # input("Session complete. Press Enter to close browser...")
        
    except KeyboardInterrupt:
        print("\nStopping bot...")
        bot.close()