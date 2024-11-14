import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Configuration
INPUT_CSV = "input_urls.csv"        
OUTPUT_CSV = "output_profile_data.csv"  
WEBDRIVER_PATH = "chromedriver.exe"    
DELAY = 2  

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")          
chrome_options.add_argument("--no-sandbox")         
chrome_options.add_argument("--disable-dev-shm-usage")  
chrome_options.add_argument("--disable-gpu")       
chrome_options.add_argument("--disable-extensions") 

# Initialize WebDriver with Service
service = Service(WEBDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_twitter_profile(url):
    driver.get(url)
    time.sleep(DELAY)  
    
    profile_data = {
        "Bio": "",
        "Following Count": "",
        "Followers Count": "",
        "Location": "",
        "Website": ""
    }
    
    try:
        bio = driver.find_element(By.XPATH, '//div[@data-testid="UserDescription"]/span')
        profile_data["Bio"] = bio.text
    except:
        pass
    
    try:
        following_count = driver.find_element(By.XPATH, '//a[@href$="/following"]/span[1]/span')
        profile_data["Following Count"] = following_count.text
    except:
        pass
    
    try:
        followers_count = driver.find_element(By.XPATH, '//a[@href$="/followers"]/span[1]/span')
        profile_data["Followers Count"] = followers_count.text
    except:
        pass
    
    try:
        location = driver.find_element(By.XPATH, '//div[@data-testid="UserProfileHeader_Items"]/span[1]')
        profile_data["Location"] = location.text
    except:
        pass
    
    try:
        website = driver.find_element(By.XPATH, '//div[@data-testid="UserProfileHeader_Items"]/a')
        profile_data["Website"] = website.get_attribute("href")
    except:
        pass
    
    return profile_data

def main():
    with open(INPUT_CSV, mode='r') as file:
        reader = csv.reader(file)
        urls = [row[0] for row in reader]

    with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Bio", "Following Count", "Followers Count", "Location", "Website"])
        
        for url in urls:
            try:
                profile_data = scrape_twitter_profile(url)
                writer.writerow([url] + list(profile_data.values()))
                print(f"Scraped: {url}")
            except Exception as e:
                print(f"Error scraping {url}: {e}")

    driver.quit()

if __name__ == "__main__":
    main()
