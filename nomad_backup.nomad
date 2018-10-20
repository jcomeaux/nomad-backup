
job "nomad-backup" {
    datacenters = [ "shared-services"]
    type = "batch"
    group "nomad-backup" {
        task "nomad-backup" {

            meta {
                NOMAD_URL = "http://nomad.example.com:4646"
                S3_BUCKET_NAME = "s3-bucket-name-goes-here"
            }

            driver = "docker"
            config {
                image = "joelcomeaux/nomad-backup"
                args = [
                    "python",
                    "local/nomad_backup.py"
                ]
            }

            template {
                data = <<EOH
                from nomad_job_manager import backup

                backup(${NOMAD_META_NOMAD_URL}, s3_backup=True, s3_bucket_name=${NOMAD_META_S3_BUCKET_NAME})
                EOH

                destination = "local/nomad_backup.py"
            }
        }
    }
}
