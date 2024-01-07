from nicegui import ui, Client

# HTML content
vue_html_content = """
<div class="container">
<div id="q-app"">
    <q-editor
     style="object-fit: None; flex-grow: 1; "
      v-model="qeditor"
      :toolbar="[
        [
          {
            label: $q.lang.editor.align,
            icon: $q.iconSet.editor.align,
            fixedLabel: true,
            options: ['left', 'center', 'right', 'justify']
          }
        ],
        ['bold', 'italic', 'strike', 'underline', 'subscript', 'superscript'],
        ['token', 'hr', 'link', 'custom_btn'],
        ['print', 'fullscreen'],
        [
          {
            label: $q.lang.editor.formatting,
            icon: $q.iconSet.editor.formatting,
            list: 'no-icons',
            options: [
              'p',
              'h1',
              'h2',
              'h3',
              'h4',
              'h5',
              'h6',
              'code'
            ]
          },
          {
            label: $q.lang.editor.fontSize,
            icon: $q.iconSet.editor.fontSize,
            fixedLabel: true,
            fixedIcon: true,
            list: 'no-icons',
            options: [
              'size-1',
              'size-2',
              'size-3',
              'size-4',
              'size-5',
              'size-6',
              'size-7'
            ]
          },
          {
            label: $q.lang.editor.defaultFont,
            icon: $q.iconSet.editor.font,
            fixedIcon: true,
            list: 'no-icons',
            options: [
              'default_font',
              'arial',
              'arial_black',
              'comic_sans',
              'courier_new',
              'impact',
              'lucida_grande',
              'times_new_roman',
              'verdana'
            ]
          },
          'removeFormat'
        ],
        ['quote', 'unordered', 'ordered', 'outdent', 'indent'],

        ['undo', 'redo'],
        ['viewsource']
      ]"
      :fonts="{
        arial: 'Arial',
        arial_black: 'Arial Black',
        comic_sans: 'Comic Sans MS',
        courier_new: 'Courier New',
        impact: 'Impact',
        lucida_grande: 'Lucida Grande',
        times_new_roman: 'Times New Roman',
        verdana: 'Verdana'
      }"
    ></q-editor>
    
    <q-expansion-item label="Markdown Content" icon="description">
  <q-card flat>
    <q-card-section>
      <pre style="white-space: pre-line">{{ qeditor }}</pre>
    </q-card-section>
  </q-card>
</q-expansion-item>

</div>
</div>

"""

# JavaScript for Vue and Quasar
vue_js_script = """
const { ref } = Vue

const app = Vue.createApp({
  setup () {
    const qeditor = ref('<pre>********* View Markdown for your text below. ***********' +
                        '</pre> ')

    // Expose the editor content globally
    window.getEditorContent = () => {
      return qeditor.value;  // Assuming qeditor holds the editor content
    };

    return { qeditor }
  }
})
app.use(Quasar, { config: {} })
app.mount('#q-app')
"""


async def fetch_editor_content():
    js_script = """
    const editorContent = window.getEditorContent();
    """
    js = ui.run_javascript(js_script)
    return js


def fetch_editor_markdown():
    html_script = """
    <pre style="white-space: pre-line">{{ qeditor }}</pre>
    """
    html = ui.html(html_script)
    return html


body_html = '''
<body>
When \(a \ne 0\), there are two solutions to \(ax^2 + bx + c = 0\) and they are
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$
</body>
'''