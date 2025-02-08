from bs4 import BeautifulSoup
import argparse
import requests
from requests.exceptions import RequestException
import webbrowser
import ctypes
import time
import hashlib
import pushbullet
import threading
import os
from dotenv import load_dotenv
import traceback

def create_or_open_file(filename: str, mode: str):
    if not os.path.exists(filename):
        with open("last_hash.txt", "w") as file:
            file.write("")
    return open(filename, mode)

def get_api_value(key: str):
    return os.getenv(key)

def get_html_document(url, retries=1, delay=5):
    for attempt in range(retries + 1):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.text
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise

def is_not_sleep_time():
    current_time = time.localtime()
    return 7 <= current_time.tm_hour <= 21

def sleep_until_morning():
    current_time = time.localtime()
    target_hour = 7
    target_minute = 0

    target_time = time.mktime((current_time.tm_year, current_time.tm_mon, current_time.tm_mday, target_hour, target_minute, 0, current_time.tm_wday, current_time.tm_yday, current_time.tm_isdst))
    sleep_seconds = target_time - time.mktime(current_time)
    time.sleep(sleep_seconds)

def show_message(message: str, header: str):
    ctypes.windll.user32.MessageBoxW(0, message, header, 1)

# url_to_scrape = "https://www.bilete-fcsb.ro/"
# header_in_case_of_site_update = "Bilete Meci"
# message_in_case_of_site_update = "E posibil ca biletele sa fie disponibile. Site-ul a fost actualizat"
# info_header = "Info"
# info_regarding_the_functionality_of_the_program = f"Programul ruleaza. Se va verifica disponibilitatea biletelor la fiecare 1 minut"
# num_seconds_before_next_check = 60

def main(url_to_scrape, header_in_case_of_site_update, message_in_case_of_site_update, info_header, info_regarding_the_functionality_of_the_program, num_seconds_before_next_check):
    last_hash = ""
    minutes_counter = 60
    load_dotenv()

    while True:
        try:
            publish_alerts = is_not_sleep_time()
            pb = pushbullet.PushBullet(get_api_value("PUSHBULLET_API_KEY"))
            if publish_alerts:
                if minutes_counter == 60:
                    minutes_counter = 0
                    push = pb.push_note(info_header, info_regarding_the_functionality_of_the_program)
            html_document = get_html_document(url_to_scrape, retries=1, delay=5)
            soup = BeautifulSoup(html_document, 'html.parser')
            if last_hash == "":
                file  = create_or_open_file(r"last_hash.txt", "r")
                last_hash = file.readline()
                file.close()
            text_site = soup.get_text()
            new_hash = hashlib.md5(str(text_site).encode('UTF-8')).hexdigest()
            if last_hash == "":
                last_hash = new_hash
                file = create_or_open_file(r"last_hash.txt","w+")
                file.write(new_hash)
                file.close()
            elif new_hash == last_hash:
                print(f'{new_hash} is the same as {last_hash} at {time.localtime()}.\nWe will wait {num_seconds_before_next_check // 60} more minutes before trying again.')
                new_hash = last_hash
                minutes_counter += num_seconds_before_next_check // 60
                time.sleep(num_seconds_before_next_check)
            else:
                print(message_in_case_of_site_update)
                if not publish_alerts:
                    sleep_until_morning()
                push = pb.push_note(header_in_case_of_site_update, message_in_case_of_site_update)
                webbrowser.open(url_to_scrape)
                file = create_or_open_file(r"last_hash.txt","w+")
                file.write(new_hash)
                file.close()
                # Run the message box in a separate thread
                threading.Thread(target=show_message(message_in_case_of_site_update, header_in_case_of_site_update)).start()
                break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            traceback.print_exc()
            minutes_counter += num_seconds_before_next_check // 60
            time.sleep(num_seconds_before_next_check)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape a website and send notifications.")
    parser.add_argument("--url", type=str, required=True, help="URL to scrape")
    parser.add_argument("--header_update", type=str, default="Site updated", help="Header in case of site update")
    parser.add_argument("--message_update", type=str, default="The site has been updated. Please check.", help="Message in case of site update")
    parser.add_argument("--info_header", type=str, default="Info", help="Info header")
    parser.add_argument("--info_message", type=str, default="The program is working fine", help="Info regarding the functionality of the program")
    parser.add_argument("--check_interval", type=int, default=60, help="Number of seconds before next check")
    args = parser.parse_args()
    main(args.url, args.header_update, args.message_update, args.info_header, args.info_message, args.check_interval)