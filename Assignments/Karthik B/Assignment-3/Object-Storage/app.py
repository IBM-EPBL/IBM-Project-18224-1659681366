import ibm_boto3
from flask import Flask, render_template
from ibm_botocore.client import Config, ClientError

# COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
# COS_API_KEY_ID = "W9RHwIKs7oFwWKFL7ccCMv-VZvUkOKIVeqkvjQSzu81"
# COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/ae470778003340e28f0fe69a3cb8a7cb::serviceid:ServiceId-0ca7d771-103e-49c3-a32b-589130fefabb"
# Constants for IBM COS values

COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "VD6MiVWCpvX0hZaSJsJK3F7Md8B6xZwN6K8GQUxoJivR" # eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/06397f70d4304e24ace970469e8fb2e5::serviceid:ServiceId-55e185ee-009a-42ce-ba50-5b5b67af5689"


cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

app=Flask(__name__)

def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names=[]
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

@app.route('/')
def home():
    files = get_bucket_contents('demo-kiot')
    return render_template('index.html',files=files)

app.run(debug=True)


