import pandas as pd
import plotly.graph_objects as go
import base64
from io import BytesIO

def bar_chart(data):
    df = pd.DataFrame(data).T.reset_index().rename(columns={'index': 'Category'})
    df = df.sort_values(by='subscribers', ascending=False).head(10)
    fig = go.Figure(data=[
        go.Bar(x=df['Category'], y=df['subscribers'], name='Subscribers'),
        go.Bar(x=df['Category'], y=df['video views'], name='Video Views')
    ])
    fig.update_layout(title='YouTube Channel Statistics', xaxis_title='Category', yaxis_title='Count', barmode='group')
    if len(df['Category']) > 8:
        fig.update_layout(xaxis=dict(tickangle=90))
    else:
        fig.update_layout(xaxis=dict(tickangle=60))
    fig.update_traces(marker=dict(line=dict(color='black', width=1)))
    htmlstring = fig.to_html(full_html=False)
    pngstring = fig.to_image(format="png")
    return htmlstring, pngstring

# calling the function
htmlstring, pngstring = bar_chart({"Music":{"subscribers":5195000000,"video views":3121477506633},"Entertainment":{"subscribers":5158200000,"video views":2527739309583},"People & Blogs":{"subscribers":2779400000,"video views":1265791201548}})