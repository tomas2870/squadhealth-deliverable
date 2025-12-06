import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import URL
from pdf_processor import extract_text_from_pdf

class BrowserBot:
    def __init__(self):
        # Configure Standard Chrome Options
        options = Options()

        # set up auto-download for pdf
        self.download_dir = os.path.join(os.getcwd(), "downloaded_files")
        prefs = {
            "download.default_directory": self.download_dir,
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
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--start-maximized")

        # #random stuff
        # options.add_argument("--no-first-run")
        # options.add_argument("--no-service-autorun")
        # options.add_argument("--password-store=basic")
        
        # # Standard arguments for stability
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--start-maximized")
        
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
    
    def wait_for_new_pdf(self, timeout=30):
        # files that exist before download
        before = set(os.listdir(self.download_dir)) if os.path.exists(self.download_dir) else set()
        end = time.time() + timeout

        while time.time() < end:
            current = set(os.listdir(self.download_dir))
            new_files = current - before

            # ignore temp .crdownload files, only keep .pdf
            pdfs = [f for f in new_files if f.lower().endswith(".pdf")]
            if pdfs:
                # assume first new pdf is the one we want
                return os.path.join(self.download_dir, pdfs[0])
            time.sleep(0.2)

        return None
    
    def obtain_pdf(self):
        self.driver.get(URL)

        self.wait_for_app()
        print("waited")
        btn = None
        while btn is None:
            btn = self.find_print_pdf()
        btn.click()

        pdf = self.wait_for_new_pdf()
        extract_text_from_pdf(pdf)

    def fill_form(self):
        print("hello")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    bot = BrowserBot()
    try:
        bot.obtain_pdf()
        
        # Keep browser open for inspection if needed
        # input("Session complete. Press Enter to close browser...")
        
    except KeyboardInterrupt:
        print("\nStopping bot...")
        bot.close()