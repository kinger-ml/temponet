# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 20:31:42 2020

@author: Krishna Kinger
"""
import pandas as pd
import plotly.graph_objects as go

colors = ['red', 'green', 'blue', 'brown', 'burlywood', 'cadetblue', 'chocolate', 
          'coral', 'cornflowerblue','orangered', 'royalblue', 'saddlebrown','darkblue', 
          'darkcyan','darkgoldenrod', 'darkgray', 'maroon', 'darkgreen', 'orange', 
          'salmon', 'sandybrown']

def process_coauthorship(channels):
    for channel in channels:
        df = pd.read_csv(channel)
        df.Time = pd.to_datetime(df.Time)
        df.Paper = df.Paper.apply(str)
        fig = go.Figure()
        i=0
        conferences = df.Conference.unique()
        for conference in conferences:
            temp = df[df.Conference == conference]
            papers = temp.Paper.unique()
            tim_arr, y_arr = [],[]
            for paper in papers:
                df1 = temp[temp.Paper == paper]
                tim_arr.extend([df1.Time.iloc[0]]*(len(df1)+1))
                y_arr.extend(df1.Author.tolist())
                y_arr.append(None)
            fig.add_trace(go.Scatter(x = tim_arr, y = y_arr, opacity = 0.5, name=conference, line=dict(width=2, color=colors[i])))
            i+=1
        return fig

if __name__ == "__main__":
    pass
