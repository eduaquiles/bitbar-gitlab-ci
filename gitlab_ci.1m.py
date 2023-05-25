#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# <xbar.title>Gitlab CI</xbar.title>
# <xbar.desc>Shows currently running pipelines from your GitLab in your bar.</xbar.desc>
# <xbar.version>v0.21</xbar.version>
# <xbar.author>Eduardo Aquiles, Martin Kluska</xbar.author>
# <xbar.author.github>eduaquiles, pionl</xbar.author.github>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.image>https://raw.githubusercontent.com/pionl/bitbar-gitlab-ci/master/gitlab_ci.png</xbar.image>
# <xbar.abouturl>https://github.com/pionl/bitbar-gitlab-ci</xbar.abouturl>
#

import json

from urllib.request import urlopen


INSTANCES = [
    {
        # Your private key for accessing gitlab: User -> Settings -> Access tokens -> add personal access token with api scope
        'privateToken': 'token',
        # Gitlab URL
        'url': 'https://gitlab.example.com',
        # Define your server and projects (name: id)
        # To get id go to project -> Settings -> General -> General project settings
        'projects': {
            "React": 3,
        },
    },
]

pipelines = []

# Converts the gitlab status to emoji
def stateIcon(status):
    mapping = {
        "created": "🧱",
        "pending": "⏳",
        "running": "⚙️",
        "failed": "💣",
        "success": "✔️",
        "skipped": "➰",
        "manual": "⌨️"
    }
    return mapping.get(status,"😬")

# Calls gitlab API endpoint with private_token
def api (instance, method):
    url = instance['url'] + "/api/v4/" + method
    param = 'private_token=' + instance['privateToken']
    # Detect if method has query string (we need to append private token)
    url = url + (('&') if "?" in url else ('?')) + param
    body = urlopen(url).read()
    return json.loads(body.decode('utf-8'))

# Project details
class Project:
    def __init__ (self, name, id):
        self.name = name
        self.id = id

# Pipeline job
class Job:
    def __init__ (self, json):
        self.name = json["stage"] + (": " + json["name"] if json["name"] != json["stage"] else "" )
        self.status = json["status"]
        self.duration = 0 if json["duration"] is None or self.status == 'running' else int(json["duration"])
        self.commit = json['commit']['title']

    # Jobs name with duration
    def displayName(self):
        return self.name + (' ' + str(self.duration) + 's' if self.duration > 0 else '')
    
# Pipeline
class Pipeline:
    def __init__ (self, projectName, projectId, json):
        self.project = Project(projectName, projectId)
        self.id = json["id"]
        self.jobs = []
        self.ref = str(json["ref"])
        self.status = json["status"]
        self.commit = None

    # Display name with current running jobs
    def displayName(self):
        return self.project.name + ' - ' + self.ref + ' (' + stateIcon(self.status) + ')'

    # Add jobs array json
    def addJobs(self, jobsArray):
        for jobJson in jobsArray:
            # Parse the job
            job = Job(jobJson)
            # Add the jobs array
            self.jobs.append(job)

            # Get the commit from the first job
            if self.commit is None:
                self.commit = job.commit

# Loop the projects and get the jobs
for instance in INSTANCES:
    for name, project in instance['projects'].items():
        collectedPipelines = [api(instance, "projects/"+str(project)+"/pipelines/latest?ref=master")]

        for pipelineJson in collectedPipelines:
            pipeline = Pipeline(name, project, pipelineJson)
            jobsArray = api(instance, "projects/"+str(project)+"/pipelines/"+str(pipeline.id)+"/jobs")
            if len(jobsArray) > 0:
                pipeline.addJobs(jobsArray)
                pipelines.append(pipeline)

pipelineCount = len(pipelines)
if pipelineCount == 0:
    print("❓")
    exit


## Render the pipelines names (xbar will loop)
statuses = []
for index, pipeline in enumerate(pipelines):
    statuses.append(stateIcon(pipeline.status))
print("🤖 " + "".join(statuses))

## Start menu
print("---")

for pipeline in pipelines:
    print('🚂 ' + pipeline.project.name + ' - ' + pipeline.ref + '| color=black')
    print('-- commit: ' + pipeline.commit + '| color=black')
    print('---')
    for job in pipeline.jobs:
        style = ''
        if job.status == 'success':
            style = '| color=green'
        elif job.status == 'running':
            style = '| color=blue'

        print (stateIcon(job.status) + " " + job.displayName() + style)
