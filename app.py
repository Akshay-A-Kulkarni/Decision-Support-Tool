import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import io
import base64

#Custom function imports
import pareto_multi_d as pmd
import sqla

external_stylesheets = [dbc.themes.LUX]

df = pd.DataFrame([{'Upload Metadata + Connect CSV or DB': None} for i in range(10)])
mdf = pd.DataFrame([{'----': "Upload a Metadata File"}])

upload_file_name = ""
db_engine = None
table_obj = None
entity_names = ['Connect to a db first']
pill_button = {'border-radius': '40px'}

# Defining fields for db connections
hostname_input = dbc.FormGroup([
        dbc.Label("Hostname", width=2),
        dbc.Col(
            dbc.Input(id="db-field-1",
                      type="email", placeholder="Enter host connection information" ),
            width=10,),],row=True,
        )
user_input = dbc.FormGroup([
        dbc.Label("User", html_for="example-email-row", width=2),
        dbc.Col(
            dbc.Input(id="db-field-2",
                      type="User", placeholder="Enter User Name"),
            width=10,),],row=True,
        )
password_input = dbc.FormGroup([
        dbc.Label("Password", html_for="example-password-row", width=2),
        dbc.Col(
            dbc.Input(id="db-field-3",
                      type="password", placeholder="Enter password"),
            width=10,),],row=True,
        )
port_input = dbc.FormGroup([
        dbc.Label("Port", html_for="port-row", width=2),
        dbc.Col(
            dbc.Input(
                id="db-field-4",
                placeholder="Enter port",
            ),width=10,),],row=True,
        )
db_input = dbc.FormGroup([
        dbc.Label("Database", html_for="port-row", width=2),
        dbc.Col(
            dbc.Input(
                id="db-field-5",
                placeholder="Enter Database Name",
            ),width=10,),],row=True,
        )

# assigning form to variable
form = dbc.Form([hostname_input, user_input, password_input, port_input, db_input])

# creating pop prompt after clicking update
upload_modal = html.Div([
        dbc.Button("help", id="open-centered-info", color="info",
                   outline=True, style=pill_button, size='sm'),
        html.Span(" "),
        dbc.Button("Upload CSV  |  Connect DB", id="open-centered", color="success",
                   outline=True, style=pill_button),
        dbc.Modal([
                dbc.ModalBody([
                    html.Div([
                            dbc.Button(children=[
                                html.Span(
                                    "Upload A File [CSV or XLSX]", id="tooltip-target"),
                                dbc.Tooltip(
                                    "Click to upload the table/file containing Objective data",
                                    target="tooltip-target", offset=1000, placement='auto'
                                )],
                                id="collapse-button1",
                                className="mb-3",
                                color="primary",
                                style={'width': "100%"},),
                            dbc.Collapse(
                                dbc.Card(dbc.CardBody(dcc.Upload(
                                    id='upload-data',
                                    children=html.Div([
                                            'Drag and Drop',
                                            html.Br(),
                                            'or',
                                            html.Br(),
                                            dbc.Button('Click to Select Files', color="secondary",
                                                       className="mr-1")]),
                                    style={
                                        'width': '100%',
                                        'height': '20%',
                                        'lineHeight': '40px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '0px'},
                                    multiple=True, ))),
                                id="collapse1",
                            ),
                        ]
                    ),
                    html.Div([
                            dbc.Button(children=[
                                html.Span(
                                    "Upload MetaData", id="tooltip-target2"),
                                dbc.Tooltip(
                                    "Upload the Metadata file here Containing Col Names| Max/Min |"
                                    " Epsilon for your uploaded file",

                                    target="tooltip-target2", offset=100, placement='auto-end'
                                )],
                                id="collapse-button2",
                                className="mb-3",
                                color="primary",
                                style={'width': "100%"},),
                            dbc.Collapse(
                                dbc.Card(dbc.CardBody(dcc.Upload(
                                    id='upload-metadata',
                                    children=html.Div([
                                            'Drag and Drop',
                                            html.Br(),
                                            'or',
                                            html.Br(),
                                            dbc.Button('Click to Select Files', color="secondary",
                                                       className="mr-1")]),
                                    style={
                                        'width': '100%',
                                        'height': '20%',
                                        'lineHeight': '40px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '0px'},
                                    multiple=True, ))
                                ),
                                id="collapse2",),]),
                    html.Hr(),
                    html.H5("CONNECT TO A DB"),
                    html.Br(),
                    form,]),
                dbc.ModalFooter(
                    dbc.Button(
                        id='db-submit-button', n_clicks=0, children=['Connect'], color='primary'
                        , style=pill_button, className="ml-auto")
                ),
            ],
            id="modal-centered",
            centered=True,
        ),
    ]
)

image_filename = 'howto.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

info_modal = html.Div(
    [dbc.Modal(id="modal-centered-info",
               keyboard=True,
               backdrop=True,
               # size='lg',
               autoFocus=True,
               children=[
                   html.Div([
                           html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), width="100%") ])
               ])
     ])

