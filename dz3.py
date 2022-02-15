class Url:

    def __init__(self, scheme, path=None, authority=None, query=None, fragment=None):
        self.scheme = scheme
        self.authority = authority
        if path is None:
            path = []
        self.path = path
        if query is None:
            query = {}
        self.query = query
        if fragment is None:
            fragment = ''
        self.fragment = fragment

    def __eq__(self, other):
        return str(self) == other

    def __str__(self):
        scheme = self.scheme + ':' if self.scheme else ''
        authority = '//' + self.authority if self.authority else ''
        if type(self.query) == dict and self.query:
            query = '?'
            counter = 0
            for key, value in self.query.items():
                counter += 1
                if counter >= 2:
                    query += '&'
                query += f'{key}={value}'
        else:
            query = '?' + str(self.query) if self.query else ''
        fragment = "#" + self.fragment if self.fragment else ''
        path = self.path if self.path else ''
        if type(path) == list and path:
            path = '/' + '/'.join(path)
        return f'{scheme}{authority}{path}{query}{fragment}'


class HttpsUrl(Url):

    def __init__(self, path=None, authority=None, query=None, fragment=None):
        super().__init__('https', path=path, authority=authority, query=query, fragment=fragment)


class HttpUrl(Url):

    def __init__(self, path=None, authority=None, query=None, fragment=None):
        super().__init__('http', path=path, authority=authority, query=query, fragment=fragment)


class GoogleUrl(HttpsUrl):

    def __init__(self, path=None,  query=None, fragment=None):
        super().__init__(path=path, authority='google.com', query=query, fragment=fragment)


class WikiUrl(HttpsUrl):

    def __init__(self, path=None,  query=None, fragment=None):
        super().__init__(path=path, authority='wikipedia.org', query=query, fragment=fragment)


class UrlCreator():

    def __init__(self, *args, **kwargs):
        self._url = Url(*args, **kwargs)

    def __getattr__(self, item):
        if hasattr(self._url, item):
            return getattr(self._url, item)
        return UrlCreator(scheme=self._url.scheme,
                          authority=self._url.authority,
                          path=self._url.path + [item],
                          query=self._url.query,
                          fragment=self._url.fragment)

    def __call__(self, *args, **kwargs):
        return UrlCreator(scheme=self._url.scheme,
                          authority=self._url.authority,
                          path=self._url.path + list(args),
                          query={**self._url.query, **kwargs},
                          fragment=self._url.fragment)

    def __str__(self):
        return str(self._url)
