from browser import BrowserBot 
from pdf_llm_engine import PdfLLMEngine
from pdf_processor import extract_text_from_pdf
from config import URL


def main():
    bot = BrowserBot()
    try:
        bot.start_session(URL)           # navigate + wait for app
        pdf_path = bot.obtain_pdf()      # click Print PDF + wait_for_new_pdf
        
        if not pdf_path:
            print("Failed to download PDF")
            return
        
        text = extract_text_from_pdf(pdf_path)

        engine = PdfLLMEngine()
        engine.set_document(text)

        bot.fill_form(engine)            # answer questions + submit
    finally:
        bot.close()


if __name__ == "__main__":
    main()