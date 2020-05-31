import boto3
import io
import zipfile
import mimetypes
from botocore.client import Config

def lambda_handler(event, context):
    # s3 = boto3.resource("s3")
    s3 = boto3.resource("s3", config=Config(signature_version='s3v4'))

    sns =  boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:745127658540:portfolio')

    try:
        # declare buckets
        portfolio_bucket = s3.Bucket('portfolio.mcrolly.com')
        build_bucket = s3.Bucket('portforliobuild')
        # download files
        #build_bucket.download_file('portfoliobuild.zip', 'portfoliobuild.zip')

        portfolio_zip = io.BytesIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                # mime_type = mimetypes.guess_type(nm)[0]
                # portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': str(mime_type)})
                portfolio_bucket.upload_fileobj(obj, nm,
                                                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        topic.publish(Subject="Portfolio Deployment Succeeded ", Message="Portfolio Deployed Successfully")
    except:
        topic.publish(Subject="Portfolio Deployment Failed ", Message="Portfolio Deployment failed")
        raise
    return "Hello from Lambda"
