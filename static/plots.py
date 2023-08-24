import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
from matplotlib.backends.backend_pdf import PdfPages

def ploter(data1, data2, data3, data4, h, f1, f2,hm,f1m,f2m):
    # data = [data1, data2, data3, data4]
    data = [data1,data3, data4]
    fig1, ax1 = plt.subplots()
    ax1.boxplot(data)
    # ax1.set_xticklabels(['IMD', 'GCM Historical', 'GCM Future1', 'GCM Future2'])
    ax1.set_xticklabels(['IMD(1975-2014)','Future1(2021-2060)', 'Future2(2061-2100)'])
    ax1.set_ylabel('Temperature Data (°C)')
    ax1.set_title('Comparison of temperature for different time periods')
    # ax1.yaxis.grid(True)
    # ax1.xaxis.grid(True)
    ax1.yaxis.set_major_locator(plt.MultipleLocator(2))
    month =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    fig2, ax2 = plt.subplots()
    ax2.plot(month,h, label='Historical(1975-2014)')
    ax2.plot(month,f1, label='Future1(2021-2060)')
    ax2.plot(month,f2, label='Future2(2061-2100)')
    ax2.set_xlabel('Month ')
    ax2.set_ylabel('Mean Temperature (°C)')
    ax2.set_title('Monthly Mean Temperatures')
    ax2.legend()
   
    fig3, ax3 = plt.subplots()
    ax3.plot(month,hm, label='Historical(1975-2014)')
    ax3.plot(month,f1m, label='Future1(2021-2060)')
    ax3.plot(month,f2m, label='Future2(2061-2100)')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Max Temperature (°C)')
    ax3.set_title('Monthly Max Temperatures')
    # for i, temp in enumerate(hm.values):
    #  ax3.text(hm.index[i], temp, f"{temp:.1f}", ha='center', va='bottom')
    # for i, temp in enumerate(f1m.values):
    #  ax3.text(f1m.index[i], temp, f"{temp:.1f}", ha='center', va='bottom')
    # for i, temp in enumerate(f2m.values):
    #  ax3.text(f2m.index[i], temp, f"{temp:.1f}", ha='center', va='bottom')
    ax3.legend()
    # Set the y-axis interval to 1 unit and show the graph lines
    for ax in [ax2, ax3]:
     ax.yaxis.set_major_locator(plt.MultipleLocator(2))
    #  ax.yaxis.grid(True)
    #  ax.xaxis.grid(True)
    
    
    figs = [fig1, fig2,fig3]

    with PdfPages('static/plots.pdf') as pdf:
        # Save each figure in the PDF
        for fig in figs:
            pdf.savefig(fig)
 