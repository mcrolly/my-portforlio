import boto3
import io
import zipfile
import mimetypes
from botocore.client import Config

def lambda_handler(event, context):
    sns =  boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:745127658540:portfolio')

    #initializing location so we can run if job does not exist
    location = {
    "bucketName": "portforliobuild",
    "objectKey": "portfoliobuild.zip"
    }

    try:
        #code for codepipeline
        job = event.get("CodePipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "BuildArtifact":
                    location = artifact["location"]["s3Location"] # location is the name of the bucket

        print(f'Building Potfolio from {location}')
        # s3 = boto3.resource("s3")
        s3 = boto3.resource("s3", config=Config(signature_version='s3v4'))
        # declare buckets
        portfolio_bucket = s3.Bucket('portfolio.mcrolly.com')
        #build_bucket = s3.Bucket('portforliobuild') #commenting hardcoded bucket name
        build_bucket = s3.Bucket(location['bucketName'])


        portfolio_zip = io.BytesIO()
        #build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip) #commenting hardcoded object key
        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                # mime_type = mimetypes.guess_type(nm)[0]
                # portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': str(mime_type)})
                portfolio_bucket.upload_fileobj(obj, nm,
                                                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print('Job Done')
        topic.publish(Subject="Portfolio Deployment Succeeded ", Message="Portfolio Deployed Successfully")
        # Next we need to tell Code CodePipeline that the func executed successfully
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Portfolio Deployment Failed ", Message="Portfolio Deployment failed")
        raise
    return "Hello from Lambda"
