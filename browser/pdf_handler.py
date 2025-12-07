import os
import time
from selenium.webdriver.common.by import By


class PDFHandler:
    """Handles PDF download operations."""
    
    DOWNLOAD_POLL_INTERVAL = 0.2  # seconds
    DEFAULT_DOWNLOAD_TIMEOUT = 30  # seconds
    
    def __init__(self, browser_manager, frame_navigator):
        """
        Initialize the PDF handler.
        
        Args:
            browser_manager: BrowserManager instance
            frame_navigator: FrameNavigator instance
        """
        self.browser = browser_manager
        self.driver = browser_manager.driver
        self.download_dir = browser_manager.download_dir
        self.frame_navigator = frame_navigator
    
    def download_pdf(self, timeout=DEFAULT_DOWNLOAD_TIMEOUT):
        """
        Find the Print PDF button, click it, and wait for download to complete.
        
        Args:
            timeout: Maximum time to wait for download (seconds)
            
        Returns:
            Path to downloaded PDF file, or None if download failed
        """
        button = self._find_print_button()
        
        if button is None:
            return None
        
        button.click()
        
        return self._wait_for_download(timeout)
    
    def _find_print_button(self, max_attempts=10, retry_delay=1):
        """
        Find the Print PDF button, retrying if necessary.
        
        Args:
            max_attempts: Maximum number of attempts to find button
            retry_delay: Delay between retry attempts (seconds)
            
        Returns:
            WebElement (button) if found, None otherwise
        """
        for attempt in range(max_attempts):
            button = self.frame_navigator.find_element_in_frames(
                By.XPATH,
                "//button[normalize-space()='Print PDF']"
            )
            
            if button is not None:
                return button
            
            if attempt < max_attempts - 1:
                time.sleep(retry_delay)
        
        return None
    
    def _wait_for_download(self, timeout):
        """
        Wait for a new PDF file to appear in the download directory.
        
        Args:
            timeout: Maximum time to wait (seconds)
            
        Returns:
            Path to downloaded PDF file, or None if timeout reached
        """
        # Get files that exist before download
        before = set(os.listdir(self.download_dir)) if os.path.exists(self.download_dir) else set()
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            current = set(os.listdir(self.download_dir))
            new_files = current - before
            
            # Filter for completed PDF files (ignore .crdownload temp files)
            pdfs = [f for f in new_files if f.lower().endswith(".pdf")]
            
            if pdfs:
                pdf_path = os.path.join(self.download_dir, pdfs[0])
                return pdf_path
            
            time.sleep(self.DOWNLOAD_POLL_INTERVAL)
        
        return None