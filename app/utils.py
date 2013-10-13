from flask import flash, request, url_for

def flash_errors(form, category='danger'):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'%s - %s' % (getattr(form, field).label.text,
                error), category)

def url_for_other_page(remove_args=[], **kwargs):
    args = request.args.copy()
    for key, value in remove_args:
        args.pop(key)
    new_args = [x for x in kwargs.iteritems()]
    for key, value in new_args:
        args[key] = value
    return url_for(request.endpoint, **args)
