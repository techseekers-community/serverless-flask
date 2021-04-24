import boto3
from config import CONFIGURATION_SET
from botocore.exceptions import ClientError

sns = boto3.client('sns')
ses = boto3.client('ses')


def send_email(sender, reciepient, bodyHtml, bodyText, subject):
    try:
        # Provide the contents of the email.
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    reciepient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': bodyHtml,
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': bodyText,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source=sender,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e)
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def send_sms(phonenumber, message):
    sns.publish(
        PhoneNumber=phonenumber,
        Message=message
    )
