from flask.ext.assets import Bundle, Environment

js = Bundle(
    'bower_components/jquery/dist/jquery.js',
    'bower_components/jquery-pjax/jquery.pjax.js',
    'bower_components/bootbox/bootbox.js',
    'bower_components/bootstrap/dist/js/bootstrap.min.js',
    'js/application.js',
    filters='jsmin',
    output='gen/packed.js'
)

css = Bundle(
    'bower_components/bootstrap/dist/css/bootstrap.css',
    'css/style.css',
    filters='cssmin',
    output='gen/packed.css'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
