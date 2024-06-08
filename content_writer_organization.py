import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.agents import load_tools
from langchain.agents import tool
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
                            temperature = 0.8,
                            google_api_key=GOOGLE_API_KEY)


# Set groq as llm
#llm = ChatGroq(groq_api_key=GROQ_API_KEY,model_name="Llama3-8b-8192")


def manager():
     with st.form("Manager"):  # Ensure `st.form` is within the expander
        goal_manager = st.text_area('Manager:', 'Define about his goal like "Lead the team in creating effective content writing etc..."')
        backstory_manager = st.text_area('Manager Backstory:', 'Tell something about him like "A seasoned Chief Marketing Officer with a keen eye for standout content creation."')
        submitted1 = st.form_submit_button("Submit Details")

        if submitted1:
            # Process form 1 data
            st.session_state["goal_manager"] = goal_manager
            st.session_state["backstory_manager"] = backstory_manager
            # Call the processing function
            #process_form_data(form_type="Marketing_strategist")  # Pass form identifier

            st.success(f"Thanks goals are {goal_manager}! backstory is {backstory_manager}.")

def reviewer():
     with st.form("reviewer"):  # Ensure `st.form` is within the expander
        goal_reviewer = st.text_area('Reviewer Goals:', 'Define about his goal like "Critique and refine all types of content like email, blog, articles, papers, etc..."')
        backstory_reviewer = st.text_area('Reviewer Backstory:', "A professional copywriter with a wealth of experience in persuasive content writing.")
        submitted1 = st.form_submit_button("Submit Details")

        if submitted1:
            # Process form  data
            st.session_state["goal_reviewer"] = goal_reviewer
            st.session_state["backstory_reviewer"] = backstory_reviewer
            # Call the processing function
            #process_form_data(form_type="reviewer")  # Pass form identifier
            st.success(f"Thanks goals are {goal_reviewer}! backstory is {backstory_reviewer}.")


def writer():
     with st.form("writer"):  # Ensure `st.form` is within the expander
        goal_writer = st.text_area('Content Writer Goals:', 'Define about his goal like "Craft concise and engaging content like email, blog, articles, papers, etc..."')
        backstory_writer = st.text_area('Content Writer Backstory:',"Experienced in writing impactful and awesome Content..")
        submitted1 = st.form_submit_button("Submit Details")

        if submitted1:
            # Process form  data
            st.session_state["goal_writer"] = goal_writer
            st.session_state["backstory_writer"] = backstory_writer
            # Call the processing function
            #process_form_data(form_type="reviewer")  # Pass form identifier
            st.success(f"Thanks goals are {goal_writer}! backstory is {backstory_writer}.")



def task():
     with st.form("Task"):  # Ensure `st.form` is within the expander
        task_description = st.text_area('Provide Task Description in steps:','Like: Detailed description of task, atleast give a description in 500 words, try to write it in steps' )
        expected_output = st.text_area('Write the expected output:', 'Like: Two final, revised article variations on topic "Health and Fitness".')
        submitted1 = st.form_submit_button("Submit Details")

        if submitted1:
            # Process form  data
            st.session_state["task_description"] = task_description
            st.session_state["expected_output"] = expected_output
            # Call the processing function
            #process_form_data(form_type="reviewer")  # Pass form identifier
            st.success(f"Thanks task description is {task_description}! expected output is {expected_output}.")






st.title("Multiple agents to solve your problems")


#form2()
task()
manager()
reviewer()
writer()



#create searches
@tool('DuckDuckGoSearch')
def search(search_query:str):
    """Search the web for information on given topic""" 
    return DuckDuckGoSearchRun().run(search_query)

# Define Agents

writer = Agent(
    role='Professional Content Writer',
    goal=st.session_state["goal_writer"],
    backstory=st.session_state["backstory_writer"],
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools = [search],
)

manager = Agent(
    role='Manager',
    goal=st.session_state["goal_manager"],
    backstory=st.session_state["backstory_manager"],
    verbose=True,
    allow_delegation=True,
    llm=llm
)

reviewer = Agent(
    role='Content Specialist',
    goal=st.session_state["goal_reviewer"],
    backstory=st.session_state["backstory_reviewer"],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define Task
given_task = Task(
    description=st.session_state["task_description"],
    agent=manager,  # The Marketing Strategist is in charge and can delegate,
    expected_output=st.session_state["expected_output"] # Define the expected output

)


# Create a Single Crew
email_crew = Crew(
    agents=[writer, manager, reviewer],
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












