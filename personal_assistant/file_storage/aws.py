"""
import boto3
from botocore.exceptions import NoCredentialsError


def create_user_folder(user_id):
    s3 = boto3.client('s3')
    bucket_name = 'personal-assistant-for-django-project-bucket'

    folders = ['documentations/', 'images/', 'videos/', 'music/']

    try:
        for folder in folders:
            s3.put_object(Bucket=bucket_name, Key=f"{user_id}/{folder}")
    except NoCredentialsError:
        print("Помилка: Немає доступу до AWS. Перевірте ваші облікові дані.")
"""