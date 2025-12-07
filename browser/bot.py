from selenium.webdriver.common.by import By
from .manager import BrowserManager
from .frame_navigator import FrameNavigator
from .pdf_handler import PDFHandler
from .form_handler import FormHandler


class BrowserBot:
    """
    Facade class that provides a simple interface to browser automation.
    """
    
    # Locator for app readiness indicator
    APP_READY_LOCATOR = (
        By.XPATH,
        "//div[normalize-space()='Squad Health']"
    )
    
    def __init__(self, download_dir=None, profile_path=None):
        """
        Initialize the browser bot.
        
        Args:
            download_dir: Directory for downloaded files
            profile_path: Chrome profile path
        """
        self.manager = BrowserManager(download_dir, profile_path)
        self.driver = self.manager.driver
        self.wait = self.manager.wait
        
        self.frame_navigator = FrameNavigator(self.driver)
        self.pdf_handler = PDFHandler(self.manager, self.frame_navigator)
        self.form_handler = FormHandler(self.manager, self.frame_navigator)
    
    def start_session(self, url):
        """
        Navigate to URL and wait for app to be ready.
        
        Args:
            url: URL to navigate to
        """
        self.manager.driver.get(url)
        self.wait_for_app()
    
    def wait_for_app(self):
        """
        Wait for the app to be ready (Squad Health element visible).
        
        Returns:
            WebElement if found, None otherwise
        """
        return self.manager.wait_for_element(self.APP_READY_LOCATOR)
    
    def obtain_pdf(self, timeout=30):
        """
        Find Print PDF button, click it, and download the PDF.
        
        Args:
            timeout: Maximum time to wait for download (seconds)
            
        Returns:
            Path to downloaded PDF file, or None if failed
        """
        return self.pdf_handler.download_pdf(timeout)
    
    def fill_form(self, engine):
        """
        Find form, fill all fields using engine, and submit.
        
        Args:
            engine: Object with ask(question) method that returns answers
            
        Returns:
            True if successful, False otherwise
        """
        return self.form_handler.fill_and_submit(engine)
    
    def close(self):
        """Close the browser and clean up resources."""
        self.manager.close()