# Sunshine Shop AI

A business dashboard with an AI assistant, built in Python.

## What it does
- Shows total sales, cost and profit
- Shows a monthly chart and report table
- Lets you ask the AI questions about the business

## How the AI stays accurate
- It only answers from the business data
- It does not make up numbers or reasons
- Python does the profit calculations, not the AI

## Built with
Python, Streamlit, Ollama, Qwen 2.5

## How to run it
1. Install Ollama and run: ollama pull qwen2.5:3b
2. Run: pip install -r requirements.txt
3. Run: streamlit run app.py
