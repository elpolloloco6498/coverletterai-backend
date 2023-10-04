import json

import openai
from PyPDF2 import PdfReader

from shemas.letters import JobData


def extract_text_from_pdf(byte_file) -> str:
    reader = PdfReader(byte_file)
    page = reader.pages[0]
    return page.extract_text()


def parse_data_job_offer(job_offer_text: str) -> JobData:
    context_prompt = """
        You are a professional parser.
        your role is to analyse the text of a job offer and find the company name and the job title.
        You will return to the user the following data in this form:
        {
            "company_name": actual_company_name,
            "job_title": actual_job_title,
        }
        """
    user_prompt = f"""
        job offer: {job_offer_text}
        """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    job_data = json.loads(response["choices"][0]["message"]["content"])
    return JobData(company_name=job_data["company_name"], job_title=job_data["job_title"])
