from flask.ext.assets import Bundle, Environment

js = Bundle(
    'js/jquery.js',
    'js/jquery.pjax.js',
    'js/bootstrap.min.js',
    'js/pagination.js',
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
