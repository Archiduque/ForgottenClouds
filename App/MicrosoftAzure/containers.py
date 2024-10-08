import asyncio
import aiohttp
from config import INFO, BUCKET, ERROR, WARNING

''' 
    Info

    1. https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction#blob-storage-resources
        - Container names can be between 3 and 63 characters long.
        - Container names must start with a letter or number, and can contain only lowercase letters, numbers, and the dash (-) character.
        - Two or more consecutive dash characters aren't permitted in container names.

        https://<mystorageaccount>.blob.core.windows.net/<mycontainer>

        https://<mystorageaccount>.blob.core.windows.net/<mycontainer>?restype=container&comp=list

'''

ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789-"



def validatePermutation(permutation: str) -> bool:
    """
        Validates the container name permutation by checking if it meets the following criteria:
            - The permutation is between 3 and 63 characters in length.
            - The permutation contains only lowercase letters, numbers and the dash (-) character.
        
        Args:
            permutation (str): The container name permutation to be validated.

        Returns:
            bool: True if the permutation is valid, False otherwise.
    """

    # Set True by default
    is_valid_permutation = True

    # length between 3 and 63
    if 3 <= len(permutation) <= 63:
        # All characters are allowed
        if all(char in ALLOWED_CHARACTERS for char in permutation):
            is_valid_permutation = True

        else:
            # Invalid characters in container name
            is_valid_permutation = False

    else:
        # Invalid container name length
        is_valid_permutation = False

    return is_valid_permutation



def permutation(company_name: str, storage_account: str, keywords: list[str]) -> list[str]:
    """
        Generates permutations of container names by combining company name, keywords and "-".

        Args:
            company_name (str): The company name to be used in the container names.
            storage_account (str): The storage account name to be used in the container names.
            keywords (list[str]): A list of keywords to be included in the container names.

        Returns:
            list[str]: A list of potential containers
    """

    permutations = []

    # company_name as container name
    permutations.append(f"{company_name}")

    # storage_account as container name
    permutations.append(f"{storage_account}")

    for keyword in keywords:
        # Keyword as container name
        permutations.append(f"{keyword}") if validatePermutation(f"{keyword}") else None

        # Prepend 
        # Prepend company name to keywords and resource -> <keyword><company_name>
        permutation = None
        permutation = f"{keyword}{company_name}"
        permutations.append(permutation) if validatePermutation(permutation) else None
        # Prepend company name to keywords and resource -> <keyword>-<company_name> ! Notice the "-" character in comparision with above
        permutation = None
        permutation = f"{keyword}-{company_name}"
        permutations.append(permutation) if validatePermutation(permutation) else None

        # Append
        # Append company name to keywords and resource -> <company_name><keyword>
        permutation = None
        permutation = f"{company_name}{keyword}"
        permutations.append(permutation) if validatePermutation(permutation) else None
        # Prepend company name to keywords and resource -> <keyword>-<company_name> ! Notice the "-" character in comparision with above
        permutation = None
        permutation = f"{company_name}-{keyword}"
        permutations.append(permutation) if validatePermutation(permutation) else None

    return permutations



async def fetchALL(session: aiohttp.ClientSession, URL: str) -> str:
    '''
        Performs asynchronous GET HTTP requests for a list of URLs and returns a list of URLs that return a 200 status code.

        Args:
            URLs (list[str]): A list of URLs to check.
                - URLs are formatted as "https://<mystorageaccount>.blob.core.windows.net/<mycontainer>?restype=container&comp=list"

        Returns:
            list[str]: A list of URLs that return a 200 status code.
    '''

    try:
        async with session.get(URL) as response:

            # If the bucket exists: HTTP status code 200
            if str(response.status).startswith("200"):

                #print(f'[{config.BUCKET}] bucket found: {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{URL}{Style.RESET_ALL}')
                print(f'\t\t\t[{BUCKET}] Exposed container found in: {URL}')

                return URL


    except aiohttp.client_exceptions.ClientOSError as e:
            # If we get a peer reset connection error we will call this funcion again
            print(f"\t\t\t[{WARNING}] aiohttp error for {URL} - {e}")

            async with session.get(URL) as response:
                print(f"\t\t\t\t[{INFO}] Trying again {URL}")
                await fetchALL(session, URL)

    except Exception as e:
            print(f'\t\t\t[{ERROR}]Unexpected exception - fetchALL - {e}')



async def checkContainers(URLs: list[str]) -> list[str]:
    """
        Performs asynchronous GET HTTP requests for a list of URLs and returns a list of URLs that return a 200 status code.

        Args:
            URLs (list[str]): A list of URLs to check.
                - URLs are formatted as "https://<mystorageaccount>.blob.core.windows.net/<mycontainer>?restype=container&comp=list"

        Returns:
            list[str]: A list of URLs that return a 200 status code.
    """

    tasks = []

    async with aiohttp.ClientSession(trust_env=True) as session:
        # Create list of tasks. In this case all the URLs to be checked
        for URL in URLs:
            tasks.append(asyncio.ensure_future(fetchALL(session, URL)))
        
        # Execute them in concurrent manner
        results = await asyncio.gather(*tasks)

        # Return only successful requests, http status code 200
        return [result for result in results if result is not None]



def findContainers(storage_account: str, company: str, keywords: list[str]) -> list[str]:
    """
        Finds valid Azure storage account names based on permutations of company name, keywords, and resources.

        Args:
            company (str): The company name to be used in the storage account names.
            keywords (list[str]): A list of keywords to be included in the storage account names.
            resources (list[str]): A list of Azure resources to be appended to the storage account names.

        Returns:
            list[str]: A list of valid Azure storage account FQDNs generated from the permutations.
    """

    URLs = []
    container_names = []
    valid_container_names = []
    storage_account_name = f"{storage_account.split('.')[0]}"

    # Get permutations for company and keywords
    container_names = permutation(company, storage_account_name, keywords)

    # Append the storage accounts to each resource a build the URL
    URLs.extend(["".join(["https://", storage_account, "/", container, "?restype=container&comp=list"]) for container in container_names])

    # Check if URL (Container) is valid using asynchronous tasks
    loop = asyncio.get_event_loop()
    valid_container_names .extend(loop.run_until_complete(checkContainers(URLs)))

    # Return the list of valid storage account FQDNs
    return valid_container_names 
