from colorama import Fore, Style

# Relevant Folders
DATA = "Data" # Data Folder
OUTPUT_FOLDER = "Output" # Output Folder

# Companies 
companies_file = f"{DATA}/Companies.txt"

# Azure
azure_resources_file = f"{DATA}/Azure_Resources.txt"
keywords_file = f"{DATA}/Containers.txt"
containers_file = f"{DATA}/Containers.txt"

# Colorama Stile
INFO = f'{Fore.BLUE}{Style.BRIGHT}INFO{Style.RESET_ALL}'
AZURE_STORAGE = f'{Fore.GREEN}{Style.BRIGHT}AZURE STORAGE{Style.RESET_ALL}'
BUCKET = f'{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}BUCKET{Style.RESET_ALL}'
WORKING = f'{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}WORKING{Style.RESET_ALL}'
CREATION = f'{Fore.CYAN}{Style.BRIGHT}CREATION{Style.RESET_ALL}'
NO_RESULTS = f'{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}NO RESULTS{Style.RESET_ALL}'

DELETION = f'{Fore.LIGHTRED_EX}{Style.BRIGHT}DELETION{Style.RESET_ALL}'
WARNING = f'{Fore.LIGHTRED_EX}{Style.BRIGHT}WARNING{Style.RESET_ALL}'
ERROR = f'{Fore.RED}{Style.BRIGHT}ERROR{Style.RESET_ALL}'