# Navbar config
navbar = dbc.NavbarSimple(id='navbar',
                          children=[
                              html.Span([html.Br(),
                                         dbc.Badge(children="Table", pill=True, color="dark", className="mr-3",
                                                   id='csvbadge'),
                                         dbc.Badge(children="MetaFile", pill=True, color="dark", className="mr-3",
                                                   id='metabadge'),]),
                              upload_modal,
                              info_modal,],
                          brand=" 📈 Decision Support Framework ",
                          brand_href="#",
                          # light=True,
                          fluid=True,
                          color="primary",
                          dark=True,
                          brand_style={
                              "font-size": "25px"}
                          )

# The app is sectioned off in to two containers called "Cards"
# these cards contain all elements that need to be rendered by Dash
# the first container/Panel is controls
# and the second panel is for the matrix and pareto curve
first_panel = dbc.Card(
    dbc.CardBody(([
            html.H5("Control Panel"),
            html.Hr(),
            dbc.FormGroup([
                dbc.Label("Select A Table", html_for="dropdown"),
                dcc.Dropdown(
                    id='table-dropdown',
                    multi=False,
                    value=None,
                    style={
                        'width': '100%'},
                    placeholder="Select a Table",)], id='tb-dpwn'),
            dbc.FormGroup([
                dbc.Label("Select A Column", html_for="dropdown"),
                dcc.Dropdown(
                    id='column-dropdown',
                    multi=True,
                    style={
                        'width': '100%'},
                    placeholder="Select a column",
                    value=None)]),
            html.Hr(),
            html.Div(id='warn_user', style={'display': 'none'}),
            dbc.FormGroup([
                dbc.Label("Pareto X-axis", html_for="dropdown"),
                dcc.Dropdown(
                    id='pareto-x-dropdown',
                    multi=False,
                    style={
                        'width': '100%'},
                    placeholder="Select a column for x-axis",
                    value=None)]),
            dbc.FormGroup([
                dbc.Label("Pareto Y-axis", html_for="dropdown"),
                dcc.Dropdown(
                    id='pareto-y-dropdown',
                    multi=False,
                    style={
                        'width': '100%'},
                    placeholder="Select a column for y-axis",
                    value=None),
                html.Br(),
                dbc.FormGroup([
                    dbc.Label("Pareto Z-axis (Optional)", html_for="dropdown"),
                    dcc.Dropdown(
                        id='pareto-z-dropdown',
                        multi=False,
                        style={
                            'width': '100%'},
                        placeholder="Select a column for z-axis",
                        value=None),]),
                dbc.FormGroup([
                    dbc.Label("Hover Label", html_for="dropdown"),
                    dcc.Dropdown(
                        id='pareto-label-dropdown',
                        multi=False,
                        style={
                            'width': '100%'},
                        placeholder="Select a column for hover information",
                        value=None),])
                ]),
            html.Br(),
            dbc.Button(id='submit-button', n_clicks=0, children='Plot', color="success",
                       outline=False, size="sm", style=pill_button),
        ]
    ))
)
second_panel = dbc.Card(
    dbc.Tabs([
        dbc.Tab(
            dbc.CardBody([
                html.Div(id="output-data-upload", style={'display': 'none'},
                         children=dcc.Store(id='csvdata', storage_type='session')),
                html.Div(id="output-metadata-upload", style={'display': 'none'},
                         children=dcc.Store(id='metadata', storage_type='session')),
                html.Div(id='output-data-db', children=[
                    dash_table.DataTable(
                        id='dmatrix',
                        columns=[
                            {"name": i, "id": i, 'hideable': 'last'} if i is 'Optimal'
                            else {"name": i, "id": i}
                            for i in df.columns],
                        data=df.to_dict('records'),
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={'maxHeight': '800',
                                     'minHeight': '800',},
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        style_cell={
                            'width': '150px',
                            'whiteSpace': 'normal',
                            'padding': '5px',
                            'textAlign': 'center',},
                        style_header={
                            'color': 'black',
                            'backgroundColor': 'white',  # 'rgb(50, 50, 50)'
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            'padding': '5px'},
                        row_deletable=True,
                        virtualization=True,
                        page_action="native",
                        export_format='xlsx',
                        style_header_conditional=[{
                                'if': {'column_id': "Optimal"},
                                'maxWidth': '50'}],
                    )
                ]),
            ]),
            label='Decision Matrix', tab_id='Decision Matrix', tab_style={"width": "150px", 'text-align': 'center'}
        ),
        dbc.Tab(
            dbc.CardBody([
                    html.H5("Pareto Frontier", className="card-title"),
                    html.Div(id='output-scattergraph'),]
            ), label='Pareto Frontier', tab_id='Pareto Curve', tab_style={"width": "150px", 'text-align': 'center'}
        ),

    ], active_tab="Decision Matrix", id="panel-2-tabs")
)

