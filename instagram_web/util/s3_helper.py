# AWS related import
import boto3, botocore, secrets, os
from app import app

s3 = boto3.client(
	"s3",
	aws_access_key_id=app.config['S3_KEY'],
	aws_secret_access_key=app.config['S3_SECRET']
)

def random_file_name(file):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(file.filename)
	picture_fn = random_hex + f_ext

	return picture_fn

def upload_file_to_s3(file, bucket_name, acl='public-read'):
	# perform the filename manipulation to prevent same name
	# such as username + date

	try:
		s3.upload_fileobj(
			file,
			bucket_name,
			file.filename,
			ExtraArgs={
				"ACL": acl,
				"ContentType": file.content_type
			}
		)
	except Exception as e:
		return f"Something Happened: {e}"

	return f'{app.config["S3_LOCATION"]}{file.filename}'