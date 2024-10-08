# ForgottenClouds

This script searches for Azure Storage Accounts and Azure Blob Containers that are not properly configured and exposed to Internet. It uses a combination of keywords, Azure resources, and company names to find potential candidates. 

## Setup

```bash
# Clone the repository
git clone https://github.com/blackpuncture/ForgottenClouds.git

# Move to the repository directory
cd ForgottenClouds

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages 
pip install -r requirements.txt
```

## Usage

Before running the script, you need to configure the following files:

1. `App/Data/Companies.txt`: Add your company names to this file, one per line.
2. `App/Data/AzureResources.txt`: Add your Azure resources to this file, one per line.
3. `App/Data/Keywords.txt`: Add your keywords to this file, one per line. These keywords will be used to do permutations with the company name to find potential Azure Storage Accounts.
4. `App/Data/Containers.txt`: Add your Azure Blob Containers to this file, one per line. These keywords will be used to do permutations with the company name to find potential containers for the Azure Storage Accounts found previously

> Note: [Check out this file for additional keywords](https://github.com/NetSPI/MicroBurst/blob/master/Misc/permutations.txt)

Once you have configured the files, you can run the script using the following command:

```bash
# Move to App directory
cd App

# Execute the tool
python ForgottenClouds.py
```

The script will search for Azure Storage Accounts and Azure Blob Containers that match the keywords, Azure resources, and company names. It will then print the results to the console.

## References

- [Azure Storage Accounts](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-overview)
- [mrd0x.com - Easy Bounty With Exposed Buckets & Blobs](https://mrd0x.com/easy-bounty-with-exposed-buckets-and-blobs/)
