#!/usr/bin/env python

import os
import json
import time
import argparse
import urllib2

BACKUP_FILE = 'nomad_jobs_backup.json'

def backup(url, s3_backup=False, s3_bucket_name=None):

    def get_job_list():
        nomad_jobs_url = "{}/v1/jobs".format(url)
        try:
            req = urllib2.urlopen(nomad_jobs_url)
            jobs = json.loads(req.read())
            return jobs
        except:
            print "unable to get job list from {}".format(url)
            exit(1)
    def get_job(job_id):
        job_url = "{}/v1/job/{}".format(url, job_id)
        try:
            req = urllib2.urlopen(job_url)
            job_spec = json.loads(req.read())
            return job_spec
        except:
            print "unable to get job {} ...bailing".format(job_id)
            exit(1)

    formatted_job_list = []
    raw_job_list = get_job_list()
    for job in raw_job_list:
        if job['Status'] == "running":
            job_id = job['ID']
            formatted_job_list.append({"job":get_job(job_id)})
    _f = open(BACKUP_FILE, 'w')
    _f.write(json.dumps(formatted_job_list, indent=4, sort_keys=True))
    _f.close()
    if s3_backup:
        import boto3
        s3 = boto3.resource('s3')
        s3.Object(s3_bucket_name, 'nomad_backups/' + BACKUP_FILE).put(Body=open(BACKUP_FILE, 'rb'))

def restore(url):
    """
    Warning: we don't currently check to see if the job is there/running
    If we start a restore, this function will brute force start all the jobs
    in the BACKUP_FILE
    """
    post_job_url = "{}/v1/jobs".format(url)
    _f = open(BACKUP_FILE, 'r')
    job_list = json.loads(_f.read())
    for job in job_list:
        job_id = job['job']['ID']
        print "restoring {}".format(job_id)
        try:
            time.sleep(3)
            req = urllib2.Request(post_job_url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(job))
            print response.read()
        except:
            print "failed to post {}".format(job_id)

def main():
    FUNCTION_MAP = {
        'backup': backup,
        'restore': restore
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="nomad server url (e.g. http://nomad.example.com:4646); must be specified as the --url option OR set the NOMAD_ADDR env var")
    parser.add_argument("command", choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    if not args.url:
        if os.getenv('NOMAD_ADDR', False):
            args.url = os.getenv('NOMAD_ADDR')
        else:
            parser.print_help()
            exit()
    func = FUNCTION_MAP[args.command]
    func(args.url)

if __name__ == "__main__":
    main()
