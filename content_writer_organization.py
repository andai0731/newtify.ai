import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.agents import load_tools
from crewai_tools import tool
from langchain_groq import ChatGroq


import os

from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("groq_api_key")
#Set gemini pro as llm
llm = ChatGoogleGenerativeAI(model="gemini-pro",
                            verbose = True,
                            temperature = 0.5,
                            google_api_key=GOOGLE_API_KEY)


# Set groq as llm
#llm = ChatGroq(groq_api_key=GROQ_API_KEY,model_name="Llama3-8b-8192")


def marketing_strategist():
     with st.form("Marketing_strategist"):  # Ensure `st.form` is within the expander
        goal_marketing_strategist = st.text_area('Marketing Strategist Goals:', 'Define about his goal like "Lead the team in creating effective content marketing etc..."')
        backstory_marketing_strategist = st.text_area('Marketing Strategist Backstory:', 'Tell something about him like "A seasoned Chief Marketing Officer with a keen eye for standout marketing content."')
        submitted1 = st.form_submit_button("Submit Details")

        if submitted1:
            # Process form 1 data
            st.session_state["goal_marketing_strategist"] = goal_marketing_strategist
            st.session_state["backstory_marketing_strategist"] = backstory_marketing_strategist
            # Call the processing function
            #process_form_data(form_type="Marketing_strategist")  # Pass form identifier

            st.success(f"Thanks goals are {goal_marketing_strategist}! backstory is {backstory_marketing_strategist}.")

def content_specialist():
     with st.form("content_specialist"):  # Ensure `st.form` is within the expander
        goal_content_specialist = st.text_area('Content Specialist Goals:', 'Define about his goal like "Critique and refine all types of content like email, blog, articles, papers, etc..."')
        backstory_content_specialist = st.text_area('Content Specialist Backstory:', 'Tell something about him like "A professional copywriter with a wealth of experience in persuasive writing."')
        submitted1 = st.form_submit_button("Submit Details")

        if submitted1:
            # Process form  data
            st.session_state["goal_content_specialist"] = goal_content_specialist
            st.session_state["backstory_content_specialist"] = backstory_content_specialist
            # Call the processing function
            #process_form_data(form_type="content_specialist")  # Pass form identifier
            st.success(f"Thanks goals are {goal_content_specialist}! backstory is {backstory_content_specialist}.")


def content_writer():
     with st.form("content_writer"):  # Ensure `st.form` is within the expander
        goal_content_writer = st.text_area('Content Writer Goals:', 'Define about his goal like "Craft concise and engaging content like email, blog, articles, papers, etc..."')
        backstory_content_writer = st.text_area('Content Writer Backstory:', 'Tell something about him like "Experienced in writing impactful and awesome Content.."')
        submitted1 = st.form_submit_button("Submit Details")

        if submitted1:
            # Process form  data
            st.session_state["goal_content_writer"] = goal_content_writer
            st.session_state["backstory_content_writer"] = backstory_content_writer
            # Call the processing function
            #process_form_data(form_type="content_specialist")  # Pass form identifier
            st.success(f"Thanks goals are {goal_content_writer}! backstory is {backstory_content_writer}.")



def task():
     with st.form("Task"):  # Ensure `st.form` is within the expander
        task_description = st.text_area('Provide Task Description in steps:','Like: sDetailed description of task, atleast give a description in 100 words' )
        expected_output = st.text_area('Write the expected output:', 'Like: Two final, revised cold email variations promoting a ai plugin platform &ai solution.')
        submitted1 = st.form_submit_button("Submit Details")

        if submitted1:
            # Process form  data
            st.session_state["task_description"] = task_description
            st.session_state["expected_output"] = expected_output
            # Call the processing function
            #process_form_data(form_type="content_specialist")  # Pass form identifier
            st.success(f"Thanks task description is {task_description}! expected output is {expected_output}.")






st.title("Multiple Forms on One Page")


#form2()
task()
marketing_strategist()
content_specialist()
content_writer()



#create searches
@tool('DuckDuckGoSearch')
def search(search_query:str):
    """Search the web for information on given topic""" 
    return DuckDuckGoSearchRun().run(search_query)

# Define Agents

writer = Agent(
    role='Professional Content Writer',
    goal=st.session_state["goal_content_writer"],
    backstory=st.session_state["backstory_content_writer"],
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools = [search],
)

strategist = Agent(
    role='Marketing Strategist',
    goal=st.session_state["goal_marketing_strategist"],
    backstory=st.session_state["backstory_marketing_strategist"],
    verbose=True,
    allow_delegation=True,
    llm=llm
)

specialist = Agent(
    role='Content Specialist',
    goal=st.session_state["goal_content_specialist"],
    backstory=st.session_state["backstory_content_specialist"],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define Task
given_task = Task(
    description=st.session_state["task_description"],
    agent=strategist,  # The Marketing Strategist is in charge and can delegate,
    expected_output=st.session_state["expected_output"] # Define the expected output

)


# Create a Single Crew
email_crew = Crew(
    agents=[writer, strategist, specialist],
    tasks=[given_task],
    verbose=True,
    process=Process.sequential
)

# Execution Flow
#print("Crew: Working on Email Task")
#emails_output = email_crew.kickoff()



#st.write(emails_output = email_crew.kickoff())
st.info(email_crew.kickoff())
#st.write(f"The info is that the goal of marketing strategist id {st.session_state["form1_name"]} & back story is {st.session_state["form1_email"]}.")

st.stop()












