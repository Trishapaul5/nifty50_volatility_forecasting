import plotly.express as px
import pandas as pd
df = pd.DataFrame({'x': [1, 2, 3], 'y': [10, 15, 13]})
fig = px.line(df, x='x', y='y', title='Test Plot')
fig.write_image('test_plot.png')
print('Plot saved successfully')
