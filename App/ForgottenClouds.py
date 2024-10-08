from utils import *
from config import *
from MicrosoftAzure.az import Azure


def ForgottenClouds():

    HEADER = '''
                                                                                             ,,                           ,,             
`7MM"""YMM                                  mm     mm                            .g8"""bgd `7MM                         `7MM          OO 
  MM    `7                                  MM     MM                          .dP'     `M   MM                           MM          88 
  MM   d  ,pW"Wq.`7Mb,od8 .P"Ybmmm ,pW"Wq.mmMMmm mmMMmm .gP"Ya `7MMpMMMb.      dM'       `   MM  ,pW"Wq.`7MM  `7MM   ,M""bMM  ,pP"Ybd || 
  MM""MM 6W'   `Wb MM' "':MI  I8  6W'   `Wb MM     MM  ,M'   Yb  MM    MM      MM            MM 6W'   `Wb MM    MM ,AP    MM  8I   `" || 
  MM   Y 8M     M8 MM     WmmmP"  8M     M8 MM     MM  8M""""""  MM    MM      MM.           MM 8M     M8 MM    MM 8MI    MM  `YMMMa. `' 
  MM     YA.   ,A9 MM    8M       YA.   ,A9 MM     MM  YM.    ,  MM    MM      `Mb.     ,'   MM YA.   ,A9 MM    MM `Mb    MM  L.   I8 ,, 
.JMML.    `Ybmd9'.JMML.   YMMMMMb  `Ybmd9'  `Mbmo  `Mbmo`Mbmmd'.JMML  JMML.      `"bmmmd'  .JMML.`Ybmd9'  `Mbod"YML.`Wbmd"MML.M9mmmP' db 
                         6'     dP                                                                                                       
                         Ybmmmd'                                                                                                         
    '''

    print(HEADER)

    # Keywords
    keywords = readTXTFile(keywords_file)
    print(f"[{INFO}] Importing Keywords: {len(keywords)}")

    # Azure Resources
    azure_resources = readTXTFile(azure_resources_file)
    print(f"[{INFO}] Importing Azure Resources: {len(azure_resources)}")

    # Containers
    containers = readTXTFile(containers_file)
    print(f"[{INFO}] Importing Container Names: {len(containers)}")

    # Companies
    companies = readTXTFile(companies_file)
    print(f"[{INFO}] Importing Companies: {len(companies)}")


    ###############################################################################################
    ############################################ AZURE ############################################
    ###############################################################################################

    # Print the action in place
    print(f"[{INFO}] Checking Azure")

    # Execute the flow for Azure Resources
    Azure(companies, keywords, azure_resources)


if __name__ == "__main__":
    ForgottenClouds()

