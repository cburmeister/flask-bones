from flask import flash


def flash_errors(form, category='danger'):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'%s - %s' % (getattr(form, field).label.text,
                error), category)
