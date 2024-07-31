from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
def start_webdriver_session():
    try:
        print("Starting WebDriver session for PC/laptop")
        options = Options()
        options.add_argument("--disable-geolocation")  # Disable geolocation prompt
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Error starting WebDriver session: {e}")
        return None

def fetch_and_send_location(driver, flask_server_url, unique_url):
    try:
        driver.get(flask_server_url)
        time.sleep(2)

        # Example: Fetch location using JavaScript
        js_script = """
        navigator.geolocation.getCurrentPosition = function(success, error, options) {
            success({
                coords: {
                    latitude: 37.7749,   // Example latitude
                    longitude: -122.4194 // Example longitude
                }
            });
        };
        navigator.geolocation.getCurrentPosition(function(position) {
            var locationData = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };
            fetch('{}/location/{}', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(locationData)
            }})
            .then(response => response.text())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
        });
        """.format(flask_server_url, unique_url)

        driver.execute_script(js_script)
        time.sleep(5)
    except Exception as e:
        print(f"Error fetching location: {e}")
    finally:
        driver.quit()

def main():
    flask_server_url = 'http://127.0.0.1:5000'
    unique_url = 'your_unique_url'

    driver = start_webdriver_session()
    if driver:
        fetch_and_send_location(driver, flask_server_url, unique_url)

if __name__ == "__main__":
    main()