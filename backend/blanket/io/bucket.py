import urllib.parse
from contextlib import asynccontextmanager

import aioboto3

import blanket.io.env as env

BUCKET_NAME = env.getenv("BLANKET_BUCKET_NAME")
BUCKET_ACCESS_KEY_ID = env.getenv("BLANKET_BUCKET_ACCESS_KEY_ID")
BUCKET_SECRET_ACCESS_KEY = env.getenv("BLANKET_BUCKET_SECRET_ACCESS_KEY")
BUCKET_ENDPOINT = env.getenv("BLANKET_BUCKET_ENDPOINT")
BUCKET_REGION = env.getenv("BLANKET_BUCKET_REGION")


@asynccontextmanager
async def get_bucket_client():
    if any(
        v is None
        for v in (
            BUCKET_ACCESS_KEY_ID,
            BUCKET_SECRET_ACCESS_KEY,
            BUCKET_ENDPOINT,
            BUCKET_REGION,
        )
    ):
        raise ValueError("Missing bucket credentials")
    session = aioboto3.Session()
    async with session.client(
        "s3",
        aws_access_key_id=BUCKET_ACCESS_KEY_ID,
        aws_secret_access_key=BUCKET_SECRET_ACCESS_KEY,
        endpoint_url=BUCKET_ENDPOINT,
        region_name=BUCKET_REGION,
    ) as client:
        yield client


async def list_bucket_files(prefix: str, client) -> set[str]:
    paginator = client.get_paginator("list_objects_v2")
    result = set()
    async for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
        for content in page.get("Contents", []):
            result.add(content["Key"])
    return result


async def get_signed_url(
    bucket_path: str,
    client,
    *,
    download_file_name: str | None = None,
    ttl: int = 3600,
    verb: str = "get_object",
    inline: bool = False,
) -> str:
    """
    Get a presigned URL for a file in the bucket.

    Args:
        bucket_path: The path to the file in the bucket.
        client: The S3 client to use.
        download_file_name: The name of the file to download.
        ttl: The time to live for the presigned URL in seconds.
        verb: The HTTP verb to use for the presigned URL.
        inline: If True, set content disposition to inline for browser viewing.
                If False, set to attachment for download.

    Returns:
        A presigned URL for the file.
    """
    if download_file_name is None:
        download_file_name = bucket_path.split("/")[-1]
    extra_params = {}
    if verb == "get_object":
        if inline:
            extra_params["ResponseContentDisposition"] = (
                f"inline; filename={urllib.parse.quote(download_file_name)}"
            )
        else:
            extra_params["ResponseContentDisposition"] = (
                f"attachment; filename={urllib.parse.quote(download_file_name)}"
            )
    url = await client.generate_presigned_url(
        verb,
        Params={
            "Bucket": BUCKET_NAME,
            "Key": bucket_path,
            **extra_params,
        },
        ExpiresIn=ttl,
    )
    return url
