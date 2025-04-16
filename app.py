# app.py
import streamlit as st
import logging
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

# Import project modules
from config.settings import MAX_WORKERS, GROQ_API_KEY, GROQ_MODEL
from core.agent_factory import AgentFactory
from core.multidisciplinary_team import MultidisciplinaryTeam
from services.llm_service import LLMService
from utils.file_handler import FileHandler
from utils.logger import setup_logger

# Setup logging
logger = setup_logger("streamlit_app")

# Initialize session state
if "specialist_reports" not in st.session_state:
    st.session_state.specialist_reports = {}
if "final_diagnosis" not in st.session_state:
    st.session_state.final_diagnosis = None
if "processing" not in st.session_state:
    st.session_state.processing = False
if "selected_specialists" not in st.session_state:
    st.session_state.selected_specialists = ["cardiologist", "psychologist", "pulmonologist"]
if "api_key" not in st.session_state:
    st.session_state.api_key = GROQ_API_KEY

# App title and description
st.set_page_config(page_title="Medical AI Agent System", layout="wide")
st.title("Medical AI Agent System")
st.markdown("""
This application uses AI agents specializing in different medical fields to analyze
patient medical reports and provide a comprehensive assessment.
""")

# Sidebar
st.sidebar.title("Configuration")

# API Key Configuration
with st.sidebar.expander("API Configuration", expanded=True):
    api_key = st.text_input(
        "Groq API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Groq API key to enable the AI agents"
    )
    
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        os.environ["GROQ_API_KEY"] = api_key
        st.success("API key updated successfully!")

# Report selection
st.sidebar.subheader("Report Selection")

# Option to upload a new report
uploaded_file = st.sidebar.file_uploader(
    "Upload Medical Report",
    type=["txt", "md"],
    help="Upload a medical report file (txt or md format)"
)

# List sample reports
sample_reports_dir = os.path.join("data", "sample_reports")
sample_reports = []
if os.path.exists(sample_reports_dir):
    sample_reports = [f for f in os.listdir(sample_reports_dir) if os.path.isfile(os.path.join(sample_reports_dir, f))]

# Option to select from sample reports
if sample_reports:
    selected_sample = st.sidebar.selectbox(
        "Or select a sample report",
        options=[""] + sample_reports,
        help="Choose from pre-loaded sample reports"
    )
    
    if selected_sample:
        try:
            with open(os.path.join(sample_reports_dir, selected_sample), 'r', encoding='utf-8') as f:
                report_content = f.read()
                selected_report = selected_sample
        except Exception as e:
            st.error(f"Error loading sample report: {str(e)}")
            report_content = None
            selected_report = None
    else:
        report_content = None
        selected_report = None
else:
    selected_sample = None
    report_content = None
    selected_report = None

# Handle uploaded file
if uploaded_file is not None:
    try:
        report_content = uploaded_file.getvalue().decode("utf-8")
        selected_report = uploaded_file.name
    except Exception as e:
        st.error(f"Error reading uploaded file: {str(e)}")
        report_content = None
        selected_report = None

# Show report content if available
if report_content:
    with st.expander("View Report Content", expanded=False):
        st.text_area("Medical Report", report_content, height=400, disabled=True)

# Specialist selection
st.sidebar.subheader("Select Medical Specialists")
available_specialists = list(AgentFactory.AGENT_REGISTRY.keys())

# Allow selection of specialists
selected_specialists = []
for specialist in available_specialists:
    if st.sidebar.checkbox(specialist.capitalize(), value=specialist in st.session_state.selected_specialists):
        selected_specialists.append(specialist)

# Update session state
st.session_state.selected_specialists = selected_specialists

# Advanced settings
with st.sidebar.expander("Advanced Settings"):
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    max_tokens = st.slider("Max Tokens", min_value=256, max_value=4096, value=1024, step=256)

