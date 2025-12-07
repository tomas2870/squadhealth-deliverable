import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BrowserManager:
    """Manages browser initialization, configuration, and lifecycle."""
    
    DEFAULT_TIMEOUT = 30
    
    def __init__(self, download_dir=None, profile_path=None, timeout=DEFAULT_TIMEOUT):
        """
        Initialize the browser manager.
        
        Args:
            download_dir: Directory for downloaded files (defaults to ./downloaded_files)
            profile_path: Chrome profile path (defaults to ./chrome_profile)
            timeout: Default timeout for WebDriverWait operations
        """
        self.download_dir = download_dir or os.path.join(os.getcwd(), "downloaded_files")
        self.profile_path = profile_path or os.path.join(os.getcwd(), "chrome_profile")
        self.timeout = timeout
        
        os.makedirs(self.download_dir, exist_ok=True)
        
        self.driver = self._initialize_driver()
        self.wait = WebDriverWait(self.driver, self.timeout)
    
    def _initialize_driver(self):
        """Configure and initialize the Chrome WebDriver."""
        options = Options()
        
        # Configure PDF auto-download
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        }
        options.add_experimental_option("prefs", prefs)
        
        # Use persistent profile to avoid Cloudflare issues
        options.add_argument(f"--user-data-dir={self.profile_path}")
        
        # Hide automation indicators
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--start-maximized")
        
        driver = webdriver.Chrome(options=options)
        
        # Further hide webdriver property via CDP
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        
        return driver
    
    def wait_for_element(self, locator, timeout=None):
        """
        Wait for an element to be visible.
        
        Args:
            locator: Tuple of (By, selector_string)
            timeout: Optional custom timeout
            
        Returns:
            WebElement if found, None otherwise
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.visibility_of_element_located(locator))
        except Exception:
            return None
    
    def close(self):
        """Close the browser and clean up resources."""
        self.driver.quit()