from libsaas import http, parsers
from libsaas.services import base

class RepoContents(base.HierarchicalResource):

    path = 'contents'

    @base.apimethod
    def readme(self, ref=None):
        """
        This method returns the preferred README for a repository.
    
        :var ref: The String name of the Commit/Branch/Tag. Defaults to master.
        :vartype path: str
        """
        params = base.get_params(('ref'), locals())
        url = '{0}/readme'.format(self.parent.get_url())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def get(self, path=None, ref=None, page=None, per_page=None):
        """
        This method returns the contents of any file or directory in a 
        repository.
    
        :var path: Optional The content path.
        :vartype path: str
    
        :var ref: The String name of the Commit/Branch/Tag. Defaults to master.
        :vartype path: str
        """
        params = base.get_params(('path', 'ref', 'page', 'per_page'), locals())
        url = '{0}/{1}'.format(self.parent.get_url(), self.path)

        return http.Request('GET', url, params), parsers.parse_json

    def get_archivelink(self, archive_format=None, ref=None):
        """
        This method will return URL to download a tarball or zipball archive
        for a repository. 
    
        :var archive_format: Optional Either tarball or zipball. 
        Defaults to zipball.
        :vartype path: str
    
        :var ref: Optional The String name of the Commit/Branch/Tag. 
        Defaults to master.
        :vartype path: str
        """
        if (not archive_format):
            archive_format = 'zipball'
        if ref:
            url = '{0}/{1}/{2}'.format(self.parent.get_url(), archive_format, ref)
        else:
            url = '{0}/{1}'.format(self.parent.get_url(), archive_format)

        return url
