# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 11:41:49 2020

@author: Krishna Kinger
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime 
from custom_processor import process_coauthorship

colors = ['red', 'green', 'blue', 'brown', 'burlywood', 'cadetblue', 'chocolate', 
          'coral', 'cornflowerblue','orangered', 'royalblue', 'saddlebrown','darkblue', 
          'darkcyan','darkgoldenrod', 'darkgray', 'maroon', 'darkgreen', 'orange', 
          'salmon', 'sandybrown']

def add_time(dt, duration):
    return (dt+ datetime.timedelta(0,86400*int(duration)))

def listDirectories(path):
    dir_dict = {}
    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)):
            dir_dict[name] = path+"/"+name
    return dir_dict
    

def listFiles(path):
    for root, dirs, files in os.walk(path):
        return files

def findChannels(path):
    channel_list = []
    for file in listFiles(path):
        channel = path+'/'+file
        channel_list.append(channel)
    return channel_list

def process_channels(path):
    channels = findChannels(path)
    users = []
    for channel in channels:
        df = pd.read_csv(channel)
        columns = df.columns.tolist()
        if ('Time' and 'Duration') in columns:
            if 'Source' and 'Target' in columns:
                users.extend(df.Source)
                users.extend(df.Target)
                channel_type = 'INST'#Inter-Node Span Transaction
            else:
                users.extend(df.Source)
                channel_type = 'IST'#Indidual Span Transaction
        else:
            users.extend(df.Source)
            channel_type = 'INIT'#Inter-Node Instant Transaction
    return np.unique(np.array(users)), channel_type

def process_INIT(df):
    tim_arr, y_arr = [], []
    for i in range(len(df.Time)):
        tim_arr.append(df.Time[i])
        tim_arr.append(df.Time[i])
        tim_arr.append(df.Time[i])
        y_arr.append(df.Source[i])
        y_arr.append(df.Target[i])
        y_arr.append(None)
    return tim_arr, y_arr

def process_IST(df):
    tim_arr, time_list, y = [], [], []
    for i in range(len(df['Source'])):
        tim_arr.append(df['Time'][i])
        temp = add_time(df['Time'][i], df['Duration'][i])
        tim_arr.append(temp)
        time_list.append(temp)
        tim_arr.append(None)
        y.append(df['Source'][i])
        y.append(df['Source'][i])
        y.append(None)
    return tim_arr, time_list, y

def process_INST(df):
    tim_arr, y_arr, time_list = [], [], []
    for i in range(len(df.Time)):
        tim_arr.append(df.Time[i])
        temp = add_time(df['Time'][i], df['Duration'][i])
        tim_arr.append(temp)
        time_list.append(temp)
        tim_arr.append(df.Time[i])
        y_arr.append(df.Source[i])
        y_arr.append(df.Target[i])
        y_arr.append(None)
    return tim_arr, y_arr, time_list

def generate_plot(path):
    channels = findChannels(path)
    ite = 0
    fig = go.Figure()
    if 'CUSTOM' in path:
        if 'COAUTHORSHIP' in path:
            return process_coauthorship(channels)
    for channel in channels:
        legend_name = channel.replace('.csv', '')
        legend_name = legend_name[legend_name.rfind('/')+1:]
        df = pd.read_csv(channel)
        df.Time = pd.to_datetime(df.Time)
        columns = df.columns.tolist()
        if ('Time' and 'Duration') in columns:
            if 'Source' and 'Target' in columns:
                channel_type = 'INST'#Inter-Node Span Transaction
                tim_arr, y_arr, time_list = process_INST(df)
                fig.add_trace(go.Scatter(x = tim_arr, y = y_arr, opacity = 0.5,legendgroup=legend_name, name=legend_name, line=dict(color=colors[ite], width=2)))
                fig.add_trace(go.Scatter(x=df['Time'], y= df['Source'],opacity = 0.5, legendgroup=legend_name, name='Source', mode='markers', marker_symbol=0, marker=dict(color=colors[ite],size=5)))
                fig.add_trace(go.Scatter(x=time_list, y= df['Target'],opacity = 0.5, legendgroup=legend_name, name='Target', mode='markers', marker_symbol=11, marker=dict(color=colors[ite],size=5)))

            else:
                channel_type = 'IST'#Indidual Span Transaction
                tim_arr, time_list, y = process_IST(df)
                fig.add_trace(go.Scatter(x = tim_arr, y = y,opacity = 0.5, legendgroup=legend_name, name=legend_name, line=dict(color=colors[ite], width=3)))
                fig.add_trace(go.Scatter(x=df['Time'],opacity = 0.8, y= df['Source'], legendgroup=legend_name, name='Source', mode='markers', marker_symbol=0, marker=dict(color=colors[ite],size=5)))
                fig.add_trace(go.Scatter(x=time_list,opacity = 0.8, y= df['Source'], legendgroup=legend_name, name='Destination', mode='markers', marker_symbol=11, marker=dict(color=colors[ite],size=5)))
        else:
            channel_type = 'INIT'#Inter-Node Instant Transaction
            tim_arr, y_arr = process_INIT(df)
            fig.add_trace(go.Scatter(x = tim_arr, y = y_arr, opacity = 0.5,legendgroup=legend_name, name=legend_name, line=dict(color=colors[ite], width=2)))
            fig.add_trace(go.Scatter(x=df['Time'], y= df['Source'],opacity = 0.5, legendgroup=legend_name, name='Source', mode='markers', marker_symbol=100, marker=dict(color=colors[ite],size=5)))
            fig.add_trace(go.Scatter(x=df['Time'], y= df['Target'],opacity = 0.5, legendgroup=legend_name, name='Target', mode='markers', marker_symbol=11, marker=dict(color=colors[ite],size=5)))
            
        ite+=1
    fig.update_layout(
                    xaxis = dict(
                        side='top'
                    ),
                    yaxis = dict(
                        type = 'category'
                    ),
                    height=900
                )
    return fig

if __name__ == "__main__":
    dirs = listDirectories('../data')
    options = [{'label':key, 'value':value} for key, value in dirs.items()]