import datetime

import openai
from sqlalchemy.orm import Session

from services.letters import add_letter
from services.parsing import parse_data_job_offer
from services.users import get_user, add_user_credit
from shemas.coverletter import CreateCoverLetterSchema, CoverLetterSchema, Tone, Language
from shemas.letters import CreateLetterSchema

# os get env
openai.api_key = "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"


def generate_dummy_cover_letter() -> CoverLetterSchema:
    cover_letter_text = """
    [Your Name] [Your Address] [City, State ZIP Code] [Email Address] [Phone Number] [Date] [Employer's Name] [Company Name] [Company Address] [City, State ZIP Code] Dear [Employer's Name], I am writing to express my strong interest in the position of Software Engineer at [Company Name], as advertised in the job offer on [Source of Job Offer]. With a solid background in software development and proficiency in various programming languages and technologies, I am confident that my skills and experiences align well with the requirements of this role. As stated in the job offer, [Company Name] values collaboration, trust, and technical expertise in order to develop cutting-edge solutions. Throughout my professional experiences, I have consistently demonstrated these qualities. In my most recent role as a Software Engineer at Wiremind Cargo, I developed the cargo management application Cargostack using Python, SQL Alchemy, Angular, and Docker. 
    This experience allowed me to collaborate effectively with cross-functional teams and deliver high-quality software solutions. 
    
    Additionally, my internship at Banque de France involved developing Python applications to automate repetitive tasks for agents, showcasing my attention to detail and problem-solving skills.
    
    Furthermore, my internship at Quadrille Ingénierie provided me with hands-on experience in creating software solutions for automating end-to-end content transmissions. 
    This allowed me to strengthen my expertise in Python, Javascript, Selenium, and Linux, and further develop my skills in testing and quality assurance. 
    
    In terms of education, I hold a Master's degree in Engineering from IMT Nord Europe, specializing in computer development. 
    My coursework covered a wide range of topics including data structures, algorithms, databases, and APIs. Additionally, my semester abroad at Politechnika Wroclaw in Poland further enhanced my knowledge in software development and electrical engineering. 
    I am particularly excited about the opportunity to work within the Simulation and Modeling department at [Company Name]. Developing and integrating missile reference dynamic models aligns perfectly with my passion for innovative technologies and problem-solving. 
    I am confident that my strong foundation in C/C++, Python, and Linux, as well as my experience in software validation and simulation, make me a perfect fit for the requirements of this role.
    
    Beyond technical skills, I am also fluent in English (C1 level) and have a strong interest in the defense industry. These qualities, combined with my ability to work effectively in multidisciplinary teams, allow me to contribute to the overall success of [Company Name]. 
    I would welcome the opportunity to further discuss my qualifications and how I can contribute to the success of [Company Name]. Thank you for considering my application. I look forward to the possibility of joining your team and contributing to the mission of ensuring the sovereignty of our nations and the freedom of democracies. 
    
    Yours sincerely, [Your Name]
    """
    return CoverLetterSchema(
            text=cover_letter_text,
            tone=Tone.formal,
            language=Language.english,
        )


def gpt_generate_letter(cover_letter_schema: CreateCoverLetterSchema):
    context_prompt = """
        You are a cover letter writing expert.
        Your job is to write a cover letter based on the resume of the user and a job offer description.
        You will respond to the job offer by showing that your skills and qualities matches with the job.
        This is how I want you to structure the cover letter, you have to following this writing method:
        - start with a greeting
        - In the first paragraph, mention the job title you're applying for and where you saw the position posting. 
        Explain your interest in the role and company to show you've done your research. 
        The first section of your cover letter is also the first impression the reader will have of you, so it's important to appeal to that person quickly and succinctly.
        - Your second paragraph should be a brief overview of your background as it relates to the position. 
        Include key achievements, skills and specialties that make you particularly suited to the position.
        Focus on one or two and provide specific details about your success, including measurable impacts you made.
        Pay close attention to keywords listed in the job description and include those you identify with in the body of your cover letter. 
        You should only include information about your most recent professional experiences.
        - The closing paragraph should focus on another key achievement or skill relevant to the position.
        Instead of repeating details from your resume, summarize a specific story or anecdote that displays you're right for the role.
        If you're changing careers, this is a good opportunity to talk about transferable skills or relatable experiences from your career.
        - You should end your cover letter with a paragraph summarizing why you are applying for the role and why you would be a great fit.
        Keep the cover letter conclusion brief and explain that you look forward to the employer's response about possible next steps.
        End with your signature at the bottom.
        Do not include the address of the recipient and sender.
        Do not include the date.
        """
    user_prompt = f"""
        resume: {cover_letter_schema.resume_text}
        job offer: {cover_letter_schema.job_text}
        Please use the following tone throughout the letter: {cover_letter_schema.tone}
        Write the letter in the following language: {cover_letter_schema.language}
        """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return response["choices"][0]["message"]["content"]


def generate_cover_letter(session: Session, cover_letter_schema: CreateCoverLetterSchema):
    user = get_user(session, id=cover_letter_schema.user_id)
    if user.credits > 0:
        cover_letter_text = gpt_generate_letter(cover_letter_schema)
        # extract job data from resume text
        extract_job_data = parse_data_job_offer(cover_letter_schema.job_text)
        print(extract_job_data)
        letter_schema = CreateLetterSchema(
            company_name=extract_job_data.company_name,
            job_title=extract_job_data.job_title,
            language=cover_letter_schema.language.value,
            writing_style=cover_letter_schema.tone.value,
            generation_date=datetime.date.today(),
            text=cover_letter_text,
        )
        # add letter to history
        add_letter(session, user.id, letter_schema)
        add_user_credit(session, user.id, -1)
        session.commit()
        return CoverLetterSchema(
            text=cover_letter_text,
            tone=cover_letter_schema.tone,
            language=cover_letter_schema.language,
        )
    return {"error": "not enough credits", "error_type": "no_credits"}
