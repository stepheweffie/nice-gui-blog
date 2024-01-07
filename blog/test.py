from nicegui import app, ui

UPLOAD_DIR = 'uploads'
app.add_static_files('/uploads', UPLOAD_DIR)
# Title
title = 'Cosine Similarity'
title_style = 'color: #000000; font-size: 2rem;'
title_text = ui.html(f'{title}').style(f'{title_style}')
# Image Upload
image_path = '/uploads/cosine_similarity_histograph.png'
image_classes = 'mt-4 mb-6'
image_style = 'width: 50%; border: 1px solid #ccc;'
uploaded_image = ui.image(f'{image_path}')\
    .classes(f'{image_classes}')\
    .style(f'{image_style}')
image_text = 'Upload an image to see the cosine similarity between the image and the image you upload.'
image_text_classes = 'text-subtitle2 text-center absolute-bottom'
with uploaded_image:
    ui.label(f'{image_text}').classes(f'{image_text_classes}')

editor = ui.editor().style('width: 100%; height: 300px; border: 1px solid #ccc; padding: 10px;')
editor.bind_value_from(uploaded_image, 'src', backward=lambda v: v)
# Editor Visibility
editor_visible = ui.switch('Show editor').on('change', lambda: editor.visible(editor_visible.value))
editor_visible.value = True
editor.bind_visibility_from(editor_visible, 'value', backward=lambda v: v)
# Bind the editor's content to the HTML preview
preview = ui.html()
preview_style = 'width: 100%; height: 200px; border: 1px solid #ccc; padding: 10px;'
preview.bind_content_from(editor, 'value', backward=lambda v: v).style(f'{preview_style}')
ui.run()
