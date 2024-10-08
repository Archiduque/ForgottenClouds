from config import CREATION, ERROR, DELETION, OUTPUT_FOLDER

from pathlib import Path
from datetime import datetime
import pandas as pd



def readTXTFile(file_path: str) -> list[str]:
    """
        Reads a TXT file and returns a list with the values it contains.
            If the line startswith the character '#', we will treat the line as a comment.

        Args:
            file_path (str): The path to the TXT file you want to read.

        Returns:
            list[str]: A list with the values from the TXT file, where each value represents a line in the file.
    """

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            # Remove line breaks from each line
            return [line.strip() for line in lines if not line.startswith('#')]
        
    except FileNotFoundError as e:
        
        raise FileNotFoundError(f"\t[{ERROR}] File not found: {file_path}") from e
    
    except Exception as e:
        raise Exception(f"\t[{ERROR}] Error reading file: {file_path}") from e



def getDateTime() -> datetime:
    '''
        Returns the current date and time in the format YYYY-MM-DD-HH:MM:SS.

        Returns:
            str: The current date and time in the format YYYY-MM-DD-HH:MM:SS.
    '''

    # datetime object containing current date and time
    now = datetime.now()

    # YYYY-MM-DD-HH:MM:SS
    # today_srt = now.strftime("%Y-%m-%d %H:%M:%S")

    # YYYY-MM-DD
    today_srt = now.strftime("%Y-%m-%d")

    return today_srt



def checkPaths(company: str) -> Path:
    """
        Check if the "Output" folder exists. If not, create it.
        Check if the company folder exists. If not, create it.

        Args:
            company (str): The company name.
            
        Returns:
            company_path (Path): The path to the company folder.
    """

    # Current working directory
    path = Path().absolute()

    # Output Path
    output_path = path / OUTPUT_FOLDER

    # Company Path
    company_path = output_path / company

    # If Output directory doens't exist let's create it
    if not output_path.exists():
        try:
            Path.mkdir(output_path)
            print(f'\t\t\t\t[{CREATION}] Created a new folder for script output: {output_path}')

        except Exception as e:
            print(f'\t\t\t\t[{ERROR}] checkPaths - output_path - {e}')
            
    if not company_path.exists():
        try:
            Path.mkdir(company_path)
            print(f'\t\t\t\t[{CREATION}] Created a new folder for the company: {company_path}')

        except Exception as e:
            print(f'\t\t\t\t[{ERROR}] checkPaths - company_path - {e}')

    return company_path



def writeBlobs(blobs: list[dict], company: str, storage_account: str, container_name: str):
    """
        Writes a list of blobs to a CSV file. File name will be a mix of the storage account name and container name.

        Args:
            blobs (list[dict]): A list of dictionaries containing blob information.
            storage_account (str): The storage account name.
            container_name (str): The container name.
    """

    # Relevant columns use in the DataFrame
    columns = [
        'name',
        'container',
        'url',
        'creation_time',
        'last_modified',
        'blob_type',
        'etag',
        'size',
        'content_type',
        'content_encoding',
        'content_language',
        'content_md5',
        'status',
        'state',
    ]

    # Create a DataFrame from the blobs to save in the csv
    df = pd.DataFrame(blobs, columns=columns)

    # Check if all the Paths are created and if not, create them
    company_path = checkPaths(company)

   # Filename
    filename = company + '_' + storage_account.split(".")[0] + '_' + container_name + getDateTime() + '.csv'
    file_path = company_path / filename

    # If the file already exist, first we need to delete it
    if file_path.exists():
        try: 
            # Remove the file
            file_path.unlink() 
            print(f'\t\t\t\t[{DELETION}] File {file_path} already exist. Deleting...')

        except Exception as e:
            print(f'\t\t\t\t[{ERROR}] writeBlobs - file_path - {e}')

    # File creation
    try:
        df.to_csv(file_path, index=False)
        print(f'\t\t\t\t[{CREATION}] File {file_path} has been created')

    except Exception as e:
        print(f'\t\t\t\t[{ERROR}] writeBlobs - df.to_csv - {e}')