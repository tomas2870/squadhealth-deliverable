# Squad Health Interview Assignment

This project automates PDF extraction from a web page, performs OCR to extract text, and uses GPT-5.1 to answer form questions based on the PDF content.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key in a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

3. Make sure you have Tesseract installed for OCR:

## Running It

Just run:
```
python main.py
```

The script will handle everything automatically - navigating to the page, downloading the PDF, extracting text, answering questions, and submitting the form.

## How It Works

The code is structured in a modular way:

- **BrowserBot** is a simple interface that combines all the browser operations
- **FrameNavigator** recursively searches through iframes to find elements
- **PDFHandler** waits for and downloads the PDF file
- **FormHandler** fills out form fields by asking the LLM engine for answers
- **PdfLLMEngine** uses GPT-5.1's Responses API to answer questions based on the PDF content

The browser uses a persistent Chrome profile to avoid Cloudflare bot detection and hides automation indicators.

## Notes

- The form questions are read dynamically, so no hardcoding
- The LLM is prompted to give concise answers (just "yes"/"no" for boolean questions)
- Chrome profile data is saved locally to bypass Cloudflare on subsequent runs