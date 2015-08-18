import subprocess, shlex
''' 
 Very silly script to sync all of my github repose with their remotes at work...
 Assumes upstreams have already been set up properly. Good excuse to practice async python
 e.g. make sure subprocess process finishes before moving to the next one.
 Also good excuse to run as celery job.
'''

# indicate what directory holds git repos

# for each subdirectory in that directory...

# double check it is actually a git repo... if not move to next file

#1. git fetch upstream

#2. git checkout master

#3. git merge upstream/master




class SyncGitRepos(object):
    '''I am assuming that this will be used on a directory of repositories,
    should store output somewhere to make a nice formatted report to print at the end.'''

    def __init__(self, final_report):
        self.final_report = {}
        self.repo_report = {'name' : '', 'sync_output' : ''}


    def is_repo(directory):
        isrepo = subprocess.Popen(['git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        output = isrepo.communicate()
        if output[1] != '':
            return {'is_repo' : False }
        if output[0] != '':
            return {'is_repo' : True, 'branch': output[0]}

    def commit_changes(repo_name):
        '''At first I thought about checking to see if repo is currently on master, but in the end the number of conditionals for functionality seemed silly and doesn't really matter'''
        commit_changes = subprocess.Popen(['git', 'commit', '-a', '-m', 'auto commit'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        output = commit_changes.communicate()
        if output[1] != '':
            return {'commit_output' : output[1], 'commit_status' : False }
        if output[0] != '':
            return {'commit_output' : output[0], 'commit_status': True }

    def checkout_master(repo_name):
        checkout_master = subprocess.Popen(['git', 'checkout', 'master'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        output = checkout_master.communicate()
        if output[0] != '':
            return {'master_output' : output[0], 'master_status': True }
        if output[1] != '':
            return {'master_output' : output[1], 'master_status' : False }


    def has_remote_upstream():
        '''First make sure repository has a remote upstream,
        if it doesn't... idk? print line saying X repository
        has no upstream? If there is - fetch it, then merge'''
        has_upstream = subprocess.Popen(['git', 'remote', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        output = has_upstream.communicate()
        if output[1] != '':
            return {'upstream_output' : output[1], 'upstream_status' : False }
        if output[0] != '':
            new_output = shlex.split(output[0]):
            if 'upstream' in new_output:
                return {'upstream_output' : output[0], 'upstream_status': True }
        else:
            pass


    def fetch_remote_upstream():
        '''First make sure repository has a remote upstream,
        if it doesn't... idk? print line saying X repository
        has no upstream? If there is - fetch it, then merge'''
        fetch_upstream = subprocess.Popen(['git', 'fetch', 'upstream'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        output = fetch_upstream.communicate()
        if output[1] != '':
            return {'fetch_upstream_output' : output[1], 'fetch_upstream_status' : True }
        if output[0] != '':
            return {'fetch_upstream_output' : output[0], 'fetch_upstream_status' : True }


    def merge_remote_upstream():
        '''First make sure repository has a remote upstream,
        if it doesn't... idk? print line saying X repository
        has no upstream? If there is - fetch it, then merge'''
        merge_upstream = subprocess.Popen(['git', 'merge', 'upstream/master'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        output = merge_upstream.communicate()
        if output[1] != '':
            return {'merge_upstream_output' : output[1], 'merge_upstream_status' : False }
        if output[0] != '':
            return {'upstream_output' : output[0], 'upstream_status': True }


    def traverse_directory():
        '''Go over each subdirectory and update.'''


