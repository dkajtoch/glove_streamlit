import altair as alt

def render_most_similar(data, title):

    bars = (
    alt.Chart(data, height=400, title=title)
       .mark_bar()
       .encode(
           alt.X(
               'distance', 
               title='',
               scale=alt.Scale(domain=(0, 1.0), clamp=True),
               axis=None
            ),
            alt.Y(
               'word', 
               title='',
               sort=alt.EncodingSortField(
                   field='distance',
                   order='descending'
               )
            ),
            color=alt.Color('distance', legend=None, scale=alt.Scale(scheme='blues')),
            tooltip=[
                alt.Tooltip(
                    field='word',
                    type='nominal'
                ),
                alt.Tooltip(
                    field='distance',
                    format='.3f',
                    type='quantitative'
                )
            ]
       )
    )
    text = alt.Chart(data).mark_text(
        align='left',
        baseline='middle',
        dx=5,
        font='Roboto',
        size=15,
        color='black'
    ).encode(
        x=alt.X(
            'distance',
            axis=None
        ),
        y=alt.Y(
            'word',
            sort=alt.EncodingSortField(
                field='distance',
                order='descending'
            )
        ),
        text=alt.Text("distance", format=".3f"),
    )
    chart = bars + text
    chart = (chart.configure_axisX(
           labelFontSize=20,
           labelFont='Roboto',
           grid=False,
           domain=False
       )
       .configure_axisY(
           labelFontSize=20,
           labelFont='Roboto',
           grid=False,
           domain=False
       )
       .configure_view(
            strokeOpacity=0
       )
       .configure_title(
           fontSize=25,
           font='Roboto',
           dy=-10
       )
    )

    return chart

def render_compare(data):

    chart = (
    alt.Chart(data, height=200, title='Weights absolute value').mark_rect(binSpacing=3).encode(
        x=alt.X(
            'x:O',
            axis=None,
        ),
        y=alt.Y(
            'word:O',
            title=''
        ),
        color=alt.Color('weight:Q', scale=alt.Scale(scheme='redblue')),
    )
    .configure_axisX(
        labelFontSize=20,
        labelFont='Roboto',
        grid=False,
        domain=False
    )
    .configure_axisY(
        labelFontSize=20,
        labelFont='Roboto',
        grid=False,
        domain=False
    )
    .configure_title(
        fontSize=15,
        font='Roboto',
        dy=-10
    )
    .configure_view(
        strokeOpacity=0
    ))

    return chart

def render_absolute_compare(data):

    chart = (
    alt.Chart(data, title='Weights absolute difference').mark_line(point=True).encode(
        x=alt.X(
            'index',
            axis=None,
        ),
        y=alt.Y(
            'weight',
            title=''
        ),
        tooltip='weight'
    )
    .configure_axisX(
        labelFontSize=20,
        labelFont='Roboto',
        grid=False,
        domain=False
    )
    .configure_axisY(
        labelFontSize=12,
        labelFont='Roboto',
        grid=True,
        domain=False
    )
    .configure_title(
        fontSize=15,
        font='Roboto',
        dy=-10
    )
    .configure_view(
        strokeOpacity=0
    ))

    return chart