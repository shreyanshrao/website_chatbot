# Website Chatbot with Gemini API

A Python-based chatbot that scrapes content from websites and answers questions using Google's Gemini API.

## Features

- 🌐 Web scraping using BeautifulSoup
- 🤖 AI-powered responses using Gemini API
- 💬 Interactive console interface
- 🔄 Support for multiple websites in one session
- ⚡ Fast and efficient content processing

## Prerequisites

- Python 3.7 or higher
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

## Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure your Gemini API key (choose one method):

**Method 1: Set directly in code (Easiest)**
- Open `chatbot.py` and edit line 16
- Replace `'YOUR_API_KEY_HERE'` with your actual API key:
  ```python
  GEMINI_API_KEY = 'your-api-key-here'
  ```

**Method 2: Use environment variable**

**Linux/Mac:**
```bash
export GEMINI_API_KEY='your-api-key-here'
```

**Windows:**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Method 3: Enter when prompted**
- If no API key is found, the program will prompt you to enter it
- Note: This method requires entering the key each time you run the program

## Usage

Run the chatbot:
```bash
python chatbot.py
```

Follow the prompts:
1. Enter a website URL when prompted
2. Ask questions about the website content
3. Type `quit` or `exit` to end the session
4. Type `new_url` to scrape a different website

## Example

```
Enter website URL to scrape: https://example.com
Website content loaded successfully!

You: What is this website about?
Chatbot: [Response based on website content]

You: What are the main features?
Chatbot: [Response based on website content]

You: quit
Thank you for using the chatbot. Goodbye!
```

## Project Structure

```
relinns/
├── chatbot.py                 # Main chatbot script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── STEP_BY_STEP_PROCESS.md   # Detailed implementation documentation
```

## Dependencies

- `requests`: HTTP library for fetching web pages
- `beautifulsoup4`: HTML parsing library
- `google-generativeai`: Google Gemini API SDK

## Notes

- The chatbot extracts and uses the first 5000 characters of website content
- Some websites may block automated requests
- Ensure you have a stable internet connection

## License

This project is created for assessment purposes.
