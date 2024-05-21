import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class WebsitePerformanceAnalyzer:
    def __init__(self, site_url):
        self.site_url = site_url
    
    def get_loading_time(self):
        try:
            response = requests.get(self.site_url)
            return response.elapsed.total_seconds()
        except requests.exceptions.RequestException as e:
            print("Error fetching URL:", e)
            return None
    
    def get_time_to_first_byte(self):
        try:
            response = requests.get(self.site_url)
            return response.elapsed.total_seconds()
        except requests.exceptions.RequestException as e:
            print("Error fetching URL:", e)
            return None
    
    def get_page_size(self):
        try:
            response = requests.get(self.site_url)
            return len(response.content) / 1024  # Size in KB
        except requests.exceptions.RequestException as e:
            print("Error fetching URL:", e)
            return None
    
    def get_number_of_requests(self):
        try:
            response = requests.get(self.site_url)
            return len(response.history) + 1
        except requests.exceptions.RequestException as e:
            print("Error fetching URL:", e)
            return None
    
    def get_performance_metrics(self):
        try:
            api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={self.site_url}&strategy=mobile"
            response = requests.get(api_url)
            data = response.json()
            if 'loadingExperience' in data['lighthouseResult']['audits']:
                page_speed_index = data['lighthouseResult']['audits']['loadingExperience']['details']['items'][0]['firstContentfulPaint']['percentile']
                largest_contentful_paint = data['lighthouseResult']['audits']['loadingExperience']['details']['items'][0]['firstContentfulPaint']['percentile']
            else:
                page_speed_index = None
                largest_contentful_paint = None
            return page_speed_index, largest_contentful_paint
        except Exception as e:
            print("Error fetching performance metrics:", e)
            return None, None
        
    def calculate_performance_percentage(self, loading_time, time_to_first_byte, page_size, number_of_requests):
        loading_time_weight = 30
        time_to_first_byte_weight = 20
        page_size_weight = 25
        number_of_requests_weight = 25

        max_loading_time = 3000  # Maximum loading time in milliseconds (for example)
        max_time_to_first_byte = 500  # Maximum time to first byte in milliseconds (for example)
        max_page_size = 1024  # Maximum page size in KB (for example)
        max_number_of_requests = 100  # Maximum number of requests (for example)

        normalized_loading_time = (max_loading_time - loading_time) / max_loading_time * 100
        normalized_time_to_first_byte = (max_time_to_first_byte - time_to_first_byte) / max_time_to_first_byte * 100
        normalized_page_size = (max_page_size - page_size) / max_page_size * 100
        normalized_number_of_requests = (max_number_of_requests - number_of_requests) / max_number_of_requests * 100

        performance_percentage = (loading_time_weight * normalized_loading_time +
                                time_to_first_byte_weight * normalized_time_to_first_byte +
                                page_size_weight * normalized_page_size +
                                number_of_requests_weight * normalized_number_of_requests) / 100

        return performance_percentage
    
    def grade_website_performance(self,percentage):
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B+'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 60:
            return 'C+'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D+'
        else:
            return 'D'
        
    def analyze_images(self):
        try:
            # Send a GET request to the website URL
            response = requests.get(self.site_url)

            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all image tags on the webpage
            img_tags = soup.find_all('img')

            total_images = len(img_tags)
            total_image_size = 0

            # Calculate the total size of all images
            for img_tag in img_tags:
                # Construct the absolute URL of the image
                img_url = urljoin(self.site_url, img_tag['src'])

                # Send a HEAD request to get the image size
                img_response = requests.head(img_url)

                # Get the content-length header, which indicates the size of the image
                content_length = img_response.headers.get('content-length')

                if content_length:
                    total_image_size += int(content_length)

            return total_images, total_image_size

        except Exception as e:
            print("Error analyzing images:", e)
            return None, None


# analyzer = WebsitePerformanceAnalyzer("https://akshatsimejiya.netlify.app/")
# print("Loading Time:", analyzer.get_loading_time(), "seconds")
# print("Time to First Byte:", analyzer.get_time_to_first_byte(), "seconds")
# print("Page Size:", analyzer.get_page_size(), "KB")
# print("Number of Requests:", analyzer.get_number_of_requests())

# page_speed_index, largest_contentful_paint = analyzer.get_performance_metrics()
# if page_speed_index is not None:
#     print("Page Speed Index:", page_speed_index, "ms")
# else:
#     print("Failed to retrieve Page Speed Index")

# if largest_contentful_paint is not None:
#     print("Largest Contentful Paint:", largest_contentful_paint, "ms")
# else:
#     print("Failed to retrieve Largest Contentful Paint")
