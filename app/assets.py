from flask.ext.assets import Bundle, Environment

js = Bundle(
    'js/jquery-2.0.3.min.js',
    'js/jquery.pjax.js',
    'js/bootstrap.min.js',
    'js/bootbox.min.js',
    'js/application.js',
    filters='jsmin',
    output='gen/packed.js'
)

css = Bundle(
    'css/bootstrap.min.css',
    'css/style.css',
    filters='cssmin',
    output='gen/packed.css'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
