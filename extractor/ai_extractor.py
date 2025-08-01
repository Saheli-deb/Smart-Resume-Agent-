import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

# Load OpenAI key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment. Please check your .env file.")

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0.0,
    model="gpt-4"  # Or "gpt-3.5-turbo" if you're on free tier
)

PROMPT_TEMPLATE = """
You are an AI resume analyzer. Extract the following from the given resume:
- Name
- Email
- Phone
- Education (schooling, college, degree, year, CGPA)
- Skills
- Projects
- Certifications
- Internships / Work experience
- Domain of expertise
Return your response in clean JSON format.
Resume text:
{text}
"""

def extract_resume_data(text):
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    message = HumanMessage(content=prompt.format(text=text))
    response = llm([message])
    return response.content
