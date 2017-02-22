from collections import defaultdict
import json
from faker import Faker
import requests
from features.test_helpers.configuration_parser import ApiEndpointsParser

PATTERNS = ApiEndpointsParser().get_api_endpoints()


def remove_none_from_dict(d):
    if type(d) is dict:
        return dict((k, remove_none_from_dict(v)) for k, v in zip(d.keys(), d.values())
                    if v is not None and remove_none_from_dict(v) != {})
    elif type(d) is list:
        return [remove_none_from_dict(v) for v in d if v is not None and remove_none_from_dict(v)]
    else:
        return d


def extract_payload(data=None, on_form=False):
    payload = remove_none_from_dict(data) if data else None
    if not on_form:
        payload = json.dumps(payload) if payload else None
    return payload


class Auditor(object):
    def __init__(self):
        self.routes = defaultdict(set)

    def audit(self, verb, url):
        self.routes[verb].add(url)

    def summary(self):
        return self.routes


class Requestor(object):
    def __init__(self, host, auditor):
        self.token = None
        self.admin_token = None
        self.host = host
        self.auditor = auditor
        self._headers = {}

    def headers(self, admin=None, headers=None, on_form=False):
        if not on_form:
            self._headers = {'Content-type': 'application/json'}
        else:
            self._headers = {}

        if not admin:
            token = self.token
        else:
            self.admin_token = 1
            token = self.admin_token

        if token:
            self._headers['Authorization'] = 'Token {}'.format(token)

        if headers:
            self._headers.update(headers)

        return self._headers

    def _get(self, resource, data=None, resource_args=None, admin=None, headers=None):
        if not resource_args:
            resource_args = dict()

        self.auditor.audit('GET', PATTERNS[resource])
        endpoint_url = self._get_endpoint(resource, **resource_args)
        params = data or {}
        params['page'] = resource_args.get('page', None) if resource_args else None
        params = remove_none_from_dict(params)
        response = requests.get(endpoint_url, params=params, headers=self.headers(admin=admin, headers=headers))
        return response

    def _post(self, resource, data=None, resource_args=None, admin=None, headers=None, on_form=False, params=None):
        if not resource_args:
            resource_args = dict()

        self.auditor.audit('POST', PATTERNS[resource])
        endpoint_url = self._get_endpoint(resource, **resource_args)
        payload = extract_payload(data, on_form)
        params = params or {}
        response = requests.post(
            endpoint_url,
            data=payload,
            params=params,
            headers=self.headers(admin=admin, headers=headers, on_form=on_form)
        )
        return response

    def _patch(self, resource, data=None, resource_args=None, admin=None, headers=None, on_form=False):
        if not resource_args:
            resource_args = dict()

        self.auditor.audit('PATCH', PATTERNS[resource])
        endpoint_url = self._get_endpoint(resource, **resource_args)
        payload = extract_payload(data, on_form)
        response = requests.patch(
            endpoint_url,
            data=payload,
            headers=self.headers(admin=admin, headers=headers, on_form=on_form)
        )
        return response

    def _delete(self, resource, resource_args=None, admin=None, headers=None):
        if not resource_args:
            resource_args = dict()

        self.auditor.audit('DELETE', PATTERNS[resource])
        endpoint_url = self._get_endpoint(resource, **resource_args)
        response = requests.delete(endpoint_url, headers=self.headers(admin=admin, headers=headers))
        return response

    def _get_endpoint(self, resource, **kwargs):
        return ''.join([self.host,
                        PATTERNS[resource].replace('users/{user_id}', 'me').format(**kwargs)
                        if 'users/{user_id}' in PATTERNS[resource] and kwargs.get('user_id', None) is None else
                        PATTERNS[resource].format(
                            **kwargs)
                        ])


class Api(Requestor):
    def __init__(self, host, auditor):
        super().__init__(host, auditor)

    def refresh_token(self, **kwargs):
        response = self._post('refresh', admin=kwargs.get('admin', False))
        self.token = response.json().get('token', None)
        return response

    def logout(self, **kwargs):
        response = self._post('logout', admin=kwargs.get('admin', False))
        self.token = None
        return response

    def auth_login_v1(self, **kwargs):
        data = {
            'username': kwargs.get('username'),
            'password': kwargs.get('password')
        }
        response = self._post('login', data)
        self.token = response.json().get('token', None)
        return response

    def auth_login_v2(self, **kwargs):
        data = {
            'username': kwargs.get('username'),
            'password': kwargs.get('password'),
            'client_id': kwargs.get('client_id')
        }
        response = self._post('login_v2', data)
        self.token = response.json().get('token', None)
        return response


_faker = None


def get_faker():
    global _faker
    if not _faker:
        _faker = Faker()
    return _faker


def get_fake_email():
    email = get_faker().email()
    return 'api_acceptance_test+%s@gmail.com' % email.split('@')[0]
