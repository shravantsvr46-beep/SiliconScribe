import os
from langchain_community.document_loaders import PyPDFLoader


def get_datasheet_context(mcu_name, query, api_key):

    pdf_path = os.path.join("docs", f"{mcu_name.lower()}_manual.pdf")

    if not os.path.exists(pdf_path):
        return "No datasheet available. Use general microcontroller knowledge."

    try:

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        context = "\n".join([doc.page_content for doc in docs[:3]])

        return context

    except Exception as e:
        return f"Error reading datasheet: {e}"