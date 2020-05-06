import boto3
import io
import zipfile
import mimetypes

def lambda_handler(event, context):

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:443514573025:lambdareact')


    try:
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



        topic.publish(Subject="testreact published!", Message="lambda has successfully deployed testreact")

    except:

        topic.publish(Subject="testreact failed!", Message="lambda has failed deploying testreact")
        raise

    return "all ok here"
