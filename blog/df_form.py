from nicegui import ui
import pandas as pd
from security_layer import pass_security_layer
df = pd.DataFrame()


def request_my_dict(data: dict):
    global df
    df_new = pd.DataFrame([data])
    ui.open('/data')
    if len(df) == 0:
        df = df_new
    else:
        df = pd.concat([df, df_new], ignore_index=True)
    print(df)
    return df


@ui.page('/data')
def data_page():
    global df
    with ui.row():
        pass_security_layer()
        ui.button("back", on_click=lambda: ui.open('/'))
        ui.button("clear", on_click=lambda: df.drop(df.index, inplace=True))
        ui.button("save", on_click=lambda: print(df))  # save to JSON
    for i, row in df.iterrows():
        ui.label(f"{row.to_dict()}")


@ui.page('/')
def index():
    new = {}
    name = ui.input(label="name:").bind_value_to(new, 'name')
    address = ui.textarea(label="address:").bind_value_to(new, 'address')
    age = ui.number(label='age:').bind_value_to(new,'age')
    ui.button("submit", on_click=lambda: request_my_dict(new))


ui.run()
