import asyncio
import aiohttp
from config import AWS_S3_BUCKET, WARNING, INFO, ERROR


''' 
    Info

    1. https://docs.aws.amazon.com/es_es/AmazonS3/latest/userguide/bucketnamingrules.html
        - S3 Bucket:

        http://<mystorageaccount>.blob.core.windows.net
'''

ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789-."

def validatePermutation(permutation: str) -> bool:
    """
        Validates a S3 bucket name permutation by checking if it meets the following criteria:
            - The permutation is between 3 and 63 characters in length.
            - The permutation contains only lowercase letters, numbers, "." or "-".
            - Doesn't start by "-" or "."
        
        Args:
            permutation (str): The S3 bucket name permutation to be validated.

        Returns:
            bool: True if the permutation is valid, False otherwise.
    """

    # Set True by default
    is_valid_permutation = True

    # length between 3 and 63
    if 3 <= len(permutation) <= 63:
        # All characters are allowed
        if all(char in ALLOWED_CHARACTERS for char in permutation) and not (permutation.startswith(".") or permutation.startswith("-")):
            is_valid_permutation = True

        else:
            # Invalid characters in Storage Account
            is_valid_permutation = False

    else:
        # Invalid Storage Account length
        is_valid_permutation = False

    return is_valid_permutation



def permutation(company_name: str, keywords: list[str], regions: list[str]) -> list[str]:
    """
        Generates permutations of S3 bucket names by combining company name, keywords, and resources.

        Args:
            company_name (str): The company name to be used in the S3 bucket names.
            keywords (list[str]): A list of keywords to be included in the S3 bucket names.
            regions (list[str]): A list of the different AWS Regions

        Returns:
            list[str]: A list of potential S3 bucket names built from the permutations. 

        Note:
            In this first version, we will skip the region as AWS redirect the search
    """

    permutations = []

    # Add base case with company name as storage account
    permutations.append(f"{company_name}")

    for keyword in keywords:
        ############################## PREPEND ##############################

        # Prepend company name to keywords -> <keyword><company_name>
        permutation = None
        permutation = f"{keyword}{company_name}"
        # Validate permutation and add it to the list if valid
        permutations.append(permutation) if validatePermutation(permutation) else None

        # Prepend company name to keywords with a "." -> <keyword>.<company_name>
        # permutation = None
        # permutation = f"{keyword}.{company_name}"
        # Validate permutation and add it to the list if valid
        # permutations.append(permutation) if validatePermutation(permutation) else None

        # Prepend company name to keywords with a "-" -> <keyword>-<company_name>
        permutation = None
        permutation = f"{keyword}-{company_name}"
        # Validate permutation and add it to the list if valid
        permutations.append(permutation) if validatePermutation(permutation) else None

        ############################## APPEND ##############################

        # Append company name to keywords -> <company_name><keyword>
        permutation = None
        permutation = f"{company_name}{keyword}"
        # Validate permutation and add it to the list if valid
        permutations.append(permutation) if validatePermutation(permutation) else None

        # Append company name to keywords with a "." -> <keyword>.<company_name>
        # permutation = None
        # permutation = f"{company_name}.{keyword}"
        # Validate permutation and add it to the list if valid
        # permutations.append(permutation) if validatePermutation(permutation) else None

        # Append company name to keywords with a "-" -> <keyword>-<company_name>
        permutation = None
        permutation = f"{company_name}-{keyword}"
        # Validate permutation and add it to the list if valid
        permutations.append(permutation) if validatePermutation(permutation) else None

    return permutations



async def fetchALL(session: aiohttp.ClientSession, s3: str) -> str:
    """
        Performs asynchronous GET HTTP requests for a list of URLs and returns a list of URLs that return a 200 status code.

        Args:
            S3 (str): The FQDN of the S3 Bucket Name.

        Returns:
            str: The storage_account (FQDN) if the DNS lookup is successful, otherwise raises an exception.
    """

    try:
        async with session.get(s3) as response:

            # If the bucket exists: HTTP status code 200
            if str(response.status).startswith("200"):

                print(f'\t[{AWS_S3_BUCKET}] Exposed S3 Bucket found in: {s3}')

                return s3


    except aiohttp.client_exceptions.ClientOSError as e:
            # If we get a peer reset connection error we will call this funcion again
            print(f"\t[{WARNING}] aiohttp error for {s3} - {e}")

            async with session.get(s3) as response:
                print(f"\t\t[{INFO}] Trying again {s3}")
                await fetchALL(session, s3)

    except Exception as e:
            pass
            # print(f'\t\t[{ERROR}]Unexpected exception - fetchALL - {e}')
            ##############################################################
            # Mirar otros status code como el 402 Forbidden




async def checkS3Bucket(S3_buckets: list[str]) -> list[str]:
    """
        Performs asynchronous DNS lookups for a list of S3 Bucket Names.

        Args:
            S3_buckets (list[str]): A list of S3 FQDNs to check.

        Returns:
            list[str]: A list of s· FQDNs that successfully resolved the DNS lookup.
    """

    tasks = []

    async with aiohttp.ClientSession(trust_env = True) as session:
        # Create list of tasks. In this case all the URLs to be checked
        for s3 in S3_buckets:
            tasks.append(asyncio.ensure_future(fetchALL(session, s3)))
        
        # Execute them in concurrent manner
        results = await asyncio.gather(*tasks)

        # Return only successful requests, http status code 200
        return [result for result in results if result is not None]



def findS3Buckets(company: str, keywords: list[str], resources: list[str], regions: list[str]) -> list[str]:
    """
        Finds valid S3 Bucket names based on permutations of company name, keywords, region and resources.

        Args:
            company (str): The company name to be used in the S3 Bucket.
            keywords (list[str]): A list of keywords to be included in the S3 Bucket names.
            resources (list[str]): A list of AWS resources to be appended to the S3 Bucket names.
            regions (list[str]): Alist of AWS Regions.

        Returns:
            list[str]: A list of valid S3 Bucket FQDNs generated from the permutations.
    """

    s3 = []
    valid_s3 = []
    fqdn = []

    # Get permutations for company and keywords
    s3 = permutation(company, keywords, regions)

    for resource in resources:
        # Append the S3 Bucket to each resource
        fqdn.extend(["".join(["https://", bucket, ".", resource]) for bucket in s3])

    # Check if fqdn (S3 Bucket Names) are valid using asynchronous tasks
    loop = asyncio.get_event_loop()
    valid_s3 .extend(loop.run_until_complete(checkS3Bucket(fqdn)))

    # Return the list of valid S3 FQDNs
    return valid_s3 