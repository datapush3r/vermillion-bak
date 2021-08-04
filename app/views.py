# -*- encoding: utf-8 -*-
# from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from docker import from_env as docker_client
from docker.errors import DockerException
import json

def index(request):
    
    context = {}
    context['segment'] = 'index'

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

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template

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

        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
