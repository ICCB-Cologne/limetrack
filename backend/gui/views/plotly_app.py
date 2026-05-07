import dash
from dash import dcc, html, Dash
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from ..models import HistopathologicalSample


app = DjangoDash('SimpleExample')   # replaces dash.Dash




first_sample = HistopathologicalSample.objects.first()
column_names = [field.verbose_name for field in first_sample._meta.fields]

verbose_to_field = {
            field.verbose_name: field.name
            for field in HistopathologicalSample._meta.get_fields()
            if hasattr(field, "verbose_name")
        }

field_names = [
            verbose_to_field[cn] for cn in column_names
        ]

samples = list(
            HistopathologicalSample.objects.values(*field_names)
        )

df = pd.DataFrame(data=samples, columns=column_names)

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

graph1 = dcc.Graph(
    id='example-graph',
    figure=fig
    )



app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-color',
        options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
        value='red'
    ),
    html.Div(id='output-color'),
    dcc.RadioItems(
        id='dropdown-size',
        options=[{'label': i,
                  'value': j} for i, j in [('L','large'), ('M','medium'), ('S','small')]],
        value='medium'
    ),
    html.Div(id='output-size')

])

@app.callback(
    dash.dependencies.Output('output-color', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value')])
def callback_color(dropdown_value):
    return "The selected color is %s." % dropdown_value

@app.callback(
    dash.dependencies.Output('output-size', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value'),
     dash.dependencies.Input('dropdown-size', 'value')])
def callback_size(dropdown_color, dropdown_size):
    return "The chosen T-shirt is a %s %s one." %(dropdown_size,
                                                  dropdown_color)