# Function to run analysis in parallel
def run_specialist_analysis(report_content):
    """Run specialist analysis in parallel and update session state."""
    st.session_state.processing = True
    st.session_state.specialist_reports = {}
    st.session_state.final_diagnosis = None
    
    # Create shared LLM service for all agents
    llm_service = LLMService()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Update progress
    def update_progress(i, total, text):
        progress = int((i / total) * 100)
        progress_bar.progress(progress)
        status_text.text(text)
    
    try:
        # Create and run specialist agents in parallel
        results = {}
        agents = []
        
        # Create the agents
        for i, specialist_type in enumerate(selected_specialists):
            update_progress(i, len(selected_specialists) + 1, f"Creating {specialist_type} agent...")
            agent = AgentFactory.create_agent(
                agent_type=specialist_type,
                llm_service=llm_service,
                temperature=temperature,
                max_tokens=max_tokens
            )
            agents.append((specialist_type, agent))
        
        # Create a thread pool and run the agents
        with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(selected_specialists))) as executor:
            # Submit all tasks
            future_to_specialist = {
                executor.submit(agent.analyze, report_content): specialist_type 
                for specialist_type, agent in agents
            }
            
            # Process results as they complete
            for i, future in enumerate(as_completed(future_to_specialist)):
                specialist_type = future_to_specialist[future]
                update_progress(i, len(selected_specialists), f"Processing {specialist_type} analysis...")
                
                try:
                    result = future.result()
                    results[specialist_type] = result
                except Exception as e:
                    logger.error(f"Error in {specialist_type} analysis: {str(e)}")
                    results[specialist_type] = f"Error: {str(e)}"
        
        # Update session state with specialist reports
        st.session_state.specialist_reports = results
        
        # Run multidisciplinary team analysis if we have at least 2 specialist reports
        if len(results) >= 2:
            update_progress(len(selected_specialists), len(selected_specialists) + 1, "Running multidisciplinary analysis...")
            
            team_agent = MultidisciplinaryTeam(
                specialist_reports=results,
                llm_service=llm_service,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            final_diagnosis = team_agent.analyze()
            st.session_state.final_diagnosis = final_diagnosis
            
            # Save the final diagnosis to file
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            diagnosis_filename = f"diagnosis_{timestamp}"
            FileHandler.save_result(
                data={
                    "timestamp": timestamp,
                    "report": selected_report,
                    "specialist_reports": results,
                    "final_diagnosis": final_diagnosis
                },
                filename=diagnosis_filename,
                format_type="json"
            )
            
            # Also save a text-only version for easy reading
            FileHandler.save_result(
                data=f"Final Diagnosis ({timestamp}):\n\n{final_diagnosis}",
                filename=f"{diagnosis_filename}_text",
                format_type="txt"
            )
        
        # Complete progress
        update_progress(1, 1, "Analysis complete!")
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        st.error(f"An error occurred during analysis: {str(e)}")
    
    finally:
        st.session_state.processing = False

# Main content area
main_col1, main_col2 = st.columns(2)

# Display the analysis button
with main_col1:
    st.subheader("Run Analysis")
    
    if not st.session_state.api_key:
        st.warning("Please enter your Groq API key to enable the AI agents.")
    
    if not selected_specialists:
        st.warning("Please select at least one medical specialist.")
    
    if not report_content:
        st.warning("Please upload a medical report or select a sample report.")
    
    if st.button(
        "Analyze Medical Report",
        disabled=not (report_content and selected_specialists and st.session_state.api_key) or st.session_state.processing
    ):
        run_specialist_analysis(report_content)

# Display results
if st.session_state.specialist_reports:
    # Display specialist reports
    st.header("Specialist Reports")
    
    for specialist, report in st.session_state.specialist_reports.items():
        with st.expander(f"{specialist.capitalize()} Assessment", expanded=True):
            st.markdown(report)
    
    # Display final diagnosis if available
    if st.session_state.final_diagnosis:
        st.header("Final Diagnosis")
        st.markdown(st.session_state.final_diagnosis)
        
        # Option to download the results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_json = {
            "timestamp": timestamp,
            "report": selected_report,
            "specialist_reports": st.session_state.specialist_reports,
            "final_diagnosis": st.session_state.final_diagnosis
        }
        
        st.download_button(
            label="Download Results (JSON)",
            data=json.dumps(results_json, indent=2),
            file_name=f"medical_analysis_{timestamp}.json",
            mime="application/json"
        )

# About section
with st.expander("About this Application", expanded=False):
    st.markdown("""
    # Medical AI Agent System
    
    This application demonstrates the use of AI agents with medical specializations to analyze patient reports. Each agent focuses on their area of expertise and contributes to a comprehensive assessment.
    
    ## How it Works
    
    1. **Enter your Groq API key** in the configuration section
    2. **Upload a medical report** or select from sample reports
    3. **Choose which specialists** should analyze the report
    4. **Run the analysis** to get specialist assessments and a final diagnosis
    5. **Review and download** the results
    
    ## Specialists
    
    - **Cardiologist**: Focuses on heart-related issues and cardiovascular health
    - **Psychologist**: Assesses psychological and mental health factors
    - **Pulmonologist**: Evaluates respiratory system and lung-related concerns
    
    ## Technology
    
    This application uses the Llama 4 large language model from Groq to power the AI agents.
    """)

# Add a footer
st.markdown("""
---
**Medical AI Agent System** | This is a demonstration application and should not be used for actual medical diagnosis.
""")