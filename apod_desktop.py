""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py image_dir_path [apod_date]

Parameters:
  image_dir_path = Full path of directory in which APOD image is stored
  apod_date = APOD image date (format: YYYY-MM-DD)

History:
  Date         Author      Description
  2022-03-11  Jay Patel   Initial creation
"""
import hashlib
from sys import argv, exit
from datetime import datetime, date
from hashlib import sha256
from os import path
import sqlite3
import json
from webbrowser import get
import requests
import os
import urllib.request
from http import client
import ctypes

def main():

    # Determine the paths where files are stored
    image_dir_path = get_image_dir_path()
    db_path = path.join(image_dir_path, 'apod_images.db')

    # Get the APOD date, if specified as a parameter
    apod_date = get_apod_date()

    # Create the images database if it does not already exist
    create_image_db(db_path)

    # Get info for the APOD
    apod_info_dict = get_apod_info(apod_date)
    
    # Download today's APOD
    image_url = apod_info_dict['url']
    image_msg = download_apod_image(image_url)
    image_sha256 = hashlib.sha256(image_msg).hexdigest
    image_size = -1 # TODO
    image_path = get_image_path(image_url, image_dir_path)
   

    # Print APOD image information
    print_apod_info(image_url, image_path, image_size, image_sha256)

    # Add image to cache if not already present
    if not image_already_in_db(db_path, image_sha256):
        save_image_file(image_msg, image_path)
        add_image_to_db(db_path, image_path, image_size, image_sha256)

    # Set the desktop background image to the selected APOD
    set_desktop_background_image(image_path)

def get_image_dir_path():
    """
    Validates the command line parameter that specifies the path
    in which all downloaded images are saved locally.

    :returns: Path of directory in which images are saved locally
    """
    if len(argv) >= 2:
        dir_path = argv[1]
        if path.isdir(dir_path):
            print("Images directory:", dir_path)
            return dir_path
        else:
            print('Error: Non-existent directory', dir_path)
            exit('Script execution aborted')
    else:
        print('Error: Missing path parameter.')
        exit('Script execution aborted')

def get_apod_date():
    """
    Validates the command line parameter that specifies the APOD date.
    Aborts script execution if date format is invalid.

    :returns: APOD date as a string in 'YYYY-MM-DD' format
    """    
    if len(argv) >= 3:
        # Date parameter has been provided, so get it
        apod_date = argv[2]

        # Validate the date parameter format
        try:
            datetime.strptime(apod_date, '%Y-%m-%d')
        except ValueError:
            print('Error: Incorrect date format; Should be YYYY-MM-DD')
            exit('Script execution aborted')
    else:
        # No date parameter has been provided, so use today's date
        apod_date = date.today().isoformat()
    
    print("APOD date:", apod_date)
    return apod_date

def get_image_path(image_url, dir_path):
    """
    Determines the path at which an image downloaded from
    a specified URL is saved locally.

    :param image_url: URL of image
    :param dir_path: Path of directory in which image is saved locally
    :returns: Path at which image is saved locally
    """
        


    return "TODO"

def get_apod_info(date):
    """
    Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    :param date: APOD date formatted as YYYY-MM-DD
    :returns: Dictionary of APOD info
    """    
    print("Getting APOD info...", end='')

    url = "https://api.nasa.gov/planetary/apod?api_key=gsfSfV7oFt7IBgc30xwm0alAyTvEk9LlCQwlIdWc" + date
    resp_msg = requests.get(url)

    if resp_msg.status_code == 200:
        print('success')
        return resp_msg.json()

    else:
        print('failed. Code:', resp_msg.status_code) 
        return   
    #return {"todo" : "TODO"}

def print_apod_info(image_url, image_path, image_size, image_sha256):
    """
    Prints information about the APOD

    :param image_url: URL of image
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """    
    
    return #TODO

def download_apod_image(image_url):
    """
    Downloads an image from a specified URL.

    :param image_url: URL of image
    :returns: Response message that contains image data
    """
    resp_msg = requests.get(image_url)
    if resp_msg.status_code == 200:
        try:
            img_data = resp_msg.content   
            with open(path, 'wb') as fp: 
                fp.write(img_data)
            return path
        except:
            return
    
    else:
        print('Failed to APOD download image.')
        print('Response Code:', resp_msg.status_code)
        print(resp_msg.text)
    

def save_image_file(image_msg, image_path):
    """
    Extracts an image file from an HTTP response message
    and saves the image file to disk.

    :param image_msg: HTTP response message
    :param image_path: Path to save image file
    :returns: None
    """
    with open(path, 'wb') as fp: 
        fp.write(image_msg)
    return 
    

def create_image_db(db_path):
    """
    Creates an image database if it doesn't already exist.

    :param db_path: Path of .db file
    :returns: None
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_table_query = """ CREATE TABLE IF NOT EXISTS 'Image of The Day' (
                                'Downloaded Date'  text NOT NULL,
                                'Name' text NOT NULL,
                                'Size'  text NOT NULL,
                                'SHA-256 Hash' text NOT NULL,
                                'Path' text NOT NULL,
                                PRIMARY KEY ("Name")
                            );"""
    cursor.execute(create_table_query)

    return #TODO

def add_image_to_db(file_name, db_path, image_path, image_size, image_sha256):
    """
    Adds a specified APOD image to the DB.

    :param db_path: Path of .db file
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    addDataquery = """INSERT INTO 'Image of The Day' (
                                'Downloaded Date', 
                                'Name', 
                                'Size', 
                                'SHA-256',
                                'Path')
                            VALUES (?, ?, ?, ?, ?);"""

    Image_data = (str(date),
                file_name,
                image_size, 
                image_sha256.upper(),
                image_path
                )
    
    cursor.execute(addDataquery, Image_data)
    connection.commit()
    connection.close()
    return #TODO

def image_already_in_db(db_path, image_sha256):
    """
    Determines whether the image in a response message is already present
    in the DB by comparing its SHA-256 to those in the DB.

    :param db_path: Path of .db file
    :param image_sha256: SHA-256 of image
    :returns: True if image is already in DB; False otherwise
    """ 
    connection = sqlite3.connect('apod_images.db')
    cursor = connection.cursor()
    addDataquery = "SELECT * FROM 'Image of The Day' WHERE SHA-256 = ?;"
    cursor.execute(addDataquery, image_sha256)
    row = cursor.fetchone()
    connection.commit()
    connection.close()
    if row is None:
        return False
    else:
        return True


    return True #TODO

def set_desktop_background_image(image_path):
    """
    Changes the desktop wallpaper to a specific image.

    :param image_path: Path of image file
    :returns: None
    """
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    except:
        print("Error setting desktop backgroung image")
    return #TODO

main()