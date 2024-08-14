# coding=utf-8
# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)
"""
ossUtil.py: Provides utility functions for Alibaba Cloud OSS object storage service.

This module defines a function `uploadFileAndGetLink`, which uploads a local file to OSS
and returns a temporary access link after successful upload.
"""

import oss2
import os
from oss2.credentials import EnvironmentVariableCredentialsProvider


def upload_file_and_get_link(local_path: str, file_name: str) -> str:
    """
    Uploads a file to OSS and gets a timed access link.
    Refer:https://help.aliyun.com/zh/oss/user-guide/simple-upload

    Parameters:
        local_path (str): The local path of the file to be uploaded.
        file_name (str): The name of the file once uploaded to OSS.

    Returns:
        str: A timed access link provided by OSS, valid for 3600 seconds.
    """
    # Get access credentials
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())

    # Initialize the Bucket instance
    bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'examplebucket')

    # Open the local file for uploading
    with open(local_path, 'rb') as fileobj:
        # Position the file pointer at the 1000th byte
        fileobj.seek(1000, os.SEEK_SET)
        current = fileobj.tell()
        # Upload the file to OSS
        bucket.put_object(file_name, fileobj)

    # Generate a timed access link valid for 3600 seconds
    url = bucket.sign_url('GET', file_name, 3600, slash_safe=True)
    # Output the generated link
    print('The signed URL is:', url)
    # Return the link
    return url
