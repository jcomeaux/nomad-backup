
from nomad_job_manager import backup


backup(${NOMAD_URL}, s3_backup=True, s3_bucket_name=${S3_BUCKET_NAME})
