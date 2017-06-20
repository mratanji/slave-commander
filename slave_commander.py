'''
Module used to execute commands on all connected lsaves with provided label.
Does so by -
1. Generate list of nodes using Jenkins rest API
2. Get labels to node using nodes config.xml
3. Using rest API to execute /script (Groovy script) on node.

The Groovy script is predefined to execute system commands, not Groovy code.
i.e., command should be like 'mkdir /tmp/hello' or 'C:/test/test.exe arg1 arg2'

INPUT:

slave-command.py [TARGET_LABEL] [COMMAND]
'''
import os
import sys
import json
import re
import xml.etree.ElementTree
from threading import Thread
import requests


JENKINS_BASE_URL = os.environ.get('JENKINS_URL', 'DEFAULT_VALUE')
USERNAME = os.environ.get('jenkins_api_user', 'DEFAULT_VALUE')
API_TOKEN = os.environ.get('jenkins_api_token', 'DEFAULT_VALUE')
AUTH = (USERNAME, API_TOKEN)


def get_labels_for_node(jenkins_url, node_name):
    '''labels for node_name'''
    url = '{0}/computer/{1}/config.xml'.format(jenkins_url, node_name)
    response = requests.get(url=url)
    xml_object = xml.etree.ElementTree.fromstring(response.content)
    labels = xml_object.findtext('label')
    labels = labels.split(' ')
    labels.append('all')
    return labels


def get_nodes(jenkins_url):
    '''Nodes attached to jenkins at jenkins_url'''
    url = '{0}/computer/api/json'.format(jenkins_url)
    response = requests.get(url=url)
    nodes = []

    for node in json.loads(response.content)['computer']:
        if not node['offline']:
            nodes.append(node['displayName'])
    nodes.remove('master')
    return nodes


def get_nodes_with_label(jenkins_url, target_label):
    '''Dictionarary of nodes with label that matched target_label'''
    all_nodes = get_nodes(jenkins_url)
    node_label_mapping = {}
    for node in all_nodes:
        labels = get_labels_for_node(jenkins_url, node)
        if target_label in labels:
            node_label_mapping[node] = labels
    return node_label_mapping


def execute_command(jenkins_url, node_name, command, auth):
    '''Run command on node_name which is attached to jenkins_url using auth
     and return output'''
    command = '\"' + command + '\".execute().in.text'
    url = '{0}/computer/{1}/script'.format(jenkins_url, node_name)
    data = [('script', command)]
    response = requests.post(url=url, data=data, auth=auth)
    regex = re.compile('Result:.*pre>', re.DOTALL)
    result = regex.findall(response.content)
    final_print_string = ''
    final_print_string += ('-' * 80 + '\n')
    final_print_string += 'Result for {}:\n'.format(node_name)
    for res in result:
        final_print_string += str(res).replace('</pre>', '').replace('Result:', '')
    print final_print_string


def validate_arguments():
    '''Check if all arguments are provided'''
    if len(sys.argv) < 2:
        print 'More arguments expected - [TARGET_LABEL] [COMMAND]'
        exit(1)
    return sys.argv[1], sys.argv[2]


def execute_command_on_nodes(jenkins_url, target_nodes, command, auth):
    '''As method name describes'''
    # Serial, if you're into that kind of stuff
    # for node in target_nodes:
    #     execute_command(jenkins_url, node, command, auth)

    # Multithreaded, much better!
    threads = []
    for node in target_nodes:
        sub_thread = Thread(target=execute_command, args=(
            jenkins_url, node, command, auth))
        threads.append(sub_thread)
        print 'Scheduling {0} to run {1}'.format(node, command)
    for sub_thread in threads:
        sub_thread.start()
    for sub_thread in threads:
        sub_thread.join()


def process():
    '''Main logic'''
    target_label, command = validate_arguments()
    target_nodes = get_nodes_with_label(JENKINS_BASE_URL, target_label)
    execute_command_on_nodes(JENKINS_BASE_URL, target_nodes, command, AUTH)


process()
