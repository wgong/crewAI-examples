"""
see YouTube video: https://www.youtube.com/watch?v=_5_QHE3p8EA

## Setup
conda create -n crewai python=3.11

#export OPENAI_API_KEY="<>"

export OPENAI_API_BASE='http://localhost:11434/v1'
export OPENAI_MODEL_NAME='mistral'
export OPENAI_API_KEY=''


pip install crewai==0.28.8 crewai_tools==0.1.6 langchain_community==0.0.29

## How to run

conda activate crewai
cd ~/projects/wgong/crewAI-examples/ollama
python3 main.py

output: main.log

"""

# Warning control
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

model_name = "mistral"
model_name = "llama3"

## LLM
llm = ChatOpenAI(
    model = model_name,
    base_url = "http://localhost:11434/v1",
    openai_api_key='NA'
)
    
    
## Agents:
legal_researcher_agent = Agent(
    role="Legal Research Specialist",
    goal="Provide accurate and relevant legal information",
    backstory=(
        "You work at a law firm and are tasked with "
        "conducting research for a case involving {topic}. "
        "Your expertise will help the legal team build a strong argument."
    ),
    allow_delegation=False,
    verbose=True,
    llm = llm
)

legal_writer_agent = Agent(
    role="Legal Document Drafter",
    goal="Craft clear and persuasive legal documents",
    backstory=(
        "You are a legal writer responsible for drafting "
        "a legal brief on {topic} for an upcoming court case. "
        "Your document must be well-researched, concise, and compelling."
    ),
    verbose=True,
    allow_delegation=False,
    llm = llm
)



# Tasks:
conduct_legal_research = Task(
    description=(
        "1. Investigate relevant laws, regulations, and precedents.\n"
        "2. Analyze legal articles, journals, and expert opinions.\n"
        "3. Identify key points and arguments related to {topic}.\n"
        "4. Organize and summarize findings in a clear and concise manner."
    ),
    expected_output=(
        "A comprehensive legal research report "
        "including relevant sources and key points."
    ),
    agent=legal_researcher_agent,
)

draft_legal_brief = Task(
    description=(
        "1. Use the research report to draft a clear and persuasive brief.\n"
        "2. Include an introduction, argument, and conclusion.\n"
        "3. Ensure the brief is well-structured and easy to follow.\n"
        "4. Proofread for grammar, punctuation, and legal accuracy."
    ),
    expected_output=(
        "A well-written legal brief in markdown format, "
        "ready for submission to the legal team."
    ),
    agent=legal_writer_agent,
)

crew = Crew(
    agents=[legal_researcher_agent, legal_writer_agent],
    tasks=[conduct_legal_research, draft_legal_brief],
    verbose=2
)


result = crew.kickoff(inputs={"topic": "Employment Law and Discrimination"})

print(result)

file_output = f"crewai-{model_name}.md"
with open(file_output, "w") as f:
    f.write(result)
