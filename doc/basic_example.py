from __future__ import print_function

from libsaas.services import github

# use basic authentication to create a token for libsaas
basic = github.GitHub('me@example.org', 'my-github-password')

auth = basic.authorizations().create({'scopes': 'repo,gist',
                                      'note': 'libsaas example'})

# use token authentication for the rest of the calls
gh = github.GitHub(auth['token'])

# go through your followers
for follower in gh.user().followers():
    username = follower['login']

    # get the source repositories owned by each follower
    repos = gh.user(username).repos().get(type='owner')
    sources = [repo for repo in repos if not repo['fork']]

    # handle the case where a user has no repos
    if not sources:
        print("{0} has no repositories".format(username))
        continue

    # print the most watched repo of each follower, excluding forks
    most = sorted(sources, key=lambda repo: repo['watchers'])[-1]
    print("{0}'s most watched repository: {1}".format(username, most['name']))
