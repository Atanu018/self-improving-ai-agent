# **Self-Improving AI Agent with Autonomous Skill Acquisition**

## **Overview**
This project implements a **Self-Improving AI Agent** that autonomously identifies knowledge gaps, learns from various sources (Wikipedia, Google Search, OpenAI, etc.), and refines its understanding. The agent features:
- **Knowledge Gap Detection**: Identifies missing knowledge using NLP models.
- **Autonomous Learning**: Searches Wikipedia & Google for information.
- **Adaptive Learning Strategies**: Uses contextual refinement to improve accuracy.
- **User Interface (UI)**: Interactive web interface for querying & feedback.

---

## **Features**
✔️ Retrieves knowledge from **Wikipedia & Google Search**  
✔️ **Detects & tracks knowledge gaps** over time  
✔️ Uses **Sentence Transformers** for semantic analysis  
✔️ UI for **real-time user interaction**  
✔️ Supports **adaptive learning cycles** for continuous improvement  

---

## **Project Structure**
```
self-improving-ai-agent/
│── backend/                     # Core AI logic & learning modules
│   ├── app.py                   # Flask backend for API
│   ├── knowledge_gap.py         # Knowledge gap detection
│   ├── adaptive_learning.py      # Adaptive learning logic
│   ├── google_search.py         # Google Search integration
│   ├── wikipedia_fetcher.py     # Wikipedia API integration
│   ├── requirements.txt         # Dependencies
│   ├── config.py                # Configuration settings
│── frontend/                     # UI & Frontend assets
│   ├── index.html               # Web-based UI
│   ├── static/
│   │   ├── styles.css           # UI Styling
│   │   ├── script.js            # Frontend JS
│── logs/                         # Log files
│── README.md                     # Documentation
│── .env                           # API Keys (DO NOT COMMIT)
│── run.sh                        # Script to start the app
```

---

## **Installation**
### **Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/self-improving-ai-agent.git
cd self-improving-ai-agent
```

### **Step 2: Install Dependencies**
```bash
pip install -r backend/requirements.txt
```

### **Step 3: Set Up API Keys**
- **Google Search API** (optional but recommended)
- **OpenAI API** (for LLM-based learning)

Create a `.env` file and add:
```
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
```

### **Step 4: Run the Backend**
```bash
python backend/app.py
```
The backend should start at `http://127.0.0.1:5000/`

### **Step 5: Run the Frontend**
- Open `frontend/index.html` in a browser.
- Query the agent and review responses.

---

## **Usage**
1. Enter a **query** in the UI.
2. The agent searches Wikipedia/Google.
3. If knowledge gaps exist, it **learns & refines** the query.
4. Results are displayed, and the agent **updates its knowledge base**.

---

## **Deployment**
To deploy on **Heroku, AWS, or GCP**:
- Use **Flask for backend API**
- Host the **frontend on GitHub Pages or Netlify**
- Store API keys in **environment variables**

---

## **Future Enhancements**
📌 **Integrate ArXiv, PubMed, or news sources** for real-time updates  
📌 **Improve UI/UX** with a chatbot-style interface  
📌 **Fine-tune LLM-based learning** for better results  

---

## **Contributing**
Feel free to open an **issue** or submit a **pull request**!

---

## **License**
MIT License  

---

## **How to Get Google Search API Key?**

### **Step 1: Create a Google Cloud Project**
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Select a project** > **New Project**.
3. Name your project and click **Create**.

### **Step 2: Enable Custom Search API**
1. Open [Google Custom Search API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com).
2. Click **Enable API**.

### **Step 3: Get API Key**
1. Go to [Google API Credentials](https://console.cloud.google.com/apis/credentials).
2. Click **Create Credentials** > **API Key**.
3. Copy the **API Key** and add it to your `.env` file.

---
