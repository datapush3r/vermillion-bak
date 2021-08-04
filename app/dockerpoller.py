# -*- encoding: utf-8 -*-
from docker import from_env as docker_client
from docker.errors import DockerException

def polldocker(context):
    container_data = []
    try:
        client = docker_client()
    except DockerException as e:
        context = {
            'error': str(e)
        }
        return context

    
    for container in client.containers.list():
        data = {
            'name': container.name,
            'id': container.short_id,
            'status': container.status,
            'ports': container.ports
        }
        container_data.append(data)
        context = {
            'container_data': container_data,
        }
        return context