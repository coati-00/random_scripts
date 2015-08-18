import sys, getopt, os
# we are importing * to avoid typing .subprocess all the time...
from subprocess import *
from time import sleep
from optparse import *

#os.environ('env_var')
#private_key = os.environ['EC2_KEYPAIR']

def get_args(args):
    parser = OptionParser()
    parser.add_option("-k","--key", dest ="key", help = "key to use", default = "new_inst")
    parser.add_option("-v", "--verbose", dest = "verbose", action="store_false", help="Use this script to start an ec2     instance in the cloud")
    parser.add_option("-i","--instance", dest="instance", help = "instance to attach to" )
    parser.add_option("-m","--method", dest="method", help = "method to use for back up", default = "dd" )
    parser.add_option("-t","--tag", dest = "tag", help = "volume to attach, if none specified, one will be created" )
    parser.add_option("-d","--directory", dest = "directory", help = "directory to back up")
    options, args = parser.parse_args(args)
    return options


def start_instance(options):
    # since start instance is only called if the user does not specify one
    # to use we can just leave this variable here
    # print "start instance"
    start_instance = Popen(["ec2-run-instances", "-k", str(options.key), "ami-b232d0db"], stdout=PIPE)
    sleep(30)
    text = start_instance.stdout.read()
    split = text.split()
    instance =split[5]
    options.instance = instance
    print "end start instance"
    return options.instance 


#even if user does not specify instance at the command line start instance will still store it in options
def describe_instance(options):
    print "describe instance"
    describe_instance = Popen(["ec2-describe-instances", options.instance] , stdout=PIPE)
    sleep(25)
    describe_out = describe_instance.stdout.read()
    split_info = describe_out.split()
    dns = split_info[7]
    #region_id = split_info[1]
    
    while dns == 'pending':
        sleep(10)
        describe_instance = Popen(["ec2-describe-instances", options.instance], stdout=PIPE)
        describe_out = describe_instance.stdout.read()
        split_info = describe_out.split()
        dns = split_info[7]
        #region_id = split_info[14]
    region_id = split_info[14]
    print str(dns)
    print str(region_id)
    print "end describe instance"
    #must return the two as a list
    instance_string = [dns, region_id]
    return instance_string


### up to here dns, instance, and region_id taken care of
#size goes across get size and create volume
def get_size(options, dns):
    print "start size"
    size = None
    #for some reason will not ssh in,
    
    if options.method == 'rsync':
        print "enter rsync"
        #file_size = Popen(["ssh", "-k", str(options.key),"root@"+str(dns), "du", str(options.directory)], stdout = PIPE)
        file_size = Popen(["ssh", "-i", str(options.key), "root@"+str(dns), "du", str(options.directory)], stdout = PIPE)
        sleep(15)
        print "waiting for response"
        file_s = file_size.stdout.read()
        #sleep(15)
        print file_s
        s = file_s.split()
        if len(s) <= 0:
            print "host not found"
            return

        size = ((int(s[0]) * 2)/(1024*1024)) + 3; #int
        print "size"


    elif options.method == 'dd':
        #file_size = Popen(["ssh", "-k", str(options.key), "root@"+str(dns), "fdisk", "-s", str(options.directory)], stdout = PIPE)
        file_size = Popen(["ssh", "-i", str(options.key), "root@"+str(dns), "fdisk", "-s", str(options.directory)], stdout = PIPE)
        
        #file_size = Popen(["ssh", "root@"+str(dns), "fdisk", "-s", str(options.directory)], stdout = PIPE)
        sleep(50)
        file_s = file_size.stdout.read()
        
        print file_s
        s = file_s.split()
        print s
        if len(s) <= 0:
            print "host not found"
            return
        size = ((int(s[0]) * 2)/(1024*1024)) + 3;
    return size


#just going to assign volume to tag in options
def create_volume(options, size, region_id):
    print "start volume"
    create_volume = Popen(["ec2-create-volume", "-s", str(size) , "-z" + str(region_id)], stdout = PIPE)
    sleep(30)
    volume_outp = create_volume.stdout.read()
    v = volume_outp.split()
    #volume = v[1]
    options.tag = v[1]
    print "end volume"
    return


def attach_volume(options, dns):
    print "begin attach volume"
    attach_volume = os.system("ec2-attach-volume " + str(options.tag) + " -i " + str(options.instance) + " -d  sdh")
    #no matter what method is used for the actual back up, the mounting and formating of the volume is the same
    format_volume = Popen(["ssh", "root@"+str(dns), "yes" , "|",  "mkfs", "-t", "ext3", "/dev/sdh"], stdout = PIPE)
    sleep(30)
    mkdir_data_store = Popen(["ssh", "root@"+str(dns), "mkdir", "/mnt/data-store"], stdout = PIPE)
    sleep(10)
    read_mkdir = mkdir_data_store.stdout.read()
    mnt_dev_sdh = Popen(["ssh", "root@"+str(dns), "mount", "/dev/sdh", "/mnt/data-store"], stdout = PIPE)
    sleep(10)
    read_mnt = mnt_dev_sdh.stdout.read()
    print "end attach volume"
    return


def back_up_dd(options, dns):

    dd = Popen(["ssh", "root@"+str(dns), "dd", "bs=65536", "if="+str(options.directory), "of=/dev/sdh"], stdout = PIPE)
    sleep(30)
    read_dd = dd.stdout.read()
    print read_dd
    return

def back_up_rsync(options, dns):
    rsync = Popen(["ssh", "root@"+str(dns), "rsync", "-arvh", str(options.directory), "/mnt/data-store"], stdout = PIPE)
    sleep(30)
    read_rsync = rsync.stdout.read()
    print read_rsync
    return


if __name__ == "__main__":

    instance_string = []
    size_def = ''
    region = ''
    dns_s = ''

    ops = get_args(sys.argv[1:])
    
    # need to start by checking that directory was entered
    if not ops.directory:
        print "You must specify the directory you wish to back up. \n e.g.: python new_backup.py -d directory_name \n OR \n --directory directory_name \n"
        sys.exit(0)


    # check method and set to dd if it is anything other than rsync
    if ops.method == 'rsync':
        method = 'rsync'
    else:
        method = 'dd'
   

    # check to see if instance was specified
    if not ops.instance:
        start_instance(ops)    

    
    instance_string= describe_instance(ops)
    # Is it assumed to be a string
    dns_s = instance_string[0]
    print dns_s
    region = instance_string[1]
    print region


    # check to see if tag was given
    # if no volume was specified via tag flag, create a volume of the
    # appropriate size and attach
    # attach volume takes dns so we pass it
    if ops.tag:
        attach_volume(ops)
    elif not ops.tag:
        size_def = get_size(ops, dns_s)
        no_int = str(size_def)
        n_size = no_int.split()
        last_size = n_size[0]
        create_volume(ops, last_size, region)
        attach_volume(ops, dns_s)

    # back up volume depending on method
    # this is a bit redundant, but I had to check method before so get_size()
    # would use the appropriate technique to check file size
    if ops.method == "rsync":
        back_up_rsync(ops, dns_s)
    elif ops.method == "dd":
        back_up_dd(ops, dns_s)
