from libsaas import http, parsers
from libsaas.services import base


def parse_redirect(body, code, headers):
    if code != 302:
        raise http.HTTPError(body, code, headers)

    return headers.get('location')


class RepoContents(base.HierarchicalResource):

    path = 'contents'

    @base.apimethod
    def readme(self, ref=None):
        """
        This method returns the preferred README for a repository.

        :var ref: Optional string name of the commit/branch/tag. Defaults to
            master.
        :vartype ref: str
        """
        params = base.get_params(None, locals())
        url = '{0}/readme'.format(self.parent.get_url())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def get(self, path=None, ref=None):
        """
        This method returns the contents of any file or directory in a
        repository.

        :var path: Optional content path.
        :vartype path: str

        :var ref: Optional string name of the commit/branch/tag. Defaults to
            master.
        :vartype ref: str
        """
        params = base.get_params(('ref', ), locals())
        url = self.get_url()

        if path:
            url = '{0}/{1}'.format(url, path)

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def archivelink(self, archive_format, ref=None):
        """
        This method will return a URL to download a tarball or zipball archive
        for a repository.

        :var archive_format: Either tarball or zipball.
        :vartype path: str

        :var ref: Optional string name of the commit/branch/tag. Defaults to
            master.
        :vartype path: str
        """
        url = '{0}/{1}'.format(self.parent.get_url(), archive_format)
        if ref:
            url = '{0}/{1}'.format(url, ref)

        return http.Request('GET', url), parse_redirect
