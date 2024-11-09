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
import requests

import requests

# Function to get traffic updates for London using TomTom API
def get_traffic_tomtom():
    # Replace with your actual TomTom API key
    api_key = "/traffic/services/5/incidentDetails"  # Make sure to replace with a valid API key
    
    # Define the bounding box for London (area of interest)
    bbox = "-0.510375,51.286760,0.334015,51.691874"  # This defines the London area
    
    # Format the URL based on the TomTom API structure
    url = f"https://api.tomtom.com/traffic/services/4/incidentDetails?bbox={bbox}&key={api_key}"
    
    try:
        # Make a request to the TomTom Traffic API
        response = requests.get(url)
        
        # Print the response status and headers for debugging
        print("Response Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        
        # Check if the request was successful (HTTP status 200)
        if response.status_code == 200:
            data = response.json()
            
            # Check if the API returns incidents
            incidents = data.get("incidents", [])
            
            if incidents:
                # Prepare a formatted response for the user
                traffic_report = "Current Traffic Incidents in London:\n"
                for incident in incidents:
                    incident_id = incident.get("id", "N/A")
                    severity = incident.get("severity", "N/A")
                    description = incident.get("description", "No description available")
                    
                    traffic_report += f"Incident ID: {incident_id}\n"
                    traffic_report += f"Severity: {severity}\n"
                    traffic_report += f"Description: {description}\n"
                    traffic_report += "-" * 50 + "\n"
                
                return traffic_report
            else:
                return "No traffic incidents reported at the moment."
        else:
            # Print response text for further debugging if there's an error
            print("Response Text:", response.text)
            return f"Error: Failed to retrieve traffic data. HTTP Status Code: {response.status_code}"
    
    except requests.exceptions.RequestException as e:
        # Handle any network or request errors
        return f"Error fetching traffic data from TomTom: {str(e)}"

# Example usage of the function
print(get_traffic_tomtom())



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
        if user_input.lower() == "weather" or user_input.lower() == "give weather" or user_input.lower() == "london weather":
            response_json = {
                "needs_web_scraping": "No",
                "response": get_weather()  # Automatically call the function to get London weather
            }
        elif user_input.lower() == "traffic today" or user_input.lower() == "traffic":
            response_json = {
                "needs_web_scraping": "No",
                "response": get_traffic_tomtom()  # Placeholder traffic data for London
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
