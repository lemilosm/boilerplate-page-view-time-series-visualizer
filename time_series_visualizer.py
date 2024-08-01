import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
# df = None
df = pd.read_csv( 'fcc-forum-pageviews.csv' , index_col='date'  )

# Clean data
# Clean the data by filtering out days when the page views were 
# in the top 2.5% of the dataset or bottom 2.5% of the dataset.
# df = None
low_drop_limit = df['value'].quantile(0.025)
high_drop_limit = df['value'].quantile(1-0.025)
df = df[ (df['value'] >= low_drop_limit ) & (df['value'] <= high_drop_limit ) ]


#Create a draw_line_plot function that uses Matplotlib to draw 
# a line chart similar to "examples/Figure_1.png". 
# The title should be Daily freeCodeCamp Forum Page Views 5/2016-12/2019. 
# The label on the x axis should be Date and the label on the y axis should be Page Views.

#info>   https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16,4))
    ax.plot (df.index.values, df.values)
    ax.set(xlabel='Date', ylabel='Page Views', 
           title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.grid()
    # plt.show()
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


# Create a draw_bar_plot function that draws a bar chart similar to "examples/Figure_2.png". 
# It should show average daily page views for each month grouped by year. 
# The legend should show month labels and have a title of Months. On the chart, 
# the label on the x axis should be Years and the label on the y axis should be Average Page Views.

#info >  https://seaborn.pydata.org/generated/seaborn.barplot.html


def draw_bar_plot():
#     # Copy and modify data for monthly bar plot
#     df_bar = None
      df_bar = df.reset_index()
      df_bar['year'] = df_bar['date'].str.split('-', expand=True)[0]
      df_bar['month'] = df_bar['date'].str.split('-', expand=True)[1]
      df_bar['Month'] = pd.to_datetime(df_bar['date']).dt.month_name()

      df_bar.drop(columns='date',inplace=True)

      # now grouping by years and months, displaying then daily average(mean)
      df_bar = df_bar.groupby(['year','month','Month']).mean().reset_index()
      # df_bar.tail(13)

#     # Draw bar plot
      fig, ax = plt.subplots(figsize=(6, 6))
      hueOrder = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      # hueOrder = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

      # Draw the bar chart
      sns.barplot(x='year', y='value', hue='Month', data=df_bar, ax=ax,
                  hue_order=hueOrder,  palette = sns.color_palette(n_colors=12))

      # Set labels and title
      ax.set_xlabel('Years')
      # ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
      ax.tick_params(axis='x', labelrotation = 90)
      ax.set_ylabel('Average Page Views')
      ax.legend(title='Months')

      # plt.show()
#     # Save image and return fig (don't change this part)
      fig.savefig('bar_plot.png')
      return fig


# Create a draw_box_plot function that uses Seaborn to draw two adjacent box plots
# similar to "examples/Figure_3.png". These box plots should show how the values are
# distributed within a given year or month and how it compares over time.
# The title of the first chart should be Year-wise Box Plot (Trend) and
# the title of the second chart should be Month-wise Box Plot (Seasonality).
# Make sure the month labels on bottom start at Jan and the x and y axis are labeled correctly.
# The boilerplate includes commands to prepare the data.

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date']) #need to change dtype to datetime here
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
# info >  https://seaborn.pydata.org/generated/seaborn.boxplot.html
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Year-wise
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise
    # sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    plt.tight_layout()
    # plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig