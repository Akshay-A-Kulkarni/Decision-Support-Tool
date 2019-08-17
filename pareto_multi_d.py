import pareto
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objs as go


def plot_nondominated_sets(df, mdf, x_axis=None, y_axis=None, z_axis=None, hoverlabel=None, output='plot'):
    """
    Takes in parameters and returns a figure object to be plotted by plotly

    :param df: Input objectives table as a pandas dataframe
    :param mdf: Input metadata file as a pandas dataframe
    :param x_axis: Objective name to be plotted on the X-axis [STRING]
    :param y_axis: Objective name to be plotted on the Y-axis [STRING]
    :param z_axis: Objective name to be plotted on the Y-axis [STRING]
    :param hoverlabel: Objective name to be used to tag all the points [STRING]
    :param output: specifies the output of the fucntion [STRING]
    :return: Plotly Figure object [use plotly.offline.plot() ]
    """

    if output == 'table':
        objective_names = []
        max_col = []
        eps_vals = []

        # df = df.dropna()

        for i in range(len(mdf)):
            row = mdf.iloc[i]
            default_epsilon = 1e-9
            objective_names.append(row['Col_Name'])
            if pd.isna(row['Epsilon']):
                eps_vals.append(default_epsilon)
            else:
                eps_vals.append((row['Epsilon']))
            if row['Max_Min'] == 'Max':
                max_col.append(row['Col_Name'])

        objective_cols = [df.columns.get_loc(c) for c in objective_names if c in df]  # Converts col-names to col_ids
        max_col_ids = [df.columns.get_loc(c) for c in max_col if c in df]

        nondominated_set_multi = pareto.eps_sort([list(df.itertuples(False))],
                                                 objectives=objective_cols, maximize=max_col_ids, epsilons=eps_vals)
        nondominated_df_multi = pd.DataFrame(nondominated_set_multi)

        nondominated_df_multi.columns = df.columns
        return nondominated_df_multi
    else:
        if z_axis:
            plot_list = [x_axis, y_axis, z_axis]
        else:
            plot_list = [x_axis, y_axis]

        plot_mdf = mdf.loc[mdf['Col_Name'].isin(plot_list)]
        plot_col_ids = [df.columns.get_loc(c) for c in plot_list if c in df]
        plot_max_cols = [df.columns.get_loc(c) for c in plot_mdf.query('Max_Min == "Max"')['Col_Name'].values if c in df]
        col_eps = [1e-9 if pd.isna(e) else e for e in plot_mdf['Epsilon']]

        nondominated_set = pareto.eps_sort([list(df.itertuples(False))],
                                           objectives=plot_col_ids,
                                           maximize=plot_max_cols, epsilons=col_eps)

        nondominated_df = pd.DataFrame(nondominated_set)
        nondominated_df.columns = df.columns

        full_df = pd.merge(df, nondominated_df['row_index'], how='left', indicator='Optimal', on='row_index')
        full_df.Optimal.replace(to_replace=dict(both="True", left_only="False"), inplace=True)

        if z_axis is None:
            nd_points_list = [(nondominated_df[x_axis].values[i], nondominated_df[y_axis].values[i])
                              for i in range(len(nondominated_df))]
            nd_points_list.sort(key=lambda tup: tup[1])
            x, y = map(list, zip(*nd_points_list))

        if x_axis and y_axis and z_axis:
            fig = px.scatter_3d(full_df, x=x_axis, y=y_axis, z=z_axis,
                                color='Optimal', hover_name=hoverlabel,
                                color_discrete_map={"True": "#23B58A", 'False': "#B5234E"})
            fig.data[0].marker.size = 12
            fig.data[0].marker.line.width = 2
            fig.data[0].marker.line.color = "black"
            fig.update_layout(scene=dict(
                xaxis_title=x_axis,
                yaxis_title=y_axis,
                zaxis_title=z_axis),
                height=545,
                margin=dict(r=0, b=0, l=0))
            return fig

        elif x_axis and y_axis:
            fig = px.scatter(full_df, x=x_axis, y=y_axis,
                             color='Optimal', hover_name=hoverlabel,
                             color_discrete_map={"True": "#23B58A", 'False': "#B5234E"})
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines",
                                     line=go.scatter.Line(shape='linear', color='#3D9970'), showlegend=False))
            fig.data[0].marker.size = 12
            fig.data[0].marker.line.width = 2
            fig.data[0].marker.line.color = "black"


            fig.update_layout(
                height=545,
                title=go.layout.Title(
                    xref="paper",
                    x=0,
                ),
                xaxis=go.layout.XAxis(
                    title=go.layout.xaxis.Title(
                        text=x_axis,
                        font=dict(
                            size=18,
                            color="#7f7f7f"
                        )
                    )
                ),
                yaxis=go.layout.YAxis(
                    title=go.layout.yaxis.Title(
                        text=y_axis,
                        font=dict(
                            size=18,
                            color="#7f7f7f"
                        )
                    )
                )
            )
            return fig

        else:
            raise Exception('You must supply at least two axes')







