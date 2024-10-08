from azure.storage.blob import BlobServiceClient
import base64



def getBlobs(storage_account: str, container_url: str) -> list[dict]:
    """
        Retrieves a list of blobs from a given container in a storage account.

        Args:
            storage_account (str): The storage account name.
            container (str): The container name.

        Returns:
            list[dict]: A list of dictionaries containing blob information.
    """

    blobs = []

    # From this: "https://<mystorageaccount>.blob.core.windows.net/<mycontainer>?restype=container&comp=list"; to this: "<mycontainer>"
    container = container_url.split("/")[3].split("?")[0]

    # Create a BlobServiceClient object with the storage account URL
    blob_service_client = BlobServiceClient(
        account_url = storage_account,
    )

    # Get a reference to the container
    container_client = blob_service_client.get_container_client(container)

    # List all blobs in the container
    for blob in container_client.list_blobs():

        blob_dict = {}
        blob_dict["name"] = blob.__dict__.get("name")
        blob_dict["container"] = blob.__dict__.get("container")
        blob_dict["url"] = "".join([storage_account, "/", container, "/", blob.name])
        blob_dict["creation_time"] = blob.__dict__.get("creation_time").strftime("%Y-%m-%d %H:%M:%S")
        blob_dict["last_modified"] = blob.__dict__.get("last_modified").strftime("%Y-%m-%d %H:%M:%S")
        blob_dict["blob_type"] = blob.__dict__.get("blob_type").name
        blob_dict["etag"] = blob.__dict__.get("etag")
        blob_dict["size"] = blob.__dict__.get("size")
        blob_dict["content_type"] = blob.__dict__.get("content_settings").get("content_type")        
        blob_dict["content_encoding"] = blob.__dict__.get("content_settings").get("content_encoding")
        blob_dict["content_language"] = blob.__dict__.get("content_settings").get("content_language")
        blob_dict["content_md5"] = base64.b64encode(blob.__dict__.get("content_settings").get("content_md5")).decode("utf-8") if blob.__dict__.get("content_settings").get("content_md5") is not None else None
        blob_dict["status"] = blob.__dict__.get("lease").get("status")
        blob_dict["state"] = blob.__dict__.get("lease").get("state")

        blobs.append(blob_dict)

    return (blobs, container)