from flask import flash


def flash_errors(form, category='danger'):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'%s' % (error), category)
