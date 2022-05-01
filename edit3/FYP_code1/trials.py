from flask import Flask,send_file,render_template
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

fig,ax=plt.subplots(figsize=(6,6))
#ax=sns.set_stype(style="darkgrid")


app=Flask(__name__)

@app.route('/')
def home():
    return render_template('trial.html')

@app.route('/visualize')
def visualize():
    df = pd.read_csv('obd.csv', index_col=None, parse_dates=True)
    #plt.figure(figsize=(20, 20))s
    plt.xticks(rotation='vertical')

    sns.lineplot(df['DEVICE DATE'],df['ENGINE_RPM'])

    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')

if __name__=="__main__":
    app.run()
