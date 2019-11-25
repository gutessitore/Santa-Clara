# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

# external CSS stylesheets
external_css = [
    'https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.0/normalize.css',
    'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css',
    '//fonts.googleapis.com/css?family=Raleway:400,300,600',
    'https://use.fontawesome.com/releases/v5.2.0/css/all.css'
]

app = dash.Dash(
    name=__name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    #external_stylesheets= external_stylesheets
)
app.scripts.config.serve_locally = False

app.layout = html.Div(
    children=[

        html.Div(
            id='main_menu',
            children=[
                html.Div(
                    children=html.H1('Relatorio', id='title', className='h1'), className='three columns',
                    id='title_value',
                    style='row'
                ),
            ],
            className='row'
        ),

        html.Div(
            id='container_discretizacao',
            children=html.Div(
                dcc.Dropdown(
                    id='drop_discretizacao',
                    options=[
                        {'label': 'Diária', 'value': 'D'},
                        {'label': 'Semanal', 'value': 'W'}
                    ],
                    value='D'
                ),

            ),
            #style='four columns'
            #style={'width': '25%', 'display': 'inline-block', 'float': 'left', 'verticalAlign': 'top'}
        )



    ],
    id='main',
    className='one.column'
)


if __name__ == "__main__":
    app.run_server(debug=True)