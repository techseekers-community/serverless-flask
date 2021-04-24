import os
import boto3
from loguru import logger
import datetime
from boto3.dynamodb.conditions import Key, Attr

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    dynamodb = boto3.resource('dynamodb')

user_table = dynamodb.Table(USERS_TABLE)


class User():

    @staticmethod
    def put_new_user(email, firstName, lastName, dob, gender, password):
        user_table.put_item(
            Item={
                'userId':  email,
                'fname': firstName,
                'lname': lastName,
                'dob':  dob,
                'gender': gender,
                'password': password,
                'registered_on': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                'confirmed': False
            }
        )

    @staticmethod
    def get_user_by_id(user_id):
        resp = user_table.get_item(
            Key={
                'userId': user_id
            }
        )
        return resp['Item'] if 'Item' in resp else None

    @staticmethod
    def confirm_user(user_id):
        user_table.update_item(
            Key={
                'userId': user_id
            },
            UpdateExpression='SET confirmed = :confirmed, confirmed_on = :confirmed_on',
            ExpressionAttributeValues={
                ':confirmed': True,
                ':confirmed_on': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            }
        )
