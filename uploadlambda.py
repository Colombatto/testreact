import boto3
import io
import zipfile
import mimetypes

myzip = io.BytesIO()

s3 = boto3.resource('s3')
bucket = s3.Bucket('octanktestreact')
bucket.download_fileobj('artifacts/artifacts', myzip)


target = boto3.resource('s3')
target = s3.Bucket('octankvideostatic')

with zipfile.ZipFile(myzip) as myzipfile:
    for nm in myzipfile.namelist():
        obj = myzipfile.open(nm)
        target.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
