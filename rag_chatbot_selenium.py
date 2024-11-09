import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Function to get weather data for London
def get_weather(city="London"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=15262e37486f3096dbde755e321f1945&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data.get("cod") != 200:
        return "Sorry, couldn't fetch the weather information right now."
    
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    
    return f"The current weather in {city} is {temp}°C with {weather}."

# Function to get traffic data for London (Placeholder function)
def get_traffic():
    return "The current traffic in London is moderate with some delays on major routes."

# Function to get mayor information (Placeholder function)
def get_mayor():
    return "The current mayor of London is Sadiq Khan."

# Function to download Borough region crime data
def download_crime_data():
    chrome_options = Options()
    download_dir = "C:/path/to/your/download/folder"  # Specify your download directory
    prefs = {
        "download.default_directory": download_dir,  # Set download directory
        "download.prompt_for_download": False,  # Disable download prompt
        "directory_upgrade": True,
        "safebrowsing.enabled": True  # Allow downloads without prompt
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("start-maximized")

    # Initialize the Chrome driver with options
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://data.london.gov.uk/dataset/recorded_crime_summary"
    driver.get(url)
    time.sleep(5)  # Wait for page load

    try:
        # Find the download link and extract the href attribute
        download_button = driver.find_element(By.CSS_SELECTOR, "a.dp-resource__button")
        download_url = download_button.get_attribute("href")
        if download_url:
            driver.get(download_url)
            print("Navigated directly to the download URL for crime data.")
        else:
            print("Download URL not found.")
    except Exception as e:
        print("Error finding or clicking the download link:", e)
    finally:
        time.sleep(20)  # Adjust for download completion time
        driver.quit()

# Modified system prompt for handling "weather", "traffic", and "mayor" queries for London
system_prompt = """You are a helpful assistant that only provides information related to London. 
The user may ask for various information about London like weather, traffic, mayor, and more.
You should answer these questions directly with the relevant information.

If a question doesn't relate to London or specific queries (e.g., 'weather', 'traffic', 'mayor'), your response should be:
{
    "needs_web_scraping": "No",
    "response": "Sorry, I can only provide information related to London."
}

If the user asks for:
- "weather" or "give weather", provide London's current weather by default
- "traffic today", provide information about the current traffic in London
- "who is the mayor", provide information about London's current mayor
- "download the crime data of Borough region", initiate file download

If the query is a general question or requires web scraping, you should answer accordingly, keeping the response in the required JSON format.

Rules:
- If web scraping is needed: needs_web_scraping = "Yes" and response = ""
- If no scraping is needed: needs_web_scraping = "No" and provide the answer in response field
- Always maintain this JSON structure
- Consider the full conversation history when responding"""

# Chat function to handle user input and provide relevant responses
def chat_with_history():
    # Initialize messages list with system prompt
    messages = [system_prompt]
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
            
        # Process the response to provide London-specific answers
        if user_input.lower() == "weather" or user_input.lower() == "give weather":
            response_json = {
                "needs_web_scraping": "No",
                "response": get_weather()  # Automatically call the function to get London weather
            }
        elif user_input.lower() == "traffic today":
            response_json = {
                "needs_web_scraping": "No",
                "response": get_traffic()  # Placeholder traffic data for London
            }
        elif user_input.lower() == "who is the mayor":
            response_json = {
                "needs_web_scraping": "No",
                "response": get_mayor()  # Static mayor info for London
            }
        elif user_input.lower() == "download the crime data of borough region":
            # Trigger the file download function
            response_json = {
                "needs_web_scraping": "No",
                "response": "Starting the download of Borough region crime data..."
            }
            print("Assistant:", response_json)
            download_crime_data()  # Execute download function
            continue  # Skip to the next input without printing response again
        else:
            response_json = {
                "needs_web_scraping": "No",
                "response": "Sorry, I can only provide information related to London."
            }
        
        print("Assistant:", response_json)
    
    return messages

chat_with_history()
