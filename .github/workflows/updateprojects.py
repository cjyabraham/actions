#!/usr/bin/env python3                                                                                                  
#                                                                                                                       
# Copyright this project and it's contributors                                                                          
# SPDX-License-Identifier: Apache-2.0                                                                                   
#                                                                                                                       
# encoding=utf8

import csv
import urllib.request
import json
import os

projectsCsvFile = os.path.dirname(os.path.realpath(__file__))+'/../../_data/projects.csv'

landscapeBaseURL = 'https://landscape.cncf.io'
landscapeHostedProjects = landscapeBaseURL+'/api/items?project=hosted'
landscapeSingleItem = landscapeBaseURL+'/data/items/{}.json'

csvRows = []

with urllib.request.urlopen(landscapeHostedProjects) as hostedProjectsResponse:
    for projectStage in json.load(hostedProjectsResponse):
        for project in projectStage['items']:
            with urllib.request.urlopen(landscapeSingleItem.format(project['id'])) as singleItemResponse:
                projectData = json.load(singleItemResponse)
                print("Processing {}...".format(projectData['name']))
                csvRows.append({
                        'name': projectData['name'],
                        'description': projectData['description'],
                        'homepage_url': projectData['homepage_url'],
                        'project': projectData['project'],
                        'repo_url': project['repo_url'],
                        'logo': projectData['logo'],
                        'twitter': projectData['twitter'],
                        'crunchbase': projectData['crunchbase'],
                        'chat_channel': projectData['extra']['chat_channel'] if 'extra' in projectData and 'chat_channel' in projectData['extra'] else None,
                        'accepted': projectData['extra']['accepted'] if 'extra' in projectData and 'accepted' in projectData['extra'] else None,
                        'dev_stats_url': projectData['extra']['dev_stats_url'] if 'extra' in projectData and 'dev_stats_url' in projectData['extra'] else None,
                        'artwork_url': projectData['extra']['artwork_url'] if 'extra' in projectData and 'artwork_url' in projectData['extra'] else None,
                        'stack_overflow_url': projectData['extra']['stack_overflow_url'] if 'extra' in projectData and 'stack_overflow_url' in projectData['extra'] else None,
                        'blog_url': projectData['extra']['blog_url'] if 'extra' in projectData and 'blog_url' in projectData['extra'] else None,
                        'mailing_list_url': projectData['extra']['mailing_list_url'] if 'extra' in projectData and 'mailing_list_url' in projectData['extra'] else None,
                        'slack_url': projectData['extra']['slack_url'] if 'extra' in projectData and 'slack_url' in projectData['extra'] else None,
                        'gitter_url': projectData['extra']['gitter_url'] if 'extra' in projectData and 'gitter_url' in projectData['extra'] else None,
                        'youtube_url': projectData['extra']['youtube_url'] if 'extra' in projectData and 'youtube_url' in projectData['extra'] else None
                        })

with open(projectsCsvFile, 'w') as projectsCsvFileObject:
    writer = csv.DictWriter(projectsCsvFileObject, fieldnames = csvRows[0].keys())
    writer.writeheader() 
    writer.writerows(csvRows) 