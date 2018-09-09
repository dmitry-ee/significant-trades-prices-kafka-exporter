import docker
import re

class DockerService(object):

    docker_client = None
    def __init__(self):
        self.docker_client = docker.from_env()

    def list(self, regex=r".*", status="running"):
        filters = { "status": status }
        found_containers = self.docker_client.containers.list(filters=filters)
        return [ c for c in found_containers if re.match(regex, c.name + c.id + c.attrs["Config"]["Image"]) ]
        #return [ c for c in self.docker_client.containers.list(filters=filters) if c.status == status ]
