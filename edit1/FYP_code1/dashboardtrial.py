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
    df = pd.read_csv('obd.csv', index_col=None, parse_dates=True)
    rpm_mean = df['ENGINE_RPM'].mean()

    return render_template('dashboardtrial.html',rpm_mean=rpm_mean)


if __name__=="__main__":
    app.run()
