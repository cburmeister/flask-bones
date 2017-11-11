from flask import request, url_for


def url_for_other_page(**kwargs):
    """Returns a URL aimed at the current request endpoint and query args."""
    url_for_args = request.args.copy()
    if 'pjax' in url_for_args:
        url_for_args.pop('_pjax')
    for key, value in kwargs.items():
        url_for_args[key] = value
    return url_for(request.endpoint, **url_for_args)
