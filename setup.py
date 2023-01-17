from setuptools import setup

setup(
    name="station",
    options={
        'build_apps': {
            'include_patterns': [
                'assets/bam/*.bam',
                'assets/fonts/*.ttf',
                'assets/fonts/*.otf',
                'assets/images/*.png',
                'assets/images/enemies/*.png',
                'libsunvox/*.txt',
                'libsunvox/linux/*/*.so',
                'libsunvox/windows/*/*.dll',
                'libsunvox/windows/*/*.dylib',
                'README.md',
                'keybindings.config',
                'settings.prc',
            ],
            'gui_apps': {
                'station': 'main.py',
            },
            'icons': {
                'station': ['icon.ico'],
            },
            'log_filename': '$USER_APPDATA/stationgame/output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)
