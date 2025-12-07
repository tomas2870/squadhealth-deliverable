from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


class FormHandler:
    """Handles automated form filling operations."""
    
    def __init__(self, browser_manager, frame_navigator):
        """
        Initialize the form handler.
        
        Args:
            browser_manager: BrowserManager instance
            frame_navigator: FrameNavigator instance
        """
        self.browser = browser_manager
        self.driver = browser_manager.driver
        self.frame_navigator = frame_navigator
    
    def fill_and_submit(self, engine):
        """
        Find form, fill all fields using the provided engine, and submit.
        
        Args:
            engine: Object with an ask(question) method that returns answers
            
        Returns:
            True if form was submitted successfully, False otherwise
        """
        form = self.frame_navigator.find_form_in_frames()
        
        if form is None:
            return False
        
        if not self._fill_form_fields(form, engine):
            return False
        
        if not self._submit_form(form):
            return False
        
        return True
    
    def _fill_form_fields(self, form, engine):
        """
        Fill all fields in the form using the provided engine.
        
        Args:
            form: WebElement representing the form
            engine: Object with ask(question) method
            
        Returns:
            True if all fields were processed, False if error occurred
        """
        answered = set()
        
        while True:
            try:
                # Find all field containers
                field_divs = set(form.find_elements(By.CSS_SELECTOR, "div.flex.flex-col"))
                field_divs -= answered
                
                if not field_divs:
                    break
                
                field_div = field_divs.pop()
                answered.add(field_div)
                
                # Process this field
                if not self._process_field(field_div, engine):
                    pass  # Continue to next field
                    
            except Exception:
                return False
        
        return True
    
    def _process_field(self, field_div, engine):
        """
        Process a single form field: extract question, get answer, fill field.
        
        Args:
            field_div: WebElement containing the field
            engine: Object with ask(question) method
            
        Returns:
            True if field was processed successfully, False otherwise
        """
        try:
            # Extract question
            question_field = field_div.find_element(By.TAG_NAME, "label")
            question = question_field.text
            
            # Find answer field (input or select)
            answer_field = field_div.find_element(By.CSS_SELECTOR, "input, select")
            
            # Get answer from engine
            response = engine.ask(question)
            
            # Fill the field based on its type
            return self._fill_field(answer_field, response)
            
        except (NoSuchElementException, Exception):
            return False
    
    def _fill_field(self, field, response):
        """
        Fill a field based on its type (input or select).
        
        Args:
            field: WebElement (input or select)
            response: Answer string to fill in
            
        Returns:
            True if field was filled successfully, False otherwise
        """
        try:
            if field.tag_name == "input":
                field.send_keys(response)
                return True
                
            elif field.tag_name == "select":
                return self._fill_select_field(field, response)
                
            else:
                return False
                
        except Exception:
            return False
    
    def _fill_select_field(self, select_field, response):
        """
        Fill a select dropdown based on the response.
        
        Args:
            select_field: WebElement (select)
            response: Answer string ("yes" or "no")
            
        Returns:
            True if selection was made, False otherwise
        """
        response_lower = response.lower().strip()
        
        try:
            select = Select(select_field)
            
            if response_lower == "yes":
                select.select_by_visible_text("Yes")
                return True
                
            elif response_lower == "no":
                select.select_by_visible_text("No")
                return True
                
            else:
                return False
                
        except Exception:
            return False
    
    def _submit_form(self, form):
        """
        Find and click the submit button.
        
        Args:
            form: WebElement representing the form
            
        Returns:
            True if button was clicked, False otherwise
        """
        try:
            submit_button = form.find_element(By.TAG_NAME, "button")
            submit_button.click()
            return True
            
        except (NoSuchElementException, Exception):
            return False