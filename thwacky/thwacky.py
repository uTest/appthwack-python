"""
    thwacky
    ~~~~~~~

    thwacky is a python client for the AppThwack REST API.
"""
__name__ = 'thwacky'
__version__ = '0.0.1'
__author__ = 'Andrew Hawker <andrew@appthwack.com>'

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import functools
import os
import requests
import urllib

DOMAIN = 'https://appthwack.com'

def urlify(*resources, **params):
    """
    Build a URL to a REST endpoint.

    :param resources: Tuple of resources which describe the endpoint.
    :param params: Mapping which builds url query string.
    """
    url = '/'.join((DOMAIN,) + filter(None, resources))
    qstring = urllib.urlencode(params)
    return '?'.join(filter(None, (url, qstring)))


def keyword_filter(keys, **kwargs):
    """
    Find first instance of a key in kwargs and return the matching key/value pair.

    :param keys: Iterable containing keys we which is search kwargs for.
    :param kwargs: Mapping which contains key/value pairs we're filtering down.
    """
    return next(((k, str(v)) for (k,v) in ((k, kwargs.get(k)) for k in keys) if v), (None, None))


class AppThwackApiError(Exception):
    """
    Exception to describe an error when communicating with the AppThwack API.
    """
    pass


def expects(expected_status_code, expected_content_type):
    """
    Decorator which wraps a REST call and validates the response.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            #Perform request and capture response.
            response = func(*args, **kwargs)
            status_code = response.status_code
            content_type = response.headers.get('content-type')
            #Unexpected response status code is considered an 'exceptional' case.
            if status_code != expected_status_code:
                msg = 'Got status code {0}; expected {1} with response {2}.'.format(status_code,
                                                                                    expected_status_code,
                                                                                    response.json())
                raise AppThwackApiError(msg)
            #Unexpected response content-type is considered an 'exceptional' case.
            if bool(content_type) != bool(expected_content_type) or \
                    (content_type and expected_content_type.lower() not in content_type.lower()):
                msg = 'Got content-type {0}; expected {1} with response {2}.'.format(content_type,
                                                                                     expected_content_type,
                                                                                     response.text)
                raise AppThwackApiError(msg)
            return response
        return wrapper
    return decorator


class RequestsMixin(object):
    """
    Mixin for adding basic REST client functionality.
    """

    API_KEY = None
    SESSION_DEFAULTS = {
        'verify': False,
    }

    @expects(200, 'application/json')
    def get(self, *resources, **kwargs):
        """
        Perform HTTP GET which expects status_code: 200 and content-type: application/json.

        :param resources: List of resources which build the URL we wish to use.
        :param kwargs: Mapping of options to use for this specific HTTP request.
        """
        return requests.get(urlify('api', *resources), **self._session_config(**kwargs))

    @expects(200, 'application/json')
    def post(self, *resources, **kwargs):
        """
        Perform HTTP POST which expects status_code: 200 and content-type: application/json.

        :param resources: List of resources which build the URL we wish to use.
        :param kwargs: Mapping of options to use for this specific HTTP request.
        """
        return requests.post(urlify('api', *resources), **self._session_config(**kwargs))

    def _session_config(self, **kwargs):
        """
        Merge default, request specific and auth options to use in a HTTP request.
        """
        return dict(self.SESSION_DEFAULTS, auth=(self.API_KEY, None), **kwargs)


class AppThwackApi(RequestsMixin):
    """
    Client object which exposes access to top level endpoints (/api).
    """
    def __init__(self, api_key=None):
        """
        :param api_key: AppThwack account API key, default is 'APPTHWACK_API_KEY' environment variable.
        """
        key = api_key or os.environ.get('APPTHWACK_API_KEY')
        if not key:
            raise ValueError('AppThwack API key must be provided.')
        RequestsMixin.API_KEY = key #TODO (reconsider this) -- especially if/when stdlib support added

    def project(self, **kwargs):
        """
        Return a single `AppThwackProject` based on the kwarg filter. If no filter is given, the first
        project is returned.

        :param kwargs: 'id' or 'name' value to retrieve a specific project.
        """
        k, v = keyword_filter(('id', 'name'), **kwargs)
        return next(filter(lambda p: getattr(p, str(k)) == v, self.projects()))

    def projects(self):
        """
        Return a list of all `AppThwackProject` tied to this account.

        .. endpoint:: [GET] /api/project
        """
        data = self.get('project').json()
        return [AppThwackProject(**p) for p in data]

    def upload(self, path, name=None):
        """
        Upload a app (.apk or .ipa) to AppThwack.

        :param path: Local filepath to app you wish to upload.
        :param name: Name of app visible on AppThwack, default is local filename.

        .. endpoint:: [POST] /api/file
        """
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        root, ext = os.path.splitext(path)
        if not ext:
            raise ValueError('Path must contain a file extension.')
        if not name:
            name = os.path.basename(root) + ext
        with open(path, 'r') as fileobj:
            data = self.post('file', data={'name': name}, files={name: fileobj}).json()
            return AppThwackFile(**data)


class AppThwackObject(object):
    """
    Generic object built from JSON data returned from AppThwack.
    """

    #List of expected attributes (keys) for a JSON response of specified type.
    attributes = []

    def __init__(self, **kwargs):
        """
        Create a dynamic object which expands to contain specified attributes
        of a JSON response.

        :param kwargs: Decoded JSON mapping.
        """
        if not kwargs or not all(k in kwargs for k in self.attributes):
            raise ValueError('Invalid decoded JSON.')
        self.__dict__.update(kwargs)


class AppThwackProject(AppThwackObject, RequestsMixin):
    """
    Represents an AppThwack project as returned by `AppThwackApi`.
    """
    attributes = 'id name url'.split()
    optional_args = []

    def __init__(self, **kwargs):
        super(AppThwackProject, self).__init__(**kwargs)
        self.url = urlify('project', self.url)

    def pool(self, **kwargs):
        """
        Return a single `AppThwackDevicePool` based on the kwarg filter. If no filter is given,
        the first devicepool is returned.

        :param kwargs: 'id' or 'name' value to retrieve a specific devicepool.
        """
        k, v = keyword_filter(('id', 'name'), **kwargs)
        return next(filter(lambda p: getattr(p, str(k)) == v, self.pools()))

    def pools(self):
        """
        Return a list of all `AppThwackDevicePool` tied to this account.

        .. endpoint:: [GET] /api/devicepool/<int:project_id>
        """
        data = self.get('devicepools', self.id).json()
        return [AppThwackDevicePool(**p) for p in data]

    def run(self, name, app, **kwargs):
        """
        Schedule a run on AppThwack.

        :param name: Name of run to be used on AppThwack.
        :param app: `AppThwackFile` which represents the upload app (.apk or .ipa).
        :param kwargs: Mapping of optional args which describe execution options.

        .. endpoint:: [POST] /api/run
        """
        req = dict(project=self.id, name=name, app=app)
        opt = dict((k,v) for (k,v) in ((k, kwargs.get(k)) for k in self.optional_args) if v)
        data = self.post('run', data=dict(req, **opt)).json()
        return AppThwackRun(self.id, **data)


class AppThwackAndroidProject(AppThwackProject):
    optional_args = 'pool username password launchdata eventcount monkeyseed calabash junit'.split()

    def __init__(self, **kwargs):
        super(AppThwackAndroidProject, self).__init__(**kwargs)


class AppThwackIOSProject(AppThwackProject):
    optional_args = 'pool uia calabash kif'.split()

    def __init__(self, **kwargs):
        super(AppThwackIOSProject, self).__init__(**kwargs)


class AppThwackWebProject(AppThwackProject):
    def __init__(self, **kwargs):
        super(AppThwackWebProject, self).__init__(**kwargs)



class AppThwackRun(AppThwackObject, RequestsMixin):
    """
    Represents a scheduled run returned by `AppThwackProject`.
    """
    attributes = 'run_id'.split()

    def __init__(self, project_id, **kwargs):
        super(AppThwackRun, self).__init__(**kwargs)
        self.url = urlify('run', project_id, self.run_id)
        self.download_url = urlify(self.url, format='archive')

    def status(self):
        """
        Return the execution status for this specific run.

        .. endpoint:: [GET] /api/run/<int:project_id>/<int:run_id>/status
        """
        data = self.get(self.url, 'status').json()
        return data['status'] #TODO confirm structure

    def results(self):
        """
        Return the `AppThwackResult` for this specific run.

        .. endpoint:: [GET] /api/run/<int:project_id>/<int:run_id>
        """
        data = self.get(self.url).json()
        return AppThwackResult(self, **data)

    def download(self):
        """
        Return the raw results archive for this specific run.

        .. endpoint:: [GET] /api/run/<int:project_id>/<int:run_id>?format=archive
        """
        filename = 'tmp.zip'
        response = self.get(self.download_url)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(4096):
                f.write(chunk)


class AppThwackResult(AppThwackObject, RequestsMixin):
    """
    Represents the results of a scheduled run returned by `AppThwackRun`.
    """

    #TODO capture everything, not just the summary
    attributes = 'summary'.split()


class AppThwackFile(AppThwackObject):
    """
    Represents a app upload returned by `AppThwackApi`.
    """
    attributes = 'file_id'.split()

    def __init__(self, **kwargs):
        super(AppThwackFile, self).__init__(**kwargs)
        self.url = urlify('file', self.file_id)


class AppThwackDevicePool(AppThwackObject):
    """
    Represents a pool of devices returned by `AppThwackProject`.
    """
    attributes = 'id name'.split()

    def __init__(self, **kwargs):
        super(AppThwackDevicePool, self).__init__(**kwargs)
        self.url = urlify('devicepool', self.id)
