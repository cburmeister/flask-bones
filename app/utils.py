from flask import request, url_for


def url_for_other_page(remove_args=[], **kwargs):
    args = request.args.copy()
    remove_args = ['_pjax']
    for key in remove_args:
        if key in args.keys():
            args.pop(key)
    new_args = [x for x in kwargs.items()]
    for key, value in new_args:
        args[key] = value
    return url_for(request.endpoint, **args)
