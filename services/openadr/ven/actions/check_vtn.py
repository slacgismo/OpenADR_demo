import requests
import logging
import time


def check_vtn(url):
    # check the vtn health check
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        print("Could not connect to server.")


def check_vtn_and_retry(url) -> bool:

    retry = 0
    is_vtn_running = False
    while retry < 3:
        is_vtn_running = check_vtn(url=url)
        if is_vtn_running:
            logging.info(
                "=====================================================================")
            logging.info("VTN is running")
            logging.info(
                "=====================================================================")
            return True
        retry += 1
        logging.info(f"retry {retry}")
        time.sleep(2)
    # if vtn is not running, exit the program
    return False
