# Medical AI Agent System

A sophisticated AI-powered medical analysis system that employs specialized agents to provide comprehensive healthcare assessments. This system uses multiple AI agents, each specializing in different medical fields, to analyze patient reports and generate detailed medical assessments.

## 🌟 Features

- **Specialized Medical Agents**: Multiple AI agents specializing in different medical fields:
  - Cardiologist: Heart and cardiovascular health
  - Psychologist: Mental health and psychological factors
  - Pulmonologist: Respiratory system and lung health
  - Customizable: Easy to add new specialist agents

- **Multidisciplinary Analysis**: Combines insights from multiple specialists to provide comprehensive assessments
- **Interactive Web Interface**: User-friendly Streamlit interface for easy interaction
- **Secure API Integration**: Safe handling of API keys and medical data
- **Sample Reports**: Pre-loaded sample medical reports for testing
- **Export Capabilities**: Download analysis results in JSON and text formats

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Groq API key (for LLM access)
- Required Python packages (listed in requirements.txt)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/healthcare_agent.git
cd healthcare_agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
LOG_LEVEL=INFO
MAX_WORKERS=3
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

## 💡 Usage Guide

1. **API Configuration**
   - Enter your Groq API key in the configuration section
   - The key is securely stored in the session

2. **Report Selection**
   - Upload your own medical report (txt or md format)
   - Or select from pre-loaded sample reports
   - View the report content before analysis

3. **Specialist Selection**
   - Choose which medical specialists should analyze the report
   - Select one or more specialists based on the case

4. **Analysis**
   - Click "Analyze Medical Report" to start the process
   - View real-time progress of the analysis
   - Get detailed assessments from each specialist
   - Receive a comprehensive multidisciplinary diagnosis

5. **Results**
   - View individual specialist reports
   - See the final multidisciplinary diagnosis
   - Download results in JSON or text format

## 🛠️ Technical Architecture

- **Core Components**:
  - Base Agent System
  - Specialist Agents
  - Multidisciplinary Team
  - LLM Service Integration
  - File Management System

- **Key Technologies**:
  - Streamlit for web interface
  - Groq API for LLM access
  - Concurrent processing for parallel analysis
  - Secure file handling

## 📁 Project Structure

```
healthcare_agent/
├── agents/               # Specialist agent implementations
├── config/              # Configuration files
├── core/                # Core system components
├── data/                # Data storage
│   ├── results/        # Analysis results
│   └── sample_reports/ # Sample medical reports
├── services/            # Service implementations
├── templates/           # Prompt templates
├── utils/               # Utility functions
├── app.py              # Main application
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

## 🔧 Customization

### Adding New Specialists

1. Create a new agent class in `agents/`:
```python
from core.agent_base import BaseAgent

class NewSpecialist(BaseAgent):
    def _get_role(self) -> str:
        return "NewSpecialist"
```

2. Add a prompt template in `templates/`:
```
Act like a [specialist]. You will receive a patient's report.

Task: [specific analysis task]
Focus: [specialized focus areas]
Recommendation: [recommendation format]

Patient's Report:
medical_report
```

3. Register the agent in `core/agent_factory.py`

## ⚠️ Important Notes

- This is a demonstration application and should not be used for actual medical diagnosis
- Always consult qualified healthcare professionals for medical advice
- Keep your API keys secure and never share them
- Patient data should be handled according to relevant privacy regulations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue in the repository. 