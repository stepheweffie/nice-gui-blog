from nicegui import app
import os

app_url = 'http://127.0.0.0:8080'


def dev_config():
    app.add_static_files('/assets/highlight-css', 'assets/highlight-css')
    app.add_static_files('/assets/images', 'assets/images')
    app.add_static_files('/ace', 'ace')
    app.add_static_files('/ace/src-min', 'ace/src-min')
    app.add_static_files('/assets/js', 'assets/js')
    app.add_static_files('/assets/css', 'assets/css')
    app.add_static_files('/assets/html', 'assets/html')
    js_templates = os.listdir('ace/src-min')
    ace = js_templates.index('ace.js')
    js_templates.pop(ace)
    js_templates.insert(0, 'ace.js')
    ace = os.path.join('/ace/src-min', js_templates[0])