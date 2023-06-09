#!/usr/bin/env python3

import boto3
import botocore
import os

def main():
    configure_aws_access()
# test_aws_access() attempts to access aws API via boto3.client('iam'). 
# Returns True if AWS access is properly configured, False otherwise.
def test_aws_access(conf_access_key_id, conf_secret_access_key, conf_region_name):
    try:
        sts = boto3.client('sts', region_name=conf_region_name, aws_access_key_id=conf_access_key_id, aws_secret_access_key=conf_secret_access_key) # Test if aws access is configured by attempting to use "boto3.client('iam')".
        sts.get_caller_identity()
        return True
    except botocore.exceptions.UnauthorizedSSOTokenError as e:
        return False
    except botocore.exceptions.NoCredentialsError as e:
        print("info: no aws credentials found, proceeding with aws access configuration.")
        return False # Return False if no aws credentials are configured.
    except botocore.exceptions.NoRegionError as e:
        print("info: no aws region specified, proceeding with aws access configuration.")
        return False # Return False if no aws region is configured.
    except Exception as e:
        print(f"error: {e}")
        return False
    return True

def prompt_for_information(name, message):
    repeat_input_prompt = True
    input_value = None
    while repeat_input_prompt is True:
        repeat_confirm_prompt = True
        input_value = input(f"{message} ({name}): ")
        if len(input_value) > 0:
            while repeat_confirm_prompt is True:
                confirm_value = input(f"input: ({name}: {input_value})\nconfirm (Y/n): ")
                if len(confirm_value) == 0 or confirm_value[:1].lower() == "y":
                    repeat_confirm_prompt, repeat_input_prompt = False, False
                elif confirm_value[:1].lower() == "n":
                    repeat_confirm_prompt = False
    return input_value


def configure_aws_access():
    # TODO: Call a function that prompts the user for aws credential, confirms if credentials are valid, and re-prompts the user 
    # if the credentials are not valid for valid creds endlessly until  valid credentials are provided.
    # TODO: Call a function that
    access_configured = False
    while not access_configured:
        if os.environ.get('AWS_ACCESS_KEY_ID') is None or os.environ.get('AWS_SECRET_ACCESS_KEY') is None or os.environ.get('AWS_REGION_NAME') is None:

            aws_access_key_id = prompt_for_information('AWS_ACCESS_KEY_ID', 'CONF')
            aws_secret_access_key = prompt_for_information('AWS_SECRET_ACCESS_KEY', 'CONF')
            aws_region_name = prompt_for_information('AWS_REGION_NAME', 'CONF')
            if test_aws_access(aws_access_key_id, aws_secret_access_key, aws_region_name):
                os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
                os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
                os.environ['AWS_REGION_NAME'] = aws_region_name
                with open('.env', 'w') as env_file:
                    env_file.write(f"AWS_ACCESS_KEY_ID={aws_access_key_id}\nAWS_SECRET_ACCESS_KEY={aws_secret_access_key}\nAWS_REGION_NAME={aws_region_name}")
                access_configured = True
        else:
            with open('.env', 'r') as env_file:
                for line in env_file.readlines():
                    try:
                        key, value = line.split('=')
                        os.environ[key] = value.strip('\n')
                    except ValueError:
                        pass

            if test_aws_access(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'), os.environ.get('AWS_REGION_NAME')):
                access_configured = True
            else:
                os.environ.pop('AWS_ACCESS_KEY_ID', None)
                os.environ.pop('AWS_SECRET_ACCESS_KEY', None)
                os.environ.pop('AWS_REGION_NAME', None)
                with open('.env', 'w') as env_file:
                    env_file.write('')
if __name__ == "__main__":
    main()