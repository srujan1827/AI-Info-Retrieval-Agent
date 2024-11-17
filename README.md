# AI Agent Dashboard

This is an AI Agent Dashboard built with Streamlit that allows users to upload a CSV file or provide a Google Sheet URL containing entities (e.g., countries, companies, etc.). The app then performs web searches using SerpAPI and processes the results using the Groq API to extract concise information based on a custom query.

## Features

- Upload a CSV file or input a Google Sheet URL containing entities.
- Enter a custom query with placeholders for dynamic entity insertion.
- Perform web searches for each entity using SerpAPI.
- Process search results using the Groq API to extract concise answers.
- Download the final results as a CSV file.

## Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
- Accounts and API keys for:
  - [SerpAPI](https://serpapi.com/)
  - [Groq API](https://groq.com/)
  - [Google Cloud Platform](https://cloud.google.com/) for Google Sheets access

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

