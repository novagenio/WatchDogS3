import logging
from botocore.exceptions import ClientError
import boto
import sys
import boto.s3.connection
from boto.s3.key import Key

access_key = 'BE4KJ06MVZWWFAZN5LQD'
secret_key = '8AGvAwBUnu98FB95GLMuneD+Yz9U8siEe/zEKSpX'

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 's3.boaw.cloudstorage.corp',
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )


bucket = conn.get_bucket('scib-pro-pr-entits-portal-sbgm')
for key in bucket.list():
        print ("{name}\t{size}\t{modified}".format(
                name = key.name,
                size = key.size,
                modified = key.last_modified,
                ))


 
        
