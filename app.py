
import streamlit as st
from scraper import scrape_page
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO

def create_pdf(result):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    for item in result:
        if item["type"] == "text":
            story.append(Paragraph(item["content"], styles["BodyText"]))
            story.append(Spacer(1, 12))

        elif item["type"] == "image":
            story.append(Paragraph(
                f"Image URL: {item['content']}",
                styles["BodyText"]
            ))
            story.append(Spacer(1, 12))

    pdf.build(story)
    buffer.seek(0)
    return buffer.getvalue()




st.title("Webpage Scraper")

url = st.text_input("Enter website URL")

if st.button("Scrape"):
    if url:
        with st.spinner("Scraping webpage..."):
            try:
                result = scrape_page(url)

                for item in result:
                    if item["type"] == "text":
                        st.write(item["content"])

                    elif item["type"] == "image":
                        st.write("Image URL:", item["content"])
                pdf_data = create_pdf(result)

                st.write("PDF ready!")
                st.download_button(
                        label="Download PDF",
                        data=pdf_data,
                        file_name="scraped_content.pdf",
                        mime="application/pdf"
                        )

            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a website URL.")
