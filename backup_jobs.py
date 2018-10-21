
from nomad_job_manager import backup
import os


backup(os.environ.get('NOMAD_URL'), s3_backup=True, s3_bucket_name=os.environ.get('S3_BUCKET_NAME'))
