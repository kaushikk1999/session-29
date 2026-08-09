import json, os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import date
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

from dotenv import load_dotenv

app = Flask(__name__, static_folder='static')
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Ensure Gemini is using the API key
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

# Load Knowledge Base
try:
    with open("data/knowledge_base.json") as f:
        KB = json.load(f).get("entries", [])
except Exception as e:
    print(f"Error loading KB: {e}")
    KB = []

# Tools
@tool
def calculator(expression: str) -> str:
    """Evaluate a simple arithmetic expression, e.g. '0.20 * 560'. Use for any maths."""
    try:
        allowed = set("0123456789+-*/(). ")
        if not set(expression) <= allowed:
            return "Error: only basic arithmetic is allowed."
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

@tool
def search_kb(topic: str) -> str:
    """Look up a company policy or fact in the internal knowledge base.
    Use for questions about VAT, leave, mileage, expenses, remote work or lost devices."""
    hits = [e for e in KB if topic.lower() in (e["topic"] + " " + e["text"]).lower()]
    if not hits:
        return "No matching entry found in the knowledge base."
    return hits[0]["text"]

@tool
def issue_refund(order_id: str, amount: float) -> str:
    """Issue a refund on an order. Moves real money."""
    # Mocking approval in the web UI for seamless interaction
    return f"Refund of £{amount:.2f} issued for {order_id}. (Mock auto-approved via web UI)"

@tool
def get_todays_date() -> str:
    """Return today's date in ISO format. Use when the user asks what today's date is."""
    return date.today().isoformat()

# Agent setup
tools = [calculator, search_kb, issue_refund, get_todays_date]
system_prompt = (
    "You are a helpful workplace assistant. Use the tools available to answer accurately. "
    "Use the calculator for any arithmetic. Use search_kb for company policy or facts. "
    "If you cannot answer from the tools, say so — do not guess."
)

agent = create_react_agent(llm, tools, prompt=system_prompt)

def extract_text(content):
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and 'text' in item:
                return item['text']
    elif isinstance(content, str):
        return content
    return str(content)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        result = agent.invoke({"messages": [HumanMessage(content=user_message)]})
        raw_content = result["messages"][-1].content
        clean_text = extract_text(raw_content)
        return jsonify({'response': clean_text})
    except Exception as e:
        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
            return jsonify({'error': 'API Rate limit exceeded. The API key has reached its quota limit.'}), 429
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
