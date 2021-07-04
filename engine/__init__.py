# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 10. 21..
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from pygics import rest, download, File, HttpResponseType
import base64
import string
import random
import requests
from config import vra_fqdn

#===============================================================================
# Preparing
#===============================================================================
session = requests.Session()
random_choice = string.ascii_lowercase + string.ascii_uppercase + string.digits

vidm_client_auth = 'Basic ' + base64.b64encode('{}:{}'.format(vidm_client_id, vidm_client_token).encode('utf-8')).decode('utf-8')
vidm_auth_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': vidm_client_auth
}

vrux_url = 'https://{}'.format(vrux_fqdn)
vrux_auth_url = vrux_url + '/auth'

res = session.post(
    'https://{}/csp/gateway/am/api/login?access_token'.format(vra_fqdn),
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    json={
        'username': vra_admin_username,
        'password': vra_admin_password
    }, verify=False)
res = session.post(
    'https://{}/iaas/api/login'.format(vra_fqdn),
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    json={
        'refreshToken': res.json()['refresh_token']
    }
)
vra_auth_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + res.json()['token']
}

#===============================================================================
# Auth Interfaces
#===============================================================================
@rest('GET', '/auth')
def get_auth(req, **params):
    res = session.post(
        'https://{}/SAAS/auth/oauthtoken'.format(vidm_fqdn),
        headers=vidm_auth_headers,
        data='grant_type=authorization_code&code={}&redirect_uri={}'.format(params['code'], vrux_auth_url),
        verify=False)
    res.raise_for_status()
    raise HttpResponseType.Redirect(vrux_url, [('Set-Cookie', 'refreshToken={}'.format(res.json()['refresh_token']))])

@rest('GET', '/auth/request')
def get_auth_request(req):
    url = 'https://{}/SAAS/auth/oauth2/authorize?response_type=code&client_id={}&scope=openid+user+email+profile&state={}&redirect_uri={}'.format(
        vidm_fqdn,
        vidm_client_id,
        ''.join(random.choices(random_choice, k=30)),
        vrux_auth_url
        )
    raise HttpResponseType.Redirect(url)

@rest('POST', '/auth/token')
def post_auth_token(req):
    res = session.post(
        'https://{}/csp/gateway/am/api/login/oauth'.format(vra_fqdn),
        headers=vidm_auth_headers,
        data='grant_type=refresh_token&refresh_token={}&state={}'.format(req.data['refreshToken'], ''.join(random.choices(random_choice, k=30))),
        verify=False)
    res.raise_for_status()
    return {
        "token": res.json()['access_token']
    }

#===============================================================================
# vRA Proxy
#===============================================================================
icon_index = {}
@download('/vra/icon/api/icons/')
def get_vra_icon(req, id):
    if id in icon_index: return File(icon_index[id])
    res = session.get(
        'https://{}/icon/api/icons/{}'.format(vra_fqdn, id),
        headers=vra_auth_headers,
        verify=False)
    res.raise_for_status()
    ext = res.headers['Content-Type'].split('/')[1]
    name = "cache/{}.{}".format(id, ext)
    with open(name, 'wb') as fd: fd.write(res.content)
    icon_index[id] = name
    return File(name)

@rest('GET', '/vra/')
def get_vra_api(req, *path):
    res = session.get(
        'https://{}/{}'.format(vra_fqdn, '/'.join(path)),
        headers={
            'Accept': 'application/json',
            'Authorization': req.headers['AUTHORIZATION']
        }, verify=False)
    res.raise_for_status()
    return res.json()

@rest('POST', '/vra/')
def post_vra_api(req, *path):
    res = session.post(
        'https://{}/{}'.format(vra_fqdn, '/'.join(path)),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': req.headers['AUTHORIZATION']
        },
        json=req.data,
        verify=False)
    res.raise_for_status()
    return res.json()

@rest('PUT', '/vra/')
def put_vra_api(req, *path):
    res = session.put(
        'https://{}/{}'.format(vra_fqdn, '/'.join(path)),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': req.headers['AUTHORIZATION']
        },
        json=req.data,
        verify=False)
    res.raise_for_status()
    return res.json()

@rest('PATCH', '/vra/')
def patch_vra_api(req, *path):
    res = session.patch(
        'https://{}/{}'.format(vra_fqdn, '/'.join(path)),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': req.headers['AUTHORIZATION']
        },
        json=req.data,
        verify=False)
    res.raise_for_status()
    return res.json()

@rest('DELETE', '/vra/')
def delete_vra_api(req, *path):
    res = session.delete(
        'https://{}/{}'.format(vra_fqdn, '/'.join(path)),
        headers={
            'Accept': 'application/json',
            'Authorization': req.headers['AUTHORIZATION']
        }, verify=False)
    res.raise_for_status()
    return res.json()