# function to parse the uploaded file and return a div with datatable
def parse_file(contents, filename):
    content_type, content_string = contents.split(',')
    global upload_file_name
    upload_file_name = filename
    decoded = base64.b64decode(content_string)
    parsed_df = None
    try:
        if 'csv' in filename:
            parsed_df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            parsed_df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(['There was an error with this file.'])
    return parsed_df

def render_datatable(df):
    global upload_file_name
    return html.Div([
        html.H5(upload_file_name),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            fixed_rows={'headers': True, 'data': 0},
            style_cell={'width': '150px',
                        'whiteSpace': 'normal'},
            css=[{
                'selector': '.dash-cell div.dash-cell-value',
                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=True,
            selected_rows=[],
            page_action="native"
        ),
        html.Hr()])

# combining both cards
cards = dbc.Row([dbc.Col(first_panel, width={"size": 3, "order": "first", 'offset': 1}, className="h-100"),
                 dbc.Col(second_panel, width={"size": 7, "order": "last"}, style={'height': '100%'})]
                )

# IMP - App declaration.
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{
                    'name': 'google-site-verification',
                    'content': 'QtIIAiwLtIrLRaMj7PQaIrsaU1K-BlrmLDqi1u6ap3k'}]
                )
server = app.server
app.title = "Decision Support Tool"
app.layout = html.Div([
    navbar,
    dbc.Container([
        html.Br(),
        cards
    ], fluid=True)
])

# All callbacks below this line.
@app.callback(
    [Output("modal-centered", "is_open"),
     Output('column-dropdown', 'value')],
    [Input("open-centered", "n_clicks"),
     Input("db-submit-button", "n_clicks")],
    [State("modal-centered", "is_open")],)
def toggle_modal(n1, n2, is_open):
    clr_col = ''
    if n1 or n2:
        return not is_open, clr_col

    return is_open, clr_col

@app.callback(
    Output("modal-centered-info", "is_open"),
    [Input("open-centered-info", "n_clicks")],
    [State("modal-centered-info", "is_open")],)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open,

    return is_open

