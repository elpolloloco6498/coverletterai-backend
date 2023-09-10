import openai
from shemas.coverletter import CreateCoverLetterSchema, CoverLetterSchema, Tone, Language
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
        If a required skill is not present in the resume you can say that you are a fast learner and that you will be excited about learning a new skill.
        The user will provide you with a resume and a job offer.
        The letter should be no more than one page.
        Limit the cover letter to four paragraphs.
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


def generate_cover_letter(cover_letter_schema: CreateCoverLetterSchema):
    cover_letter_text = gpt_generate_letter(cover_letter_schema)
    return CoverLetterSchema(
        text=cover_letter_text,
        tone=cover_letter_schema.tone,
        language=cover_letter_schema.language,
    )
