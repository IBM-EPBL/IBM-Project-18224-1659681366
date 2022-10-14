import ibm_boto3
from flask import Flask, render_template
from ibm_botocore.client import Config, ClientError

# COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
# COS_API_KEY_ID = "W9RHwIKs7oFwWKFL7ccCMv-VZvUkOKIVeqkvjQSzu81"
# COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/ae470778003340e28f0fe69a3cb8a7cb::serviceid:ServiceId-0ca7d771-103e-49c3-a32b-589130fefabb"
# Constants for IBM COS values

COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
# eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_API_KEY_ID = "a42xSVrV_ZfS6eFbQg9wEDWJgeRnmyC86291kk2pg6YO"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/f00ce1f2bfdb4304a7cc3add45c10df4::serviceid:ServiceId-5705ffef-0d85-471b-8976-35e786dbcd5c"

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
    files = get_bucket_contents('demo-kiot-customer-care')
    return render_template('index.html',files=files)

app.run(debug=True)