@app.callback(Output('csvdata', 'data'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_csv_output(list_contents, list_names):
    if list_contents is not None:
        # global df
        children = [(parse_file(c, n)) for c, n in zip(list_contents, list_names)]
        csvdf = children[0]
        return csvdf.to_dict("records")

@app.callback(Output('metadata', 'data'),
              [Input('upload-metadata', 'contents')],
              [State('upload-metadata', 'filename')])
def update_metadata_output(list_contents, list_names):
    if list_contents is not None:
        # global mdf
        t = [(parse_file(c, n)) for c, n in zip(list_contents, list_names)]
        mdf = t[0]
        return mdf.to_dict('records')

@app.callback([Output('table-dropdown', 'options'),
               Output('table-dropdown', 'disabled')],
              [Input('db-submit-button', 'n_clicks')],
              [State(f"db-field-{i}", "value") for i in range(1, 6)])
def connect_db(n_clicks, hostname, username, password, port, dbname):
    global upload_file_name

    global db_engine

    if dbname is not None:
        upload_file_name = ''
        disable_dropdown = False
    else:
        disable_dropdown = True

    if username and password and hostname and port and dbname is True and upload_file_name == '':

        db_engine = sqla.db_connect(username, password, hostname, port, dbname)
        table_names = sqla.get_table_names(db_engine)
        return [{'label': i, 'value': i} for i in table_names], disable_dropdown
    else:
        disable_dropdown = False
        return [{'label': i, 'value': i} for i in entity_names], disable_dropdown

@app.callback(
    Output('column-dropdown', 'options'),
    [Input('csvdata', 'data')],
    [State('table-dropdown', 'value')])
def update_col_dropdown(csvdata, tbl_name):
    if tbl_name is not None and csvdata is None:
        global db_engine
        columns = sqla.get_column_names(db_engine, tbl_name)
        return [{'label': i, 'value': i} for i in columns]
    elif csvdata is not None:
        c = csvdata[0]
        columns = c.keys()
        return [{'label': i, 'value': i} for i in columns]
    else:
        return [{'label': i, 'value': i} for i in df.columns]

@app.callback(
    [Output('dmatrix', 'data'),
     Output('dmatrix', 'columns'),
     Output('dmatrix', 'style_data_conditional')],
    [Input('column-dropdown', 'value')],
    [State('csvdata', 'data'),
     State('metadata', 'data'),
     State('table-dropdown', 'value')])
def output_db_table(value, csv, metadata, tableName):
    global df
    global db_engine
    optim_rows = []

    if value is not None:
        if tableName is not None and tableName != 'Connect to a db first':
            meta_df = pd.DataFrame(metadata)
            t_obj = sqla.get_table_class(db_engine, tableName)
            df_list = [sqla.obj2dic(o) for o in t_obj]
            upload_df = pd.DataFrame(df_list)
            if metadata is not None:
                upload_df['row_index'] = np.arange(len(upload_df))
                optim_df = pmd.plot_nondominated_sets(upload_df, meta_df, output='table')
                full_df = pd.merge(upload_df, optim_df['row_index'], how='left', indicator='Optimal', on='row_index')
                full_df.Optimal.replace(to_replace=dict(both="True", left_only="False"), inplace=True)
                value.insert(0, 'Optimal')
                up_df = full_df[value]
                columns = [{"name": i, "id": i, 'hideable': 'last'} if i is 'Optimal'
                           else {'id': i, 'name': i} for i in up_df.columns]
                data = up_df.to_dict("records")
                optim_rows = [{
                    'if': {
                        'column_id': colname,
                        'filter_query': '{Optimal} eq "True"'
                    },
                    'backgroundColor': '#3D9970',
                    'color': 'black',
                    "fontWeight": 'bold'
                } for colname in value]
                return [data, columns, optim_rows]
            else:
                tmp_df = upload_df[value]
                columns = [{'id': i, 'name': i} for i in tmp_df.columns]
                optim_rows = [{
                    'if': {
                        'column_id': colname,
                    },
                    'backgroundColor': '#BEBEBE',
                    'color': 'black',
                } for colname in value]
                data = tmp_df.to_dict("records")
                return [data, columns, optim_rows]
        elif csv is not None and len(value) is not 0:
            csv_df = pd.DataFrame(csv)
            if metadata is not None:
                meta_df = pd.DataFrame(metadata)
                csv_df['row_index'] = np.arange(len(csv_df))
                optim_df = pmd.plot_nondominated_sets(csv_df, meta_df, output='table')
                full_df = pd.merge(csv_df, optim_df['row_index'], how='left', indicator='Optimal', on='row_index')
                full_df.Optimal.replace(to_replace=dict(both="True", left_only="False"), inplace=True)
                value.insert(0, 'Optimal')
                up_df = full_df[value]
                columns = [{"name": i, "id": i, 'hideable': 'last'} if i is 'Optimal'
                           else {'id': i, 'name': i} for i in up_df.columns]
                data = up_df.to_dict("records")
                optim_rows = [{
                    'if': {
                        'column_id': colname,
                        'filter_query': '{Optimal} eq "True"'
                    },
                    'backgroundColor': '#3D9970',
                    'color': 'black',
                    "fontWeight": 'bold'
                } for colname in value]
                return [data, columns, optim_rows]
            else:
                tmp_df = csv_df[value]
                columns = [{'id': i, 'name': i} for i in tmp_df.columns]
                optim_rows = [{
                    'if': {'column_id': colname,},
                    'backgroundColor': '#BEBEBE',
                    'color': 'black',} for colname in value]
                data = tmp_df.to_dict("records")
                return [data, columns, optim_rows]
        else:
            temp_df = df
            columns = [{'id': i, 'name': i} for i in temp_df.columns]
            data = temp_df.to_dict('records')
            return [data, columns, optim_rows]
    else:
        temp_df = df
        columns = [{'id': i, 'name': i} for i in temp_df.columns]
        data = temp_df.to_dict('records')
        return [data, columns, optim_rows]

@app.callback(
    Output('output-scattergraph', 'children'),
    [Input('dmatrix', "derived_virtual_data"),
     Input('submit-button', 'n_clicks')],
    [State('metadata', 'data'),
     State('pareto-x-dropdown', 'value'),
     State('pareto-y-dropdown', 'value'),
     State('pareto-z-dropdown', 'value'),
     State('pareto-label-dropdown', 'value')])
def update_pareto_scatterplot(filtered_df, n_clicks, mdf, col1, col2, col3, label):
    mdf = pd.DataFrame(mdf)
    if col1 and col2 is not None:
        if filtered_df is not None:
            scat_table = pd.DataFrame(filtered_df)
            scat_table = scat_table.drop(columns=['Optimal'])
            scat_table['row_index'] = np.arange(len(scat_table))
            plot = pmd.plot_nondominated_sets(df=scat_table, mdf=mdf,
                                              x_axis=col1, y_axis=col2, z_axis=col3, hoverlabel=label)
            return dcc.Graph(figure=plot)

@app.callback(
    Output('panel-2-tabs', 'active_tab'),
    [Input('submit-button', 'n_clicks'),
     Input('db-submit-button', 'n_clicks')])
def change_tabs(plot_clicks, db_clicks):
    if plot_clicks:
        return 'Pareto Curve'
    elif db_clicks:
        return 'Decision Matrix'

@app.callback(
    [Output('pareto-x-dropdown', 'options'),
     Output('pareto-y-dropdown', 'options'),
     Output('pareto-label-dropdown', 'options'),
     Output('pareto-z-dropdown', 'options')],
    [Input('column-dropdown', 'value')])
def update_pareto_dropdown(value):
    global mdf
    if value is not None:
        columns = value
        return ([{'label': i, 'value': i} for i in columns],
                [{'label': i, 'value': i} for i in columns],
                [{'label': i, 'value': i} for i in columns],
                [{'label': i, 'value': i} for i in columns])
    else:
        return ([{'label': i, 'value': i} for i in mdf.columns.values],
                [{'label': i, 'value': i} for i in mdf.columns.values],
                [{'label': i, 'value': i} for i in mdf.columns.values],
                [{'label': i, 'value': i} for i in mdf.columns.values])

@app.callback(
    Output("collapse1", "is_open"),
    [Input("collapse-button1", "n_clicks")],
    [State("collapse1", "is_open"), ],)
def toggle_collapse1(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse2", "is_open"),
    [Input("collapse-button2", "n_clicks")],
    [State("collapse2", "is_open")],)
def toggle_collapse2(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("tb-dpwn", "style"),
    [Input("csvdata", "data")])
def hide_table_dropdown(csvdata):
    if csvdata is not None:
        style = {'display': 'none'}
        return style

@app.callback(
    [Output("csvbadge", "children"),
     Output("metabadge", "children"),
     Output("csvbadge", "color"),
     Output("metabadge", "color")],
    [Input("csvdata", "data"),
     Input("metadata", "data")])
def status_badges(csvdata, metadata):
    c1 = 'No Tables Uploaded',
    c2 = 'No Metadata Uploaded'
    csvcolor = 'danger'
    metacolor = 'danger'
    if csvdata is not None:
        c1 = 'Table ✔',
        csvcolor = 'success'
    if metadata is not None:
        c2 = 'MetaFile ✔',
        metacolor = 'success'
    return c1, c2, csvcolor, metacolor

@app.callback(
    [Output("warn_user", "children"),
     Output("warn_user", "style")],
    [Input('submit-button', 'n_clicks')],
    [State('pareto-x-dropdown', 'value'),
     State('pareto-y-dropdown', 'value'),
     State('pareto-z-dropdown', 'value'),
     State('metadata', 'data')])
def check_pareto_dropdowns(n, x, y, z, metadata):
    style = {'display': 'none'}
    selection = []
    if n:
        if metadata is None:
            style = {}
            children = [dbc.Alert(
                "Please upload a metadata file otherwise there will be no row highlighting of the n-dimensional "
                "optimal points in the Matrix "
                "or plot the Pareto points on a graph.",
                color="info")]
            return children, style

        if x and y is not None and x != y:
            selection = [x, y]
            if z is not None:
                selection = [x, y, z]
        else:
            style = {}
            children = [dbc.Alert("You must select at least two distinct X & Y axes before plotting", color="danger")]
            return children, style

        if metadata is not None:
            mlist_df = pd.DataFrame(metadata)
            m_list = mlist_df['Col_Name'].values
            result = all(elem in m_list for elem in selection)
            if result is True:
                children = []
                style = {'display': 'none'}
                return children, style
            else:
                style = {}
                children = [dbc.Alert("The selections made are not in the metadata file, "
                                      "Please only choose columns which have associated metadata for plotting",
                                      color="warning")]
                return children, style
    else:
        return [], style

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False)
