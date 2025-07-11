# We check to see if a website is online using the requests library.
import requests
import time
import validators
import argparse
import datetime

from urllib.parse import urlparse

def is_website_online(url):
    try:
        # first we check if the url is valid if not we will exit the program.
        if not validators.url(url):
            error_msg = f"Error: '{url}' is not a valid URL. Please provide a valid URL (e.g., https://felicis.au)"
            print(error_msg)
            
            # Append error to log file
            with open("status.txt", "a") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] {error_msg}\n")
            return
        
        beginning_time = time.perf_counter()

        response = requests.head(url, timeout=10) # we give it 10 seconds to respond
        
        # We are going to inform the user how long it took to get a response from the server.
        finished_time = time.perf_counter()
        elapsed_time = finished_time - beginning_time

        # We are checking the status code and telling the user what it means.

        # we provide feedback to the user on what the status code means.
        # we also let the user know if the website is online or not.
        # we will also log the status code and response time to a file called status.txt

        status_msg = ""
        
        if response.status_code == 200:
            status_msg = f"{url} is online and reachable the status code 200 indicates success."
        elif response.status_code == 404:
            status_msg = f"{url} is online but the page was not found (404)."
        elif response.status_code == 500:
            status_msg = f"{url} is online but there was an internal server error (500)."
        elif response.status_code == 403:
            status_msg = f"{url} is online but access is forbidden (403)."
        elif response.status_code == 401:
            status_msg = f"{url} is online but authentication is required (401)."
        elif response.status_code == 301 or response.status_code == 302:
            status_msg = f"{url} is online but it has been redirected ({response.status_code})."
        else:
            status_msg = f"{url} returned status code {response.status_code}."

        print(status_msg)
        time_msg = f"Response time: {elapsed_time:.2f} seconds"
        print(time_msg)

        # Append success information to log file
        with open("status.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {status_msg}\n")
            log_file.write(f"[{timestamp}] {time_msg}\n")

    except requests.ConnectionError:
        error_msg = f"{url} is offline or unreachable due to a connection error."
        print(error_msg)
        
        # Append connection error to log file
        with open("status.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {error_msg}\n")
            
    except requests.Timeout:
        error_msg = f"{url} is offline or unreachable due to a timeout error."
        print(error_msg)
        
        # Append timeout error to log file
        with open("status.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {error_msg}\n")
            
    except requests.RequestException as e:
        error_msg = f"An error occurred while trying to reach {url}: {e}"
        print(error_msg)
        
        # Append general request error to log file
        with open("status.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {error_msg}\n")

if __name__ == "__main__":
    # this is the main function that will run if there is no command line arugments.


    # we will check to see if a website is provided as a command line argument using the arugment --url

    parser = argparse.ArgumentParser(description="Check if a website is online.")
    parser.add_argument('--url', type=str, help='The URL of the website to check. You must type https:// or https://:')

    args = parser.parse_args()

    # web check if arugments are provided if not we will run the program in a loop until the user types exit.

    if not any(vars(args).values()):
        while True:
            print("Website Status Checker Version 1.0")
            print("This program checks if a website is online or not.")
            url = input("What is the url you want to check? You must type https:// or https://: ")
            if url.lower() == "exit":
                print("Exiting the program.")
                break
            if not validators.url(url):
                print("The URL is not valid. Please provide a valid URL.")
                continue
            is_website_online(url)

    else:
        if args.url:
            # Check if the provided URL is valid before proceeding
            if not validators.url(args.url):
                print(f"Error: '{args.url}' is not a valid URL. Please provide a valid URL (e.g., https://felicis.au)")
                exit(1)
            # we now check the url using the is_website_online function.
            is_website_online(args.url)
        else:
            print("No URL provided. Please provide a URL using the --url argument. You must type https:// or https://:")
            print("Example: python main.py --url https://jessicaamy.com")
