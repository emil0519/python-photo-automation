from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import shutil
from datetime import datetime

# Setup ChromeDriver service
service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

# Directory containing images
images_dir = '/Users/emillau/Desktop/Work/python-web-automation/images'
no_match_dir = os.path.join(images_dir, 'all-compared-no-match')
os.makedirs(no_match_dir, exist_ok=True)

# Track images that have been compared
compared_images = set()

try:
    while True:
        # Rebuild the list of image files
        image_files = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:  # Exit if there are no images left to compare
            print("No images left to compare.")
            break

        # Copy image_files into a snapshot list so we don't run into problems while iterating
        image_files_snapshot = image_files.copy()

        for i in range(len(image_files_snapshot)):
            if image_files_snapshot[i] in compared_images:
                continue  # Skip if the image has already been compared

            for j in range(i + 1, len(image_files_snapshot)):  # Avoid duplicate comparisons
                print(f"Comparing {image_files_snapshot[i]} with {image_files_snapshot[j]}")

                # Load the website
                driver.get("https://facecomparison.toolpie.com/")

                # Locate input fields and buttons
                file_input_1 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "validatedCustomFile"))
                )
                file_input_2 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "validatedCustomFile2"))
                )
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "inputSubmit"))
                )

                # Check if files exist before sending
                if os.path.exists(image_files_snapshot[i]) and os.path.exists(image_files_snapshot[j]):
                    file_input_1.send_keys(image_files_snapshot[i])
                    time.sleep(1)  # Optional delay to ensure files are handled correctly
                    file_input_2.send_keys(image_files_snapshot[j])
                else:
                    print(f"Error: One of the files does not exist. Skipping comparison.")
                    continue

                submit_button.click()

                # Wait for the result and retrieve it
                time.sleep(3)
                result_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".text-warning.font-weight-bold"))
                )
                result = result_element.text.strip('%')
                print(f"Result for {image_files_snapshot[i]} vs {image_files_snapshot[j]}: {result}")
                result_percentage = int(result)

                # If the result is higher than 70%, remove the images and create a folder
                if result_percentage > 70:
                    # Create the folder name using timestamp and result
                    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M")
                    folder_name = f"{timestamp}-{result_percentage}%"
                    folder_path = os.path.join(images_dir, folder_name)

                    # Create the new folder
                    os.makedirs(folder_path, exist_ok=True)

                    # Move images to the new folder (use shutil.move)
                    shutil.move(image_files_snapshot[i], folder_path)
                    shutil.move(image_files_snapshot[j], folder_path)
                    print(f"Images {image_files_snapshot[i]} and {image_files_snapshot[j]} moved to {folder_path}.")

                    # Add the images to the compared set
                    compared_images.add(image_files_snapshot[i])
                    compared_images.add(image_files_snapshot[j])

                    # After moving images, break to refresh the list of images and continue
                    break  # Exit the inner loop and check the next pair

        # If an image has been compared with all others, move it to the 'all-compared-no-match' folder
        for image in image_files:
            if image not in compared_images:
                # Move image to the 'all-compared-no-match' folder
                shutil.move(image, os.path.join(no_match_dir, os.path.basename(image)))
                print(f"Moved {image} to {no_match_dir}")
                compared_images.add(image)

    print("Comparison complete.")
finally:
    # Quit the driver
    driver.quit()
