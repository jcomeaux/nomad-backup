
job "nomad-backup" {
    datacenters = [ "shared-services"]
    type = "batch"
    periodic {
        cron = "0 * * * * "
    }
    group "nomad-backup" {
        task "nomad-backup" {

            env {
                NOMAD_URL = "http://nomad.example.com:4646"
                S3_BUCKET_NAME = "my-buckets-name"
            }

            driver = "docker"
            config {
                image = "joelcomeaux/nomad-backup"
                args = [
                    "python",
                    "backup_jobs.py"
                ]
            }
        }
    }
}
