from AWS.s3 import findS3Buckets
from config import INFO, NO_RESULTS

def AWS(companies: list[str], keywords: list[str], aws_resources: list[str], aws_regions: list[str]):
    
    for company in companies:
        print(f"[{INFO}] Searching S3 Buckets for company: {company}")
        s3_buckets = findS3Buckets(company, keywords, aws_resources, aws_regions)

        if len(s3_buckets) == 0:
            print(f"\t[{NO_RESULTS}] No S3 Buckets found for company: {company}")

        else:
            print(s3_buckets.__str__())


