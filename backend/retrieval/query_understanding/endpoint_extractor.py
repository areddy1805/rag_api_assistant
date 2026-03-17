import re


def extract_endpoints(query):

    endpoints = re.findall(r"/v1/[a-zA-Z0-9_/{}-]+", query)

    return endpoints