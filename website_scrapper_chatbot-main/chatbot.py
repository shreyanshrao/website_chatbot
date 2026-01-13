#!/usr/bin/env python3
"""
Website Chatbot using Gemini API
This chatbot scrapes content from a given website URL and uses Gemini API
to answer questions based on the scraped content.
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from typing import Optional


GEMINI_API_KEY = ''


class WebsiteChatbot:
    """A chatbot that interacts with website content using Gemini API."""
    
    def __init__(self, api_key: str):
        """
        Initialize the chatbot with Gemini API key.
        
        Args:
            api_key: Google Gemini API key
        """
        if not api_key:
            raise ValueError("API key is required. Please set GEMINI_API_KEY environment variable.")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        # Use gemini-1.5-flash for faster responses, or gemini-1.5-pro for better quality
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.website_content = None
        self.website_url = None
    
    def scrape_website(self, url: str) -> str:
        """
        Scrape content from the given website URL.
        
        Args:
            url: Website URL to scrape
            
        Returns:
            Extracted text content from the website
        """
        try:
            print(f"Fetching content from: {url}")
            
            # Set headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Fetch the webpage
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "meta", "link", "noscript"]):
                script.decompose()
            
            # Extract text content
            text_content = soup.get_text()
            
            # Clean up the text (remove extra whitespace)
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit content length to avoid token limits (keep first 5000 characters)
            if len(text_content) > 5000:
                text_content = text_content[:5000] + "... [Content truncated]"
            
            self.website_content = text_content
            self.website_url = url
            
            print(f"Successfully scraped {len(text_content)} characters from the website.")
            return text_content
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching website: {e}")
            raise
        except Exception as e:
            print(f"Error parsing website content: {e}")
            raise
    
    def process_question(self, question: str) -> str:
        """
        Process user question using Gemini API with website content as context.
        
        Args:
            question: User's question
            
        Returns:
            Response from Gemini API
        """
        if not self.website_content:
            return "Error: No website content loaded. Please scrape a website first."
        
        try:
            # Create a prompt with website content and user question
            prompt = f"""Based on the following website content, please answer the user's question.
If the answer cannot be found in the content, please say so.

Website URL: {self.website_url}

Website Content:
{self.website_content}

User Question: {question}

Please provide a helpful and accurate answer based on the website content:"""
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def start_chat(self):
        """Start an interactive console chat session."""
        print("\n" + "="*60)
        print("Website Chatbot - Powered by Gemini API")
        print("="*60)
        print("\nInstructions:")
        print("1. Enter a website URL to scrape")
        print("2. Ask questions about the website content")
        print("3. Type 'quit' or 'exit' to end the session")
        print("4. Type 'new_url' to scrape a different website")
        print("="*60 + "\n")
        
        # Get initial website URL
        url = input("Enter website URL to scrape: ").strip()
        
        if not url:
            print("No URL provided. Exiting.")
            return
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Scrape the website
        try:
            self.scrape_website(url)
            print("\nWebsite content loaded successfully!")
        except Exception as e:
            print(f"\nFailed to load website: {e}")
            return
        
        # Start chat loop
        print("\nYou can now ask questions about the website. Type 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nThank you for using the chatbot. Goodbye!")
                    break
                
                # Check for new URL command
                if user_input.lower() == 'new_url':
                    url = input("Enter new website URL: ").strip()
                    if not url:
                        print("No URL provided. Continuing with current website.")
                        continue
                    
                    if not url.startswith(('http://', 'https://')):
                        url = 'https://' + url
                    
                    try:
                        self.scrape_website(url)
                        print("New website content loaded successfully!")
                    except Exception as e:
                        print(f"Failed to load website: {e}")
                    continue
                
                # Process the question
                print("\nChatbot: ", end="", flush=True)
                response = self.process_question(user_input)
                print(response)
                print()  
                
            except KeyboardInterrupt:
                print("\n\nSession interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")


def main():
    """Main function to run the chatbot."""
    # Get API key with priority: 1) Code constant, 2) Environment variable, 3) User input
    api_key = None
    
    # Priority 1: Check if API key is set in code
    if GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_API_KEY_HERE':
        api_key = GEMINI_API_KEY
        print("Using API key from code configuration.")
    else:
        # Priority 2: Check environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            print("Using API key from environment variable.")
    
    # Priority 3: Prompt user to enter API key if not found
    if not api_key:
        print("\n" + "="*60)
        print("Gemini API Key Not Found")
        print("="*60)
        print("\nYou can set your API key in three ways:")
        print("1. Edit chatbot.py and set GEMINI_API_KEY at the top of the file")
        print("2. Set environment variable: export GEMINI_API_KEY='your-key'")
        print("3. Enter it now (will not be saved)")
        print("\nGet your API key from: https://makersuite.google.com/app/apikey")
        print("="*60 + "\n")
        
        api_key = input("Enter your Gemini API key (or press Ctrl+C to exit): ").strip()
        
        if not api_key:
            print("\nNo API key provided. Exiting.")
            sys.exit(1)
    
    # Create and start chatbot
    try:
        chatbot = WebsiteChatbot(api_key)
        chatbot.start_chat()
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
