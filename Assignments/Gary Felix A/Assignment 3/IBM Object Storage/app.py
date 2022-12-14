from flask import Flask, redirect, url_for, render_template, request
import ibm_boto3
from ibm_botocore.client import Config, ClientError

# Constants for IBM COS values
# Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
# eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_API_KEY_ID = "a42xSVrV_ZfS6eFbQg9wEDWJgeRnmyC86291kk2pg6YO"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/f00ce1f2bfdb4304a7cc3add45c10df4::serviceid:ServiceId-5705ffef-0d85-471b-8976-35e786dbcd5c"
# eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003xxxxxxxxxx1c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

# Create resource
cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT
                         )

app = Flask(__name__)


def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

@app.route('/')
def index():
    files = get_bucket_contents('customercare')
    return render_template('index.html', files=files)


if __name__ == '__main__':
    app.run(debug=True)