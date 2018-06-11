import os
import sys
from .paths import PROJECT_ROOT, PARENT_DIR

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PARENT_DIR, 'collected_static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'web'),
)

if 'test' not in sys.argv:
    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'pipeline.finders.PipelineFinder',
    # 'pipeline.finders.CachedFileFinder',
)

import speeches
PIPELINE = {
    # Compress the css and js using yui-compressor.
    'CSS_COMPRESSOR': 'pipeline.compressors.yui.YUICompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.yui.YUICompressor',
    'COMPILERS': (
        'pipeline_compass.compass.CompassCompiler',
    ),
    # On some platforms this might be called "yuicompressor", so it may be
    # necessary to symlink it into your PATH as "yui-compressor".
    'YUI_BINARY': '/usr/bin/env yui-compressor',
    'COMPASS_BINARY': os.path.join(PROJECT_ROOT, 'vendor', 'bundle', 'bin', 'compass'),
    'COMPASS_ARGUMENTS': [ '-I', os.path.join(speeches.__path__[0], 'static'), '-r', 'zurb-foundation' ],

  'STYLESHEETS': {
    'sayit-default': {
        'source_filenames': (
            'sass/project.scss',
        ),
        'output_filename': 'css/project.css',
    },
    'sayit-shakespeare': {
        'source_filenames': (
            'sass/project-shakespeare.scss',
        ),
        'output_filename': 'css/project-shakespeare.css',
    },
    'sayit-labour': {
        'source_filenames': (
            'sass/project-labour.scss',
        ),
        'output_filename': 'css/project-labour.css',
    },
    'sayit-conservative': {
        'source_filenames': (
            'sass/project-conservative.scss',
        ),
        'output_filename': 'css/project-conservative.css',
    },
  },
  'JAVASCRIPT': {
    # Some things in document body (e.g. media player set up) call $()
    'sayit-default-head': {
        'source_filenames': (
            'speeches/js/jquery.js',
            'speeches/js/select2-override.js',
        ),
        'output_filename': 'js/sayit.head.min.js',
    },
    # The JS at the end of each page, before </body>
    'sayit-default': {
        'source_filenames': (
            'speeches/js/foundation/foundation.js',
            'speeches/js/foundation/foundation.dropdown.js',
            'javascripts/foundation/foundation.alerts.js',
            'javascripts/fragmentions.js',
            'speeches/js/speeches.js',
            # 'javascripts/vendor/jquery.text-effects.js',
        ),
        'output_filename': 'js/sayit.min.js',
    },
    # The media player
    'sayit-player': {
        'source_filenames': (
            'speeches/mediaelement/mediaelement-and-player.js',
        ),
        'output_filename': 'javascripts/sayit.mediaplayer.min.js',
    },
    'sayit-admin': {
        'source_filenames': (
            'speeches/js/jquery.js',
            'speeches/mediaelement/mediaelement-and-player.js',
            # "soundmanager2/script/soundmanager2.js"
        ),
        'output_filename': 'javascripts/sayit.admin.min.js',
    },
    'sayit-upload': {
        'source_filenames': (
            'speeches/js/jQuery-File-Upload/js/vendor/jquery.ui.widget.js',
            'speeches/js/jQuery-File-Upload/js/jquery.iframe-transport.js',
            'speeches/js/jQuery-File-Upload/js/jquery.fileupload.js',
            # "js/bootstrap-datepicker.js"
        ),
        'output_filename': 'javascripts/sayit.upload.min.js',
    },
  },
}
