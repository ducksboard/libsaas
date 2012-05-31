import libsaas
from libsaas.executors import requests_executor
from libsaas.services import github

# use the Requests executor with a custom timeout and make it always send a
# user agent string
uastring = 'libsaas {0}'.format(libsaas.__versionstr__)

requests_executor.use(timeout=5.0,
                      config={'base_headers': {'User-agent': uastring}})

# unstar all starred gists
gh = github.GitHub('my-github-token')

for gist in gh.gists().starred():
    gh.gist(gist['id']).unstar()
