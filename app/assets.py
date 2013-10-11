from flask.ext.assets import Bundle, Environment

js = Bundle(
    'js/jquery.js',
    'js/bootstrap.min.js',
    filters='jsmin',
    output='gen/packed.js'
)

css = Bundle(
    'css/bootstrap.min.css',
    'css/style.css'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
