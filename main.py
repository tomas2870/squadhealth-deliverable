from webdriver import BrowserBot 
from pdf_llm_engine import PdfLLMEngine
from pdf_processor import extract_text_from_pdf

def main():
    bot = BrowserBot()
    try:
        bot.start_session()              # navigate + bypass
        pdf_path = bot.obtain_pdf()      # click Print PDF + wait_for_new_pdf
        text = extract_text_from_pdf(pdf_path)

        engine = PdfLLMEngine()
        engine.set_document(text)

        bot.fill_form(engine)            # answer questions + submit
    finally:
        bot.close()

if __name__ == "__main__":
    main()