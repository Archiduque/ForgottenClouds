import asyncio
import aiodns
from config import AZURE_STORAGE

''' 
    Info

    1. https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json
        - Storage Account Name: Storage account names must be between 3 and 24 characters in length and may contain numbers and lowercase letters only.

        http://<mystorageaccount>.blob.core.windows.net
'''

ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"

def validatePermutation(permutation: str) -> bool:
    """
        Validates a storage account permutation by checking if it meets the following criteria:
            - The permutation is between 3 and 24 characters in length.
            - The permutation contains only lowercase letters and numbers.
        
        Args:
            permutation (str): The storage account permutation to be validated.

        Returns:
            bool: True if the permutation is valid, False otherwise.
    """

    # Set True by default
    is_valid_permutation = True

    # length between 3 and 24
    if 3 <= len(permutation) <= 24:
        # All characters are allowed
        if all(char in ALLOWED_CHARACTERS for char in permutation):
            is_valid_permutation = True

        else:
            # Invalid characters in Storage Account
            is_valid_permutation = False

    else:
        # Invalid Storage Account length
        is_valid_permutation = False

    return is_valid_permutation


def permutation(company_name: str, keywords: list[str]) -> list[str]:
    """
        Generates permutations of storage account names by combining company name, keywords, and resources.

        Args:
            company_name (str): The company name to be used in the storage account names.
            keywords (list[str]): A list of keywords to be included in the storage account names.

        Returns:
            list[str]: A list of potential storage account built from the permutations. 
    """

    permutations = []

    # Add base case with company name as storage account
    permutations.append(f"{company_name}")

    for keyword in keywords:
        # Prepend company name to keywords and resource -> <keyword><company_name>.<resource>
        permutation = None
        permutation = f"{keyword}{company_name}"
        # Validate permutation and add it to the list if valid
        permutations.append(permutation) if validatePermutation(permutation) else None

        # Append company name to keywords and resource -> <company_name><keyword>.<resource>
        permutation = None
        permutation = f"{company_name}{keyword}"
        # Validate permutation and add it to the list if valid
        permutations.append(permutation) if validatePermutation(permutation) else None

    return permutations



async def dnsLookup(storage_account: str, resolver: aiodns.DNSResolver) -> str:
    """
        Perform an async DNS lookup for the given FQDN.

        Args:
            storage_account (str): The FQDN of the Azure Storage Account.
            resolver (aiodns.DNSResolver): An object to perform asynchronous DNS queries.

        Returns:
            str: The storage_account (FQDN) if the DNS lookup is successful, otherwise raises an exception.
    """

    try:

        await resolver.query(storage_account, 'A')
        print(f"\t[{AZURE_STORAGE}] Azure Storage Account found: {storage_account}")
        
        return storage_account
        
    except aiodns.error.DNSError as e:
        
        #print(f"{e.args[1]} - Code {e.args[0]} - {storage_account}")
        pass



async def checkAzureResources(storage_accounts: list[str]) -> list[str]:
    """
        Performs asynchronous DNS lookups for a list of Azure storage accounts.

        Args:
            storage_accounts (list[str]): A list of storage account FQDNs to check.

        Returns:
            list[str]: A list of storage account FQDNs that successfully resolved the DNS lookup.
    """

    resolver = aiodns.DNSResolver()

    # Launch DNS queries for each storage account
    tasks = [dnsLookup(storage_account, resolver) for storage_account in storage_accounts]

    # Wait until all tasks are completed
    results = await asyncio.gather(*tasks)

    # Return only successful lookups (assuming dnsLookup raises for errors)
    return [storage_account for storage_account in results if storage_account is not None]



def findStorageAccounts(company: str, keywords: list[str], resources: list[str]) -> list[str]:
    """
        Finds valid Azure storage account names based on permutations of company name, keywords, and resources.

        Args:
            company (str): The company name to be used in the storage account names.
            keywords (list[str]): A list of keywords to be included in the storage account names.
            resources (list[str]): A list of Azure resources to be appended to the storage account names.

        Returns:
            list[str]: A list of valid Azure storage account FQDNs generated from the permutations.
    """

    storage_accounts = []
    valid_storage_accounts  = []
    fqdn = []

    # Get permutations for company and keywords
    storage_accounts = permutation(company, keywords)

    for resource in resources:
        # Append the storage accounts to each resource
        fqdn.extend(["".join([storage_account, ".", resource]) for storage_account in storage_accounts])

    # Check if fqdn (storage account names) are valid using asynchronous tasks
    loop = asyncio.get_event_loop()
    valid_storage_accounts .extend(loop.run_until_complete(checkAzureResources(fqdn)))

    # Return the list of valid storage account FQDNs
    return valid_storage_accounts 
