from MicrosoftAzure.storageAccounts import findStorageAccounts
from MicrosoftAzure.containers import findContainers
from MicrosoftAzure.blobs import getBlobs
from config import INFO, NO_RESULTS
from utils import writeBlobs

def Azure(companies: list[str], keywords: list[str], resources: list[str]):

    storage_account = []
    containers = []

    for company in companies:
        print(f"[{INFO}] Searching Storage Accounts for company: {company}")
        storage_accounts = findStorageAccounts(company, keywords, resources)

        if len(storage_accounts) == 0:
            print(f"\t[{NO_RESULTS}] No Storage Accounts found for company: {company}")
        
        else:
            for storage_account in storage_accounts:
                print(f"\t\t[{INFO}] Searching Containers for Storage Account: {storage_account}")
                containers_results = findContainers(storage_account, company, keywords)

                if len(containers_results) == 0:
                    print(f"\t\t\t[{NO_RESULTS}] No Containers found for Storage Account: {storage_account}")

                else:
                    # Add the containers to the list of containers to show them at the end of the script execution
                    containers.extend(containers_results)

                    # Get the blobs for each container
                    for container in containers_results:
                        blobs, container_name = getBlobs(storage_account, container)

                        if len(blobs) == 0:
                            print(f"\t\t\t\t[{NO_RESULTS}] Blob is empty for Container: {container}")
                        
                        else:
                            # Write the blobs to a CSV file
                            writeBlobs(blobs, company, storage_account, container_name)

    print(containers.__str__())
