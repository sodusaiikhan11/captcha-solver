import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = 'https://lapse-immi.moj.go.jp/ZEC/appl/e0/ZEC2/pages/FZECST011.aspx'
output_dir = 'captchas'
progress_file = 'progress.txt'

os.makedirs(output_dir, exist_ok=True)

def get_last_index():
    """Read the last index from the progress file."""
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return -1
    return -1

def save_progress(index):
    with open(progress_file, 'w') as f:
        f.write(str(index))

def download_captcha_image(index):
    driver.get(url)
    time.sleep(2) 

    try:
        captcha_element = driver.find_element(By.CSS_SELECTOR, 'img[src="JpegImage.aspx"]')
        location = captcha_element.location
        size = captcha_element.size

        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))

        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']

        captcha_image = image.crop((left, top, right, bottom))
        captcha_image.save(os.path.join(output_dir, f'captcha_{index}.png'))
        print(f'Downloaded image {index + 1}')
        save_progress(index)  
    except Exception as e:
        print(f'Error downloading image {index + 1}: {e}')

def main():
    start_index = 6126
    num_images = 10000  

    for i in range(start_index, num_images):
        try:
            download_captcha_image(i)
            time.sleep(1) 
        except Exception as e:
            print(f'Error in main loop: {e}')
            continue

    driver.quit()

if __name__ == '__main__':
    main()
