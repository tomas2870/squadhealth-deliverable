from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException


class FrameNavigator:
    """Handles navigation through iframe hierarchies to find elements."""
    
    def __init__(self, driver):
        """
        Initialize the frame navigator.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
    
    def find_element_in_frames(self, by, value):
        """
        Recursively search for an element across all iframes.
        
        Args:
            by: Selenium By locator type (e.g., By.XPATH, By.CSS_SELECTOR)
            value: Selector string
            
        Returns:
            WebElement if found, None otherwise
        """
        self._switch_to_default_content()
        return self._find_element_recursive(by, value)
    
    def _switch_to_default_content(self):
        """Safely switch to the default content (top-level document)."""
        try:
            self.driver.switch_to.default_content()
        except WebDriverException:
            pass
    
    def _find_element_recursive(self, by, value):
        """
        Recursive helper to search current frame and all child iframes.
        
        Args:
            by: Selenium By locator type
            value: Selector string
            
        Returns:
            WebElement if found, None otherwise
        """
        # Try to find element in current frame
        try:
            element = self.driver.find_element(by, value)
            return element
        except NoSuchElementException:
            pass
        
        # Search all child iframes
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        
        for frame in frames:
            try:
                self.driver.switch_to.frame(frame)
                element = self._find_element_recursive(by, value)
                
                if element is not None:
                    # Leave driver in the frame where element was found
                    return element
                
                # Element not found in this subtree, go back up
                self.driver.switch_to.parent_frame()
                
            except WebDriverException:
                # Try to recover by switching back to parent
                try:
                    self.driver.switch_to.parent_frame()
                except WebDriverException:
                    pass
        
        return None
    
    def find_form_in_frames(self):
        """
        Find a form element across all iframes.
        
        Returns:
            WebElement (form) if found, None otherwise
        """
        return self.find_element_in_frames(By.CSS_SELECTOR, "form")