import sys, os
from subprocess import *
from time import sleep
from optparse import *
dns = 'pending'
ami = ''
key = ''


parser = OptionParser()
parser.add_option("-a", "--ami", dest="ami", help="ami to use to start image")
parser.add_option("-k","--key", dest="key" )
#parser.add_option("-","", dest= )
parser.add_option("-v", "--verbose", action="store_false", dest="verbose", default=True, help="Use this script to start an ec2 instance in the cloud")


(options, args) = parser.parse_args()


if ami == '' and key == '':
    key = 'new_inst'
    ami = 'ami-b232d0db'
    start_instance = Popen(["ec2-run-instances", str(ami), "-k", str(key)], stdout=PIPE)

    sleep(30)
    text = start_instance.stdout.read()
         sleep(15)
         split = text.split()
         instance = split[5]
         #region_id = split[12]

         describe_instance = Popen(["ec2-describe-instances", instance] , stdout=PIPE)
         sleep(30)
         describe_out = describe_instance.stdout.read()
         split_dns = describe_out.split()

         dns = split_dns[7]
         while dns == 'pending':
        sleep(10)
        describe_instance = Popen(["ec2-describe-instances", instance], stdout=PIPE)
        describe_out = describe_instance.stdout.read()
        split_dns = describe_out.split()
        dns = split_dns[7]


         print instance
         print dns


elif ami != '' and key != '':
     start_instance = Popen(["ec2-run-instances", str(ami), "-k", str(key)], stdout=PIPE)

         sleep(30)
         text = start_instance.stdout.read()
         sleep(15)
         split = text.split()
         instance = split[5]
         #region_id = split[12]

         describe_instance = Popen(["ec2-describe-instances", instance] , stdout=PIPE)
         sleep(30)
         describe_out = describe_instance.stdout.read()
         split_dns = describe_out.split()

         dns = split_dns[7]
         while dns == 'pending':
        sleep(10)
        describe_instance = Popen(["ec2-describe-instances", instance], stdout=PIPE)
        describe_out = describe_instance.stdout.read()
        split_dns = describe_out.split()
        dns = split_dns[7]


         print instance
         print dns

elif ami != '' and key == '':
     key = 'new_inst'
     start_instance = Popen(["ec2-run-instances", str(ami), "-k", str(key)], stdout=PIPE)

         sleep(30)
         text = start_instance.stdout.read()
         sleep(15)
         split = text.split()
         instance = split[5]
         #region_id = split[12]

         describe_instance = Popen(["ec2-describe-instances", instance] , stdout=PIPE)
         sleep(30)
         describe_out = describe_instance.stdout.read()
         split_dns = describe_out.split()

         dns = split_dns[7]
         while dns == 'pending':
        sleep(10)
        describe_instance = Popen(["ec2-describe-instances", instance], stdout=PIPE)
        describe_out = describe_instance.stdout.read()
        split_dns = describe_out.split()
        dns = split_dns[7]


         print instance
         print dns
