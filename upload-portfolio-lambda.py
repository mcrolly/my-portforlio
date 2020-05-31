import boto3
import io
import zipfile
import mimetypes
from botocore.client import Config

# s3 = boto3.resource("s3")  # if this doesn't work , use the code line below
s3 = boto3.resource("s3", config=Config(signature_version='s3v4'))
# declare buckets
portfolio_bucket = s3.Bucket('portfolio.mcrolly.com')
build_bucket = s3.Bucket('portforliobuild')
# download files
build_bucket.download_file('portfoliobuild.zip', 'd:/build_area\portfoliobuild.zip')

portfolio_zip = io.BytesIO()
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        mime_type = mimetypes.guess_type(nm)[0]
        portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': str(mime_type)})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
