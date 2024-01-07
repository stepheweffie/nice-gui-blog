

html = '''
<p>
let \(\Delta = \sqrt{b^2-4ac}\), we can write
$$
 x = {-b \pm \sqrt {\Delta} \over 2a}
$$
We have a conclusion on it
</p>

'''

strTab = r'''| $$\Delta$$ | <0              | =0                 | >0                     |
| ------------------ | --------------- | ------------------ | ---------------------- |
|                    | 2 complex roots | 2 equal real roots | 2 different real roots |
'''

strCode = '''
<code class="language-python">
from nicegui import ui
<br><br>
    ui.label('Hello World!')
<br><br>
    ui.run(dark=True)
<code>
'''
