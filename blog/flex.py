from nicegui import ui


@ui.page('/')
def main():
    ui.add_head_html('''
     <style>
        :root {
            --nicegui-default-padding: 0rem;
            --nicegui-default-gap: 0rem;
        }
     </style>
    ''')

    quote_classes = 'm-3 p-6 bg-blue-100 rounded-lg'
    quote_p_classes = 'font-serif italic text-lg text-gray-700 leading-snug mb-1'
    quote_span_classes = 'text-sm text-gray-500'

    with (ui.element('div').classes('flex flex-row no-wrap')):
        with ui.element('div').classes(quote_classes):
            ui.label("The success combination in business is: Do what you do better... and: do more of what you do."
                     ).classes(quote_p_classes)
            ui.label("- David Joseph Schwartz").classes(quote_span_classes)

        with ui.element('div').classes(quote_classes):
            ui.label("Give out what you most want to come back.").classes(quote_p_classes)
            ui.label("- Robin Sharma").classes(quote_span_classes)

        with ui.element('div').classes(quote_classes):
            ui.label("The only way around is through.").classes(quote_p_classes)
            ui.label("- Robert Frost").classes(quote_span_classes)


ui.run(title='test example', storage_secret='123', dark=False)