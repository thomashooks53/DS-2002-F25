import boto3
import os
import requests

def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")
        exit(1)

bucket_name = "ds2002-f25-qdg4sd"
object_name = "dancing.gif"
expires_in = 60

file_url = "https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyZmF1OXF5cDB4MzBubnd3M3N5Z2xiNWFncnZvdmM2Z3A5NW5meWcxciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/w7mLEAMcpjrpe/giphy.gif"

local_file = object_name
download_file(file_url, local_file)

s3 = boto3.client("s3", region_name="us-east-1")
s3.upload_file(Filename=local_file, Bucket=bucket_name, Key=object_name)

url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": bucket_name, "Key": object_name},
    ExpiresIn=expires_in
)

print(url)

