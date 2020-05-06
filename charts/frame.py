from tum_base.defines import kValueKeyDate, kValueKeyOpen, \
                        kValueKeyHigh, kValueKeyLow, kValueKeyClose, kValueKeyVolume, \
                        kDataEngineMPLFinance
from .quota import moving_average, stochastics, relative_strength
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np
import random

_random_colors = ['#00B6C1', '#D8BFD8', '#DC143C', '#00F0F5', '#DB7093']

def _GenerateRandomColor(n):
    return random.sample(_random_colors, n)

class Frame(object):
    def __init__(self, data, engine_name, extra_bar=False):
        self.data        = data
        self.data_engine = engine_name
        self.extra_bar   = extra_bar

        self._InitFigureStyle()
        self._TransformMPLStyleData()

    def _TransformMPLStyleData(self):
        self.mpldata     = self.data.loc[:, [
            kValueKeyDate[self.data_engine], 
            kValueKeyOpen[self.data_engine], 
            kValueKeyHigh[self.data_engine], 
            kValueKeyLow[self.data_engine],  
            kValueKeyClose[self.data_engine],
            kValueKeyVolume[self.data_engine]]
            ]
        self.mpldata[kValueKeyDate[self.data_engine]] = \
            pd.to_datetime(self.data[kValueKeyDate[self.data_engine]])
        self.mpldata.columns = [kValueKeyDate[kDataEngineMPLFinance],
                                kValueKeyOpen[kDataEngineMPLFinance],
                                kValueKeyHigh[kDataEngineMPLFinance],
                                kValueKeyLow[kDataEngineMPLFinance],
                                kValueKeyClose[kDataEngineMPLFinance],
                                kValueKeyVolume[kDataEngineMPLFinance]]
        self.mpldata.set_index([kValueKeyDate[kDataEngineMPLFinance]], inplace=True)
        self.mpldata.index.name = kValueKeyDate[kDataEngineMPLFinance]

    def _InitFigureStyle(self):
        maincolor, axcolor = self._ColorStyle()
        self.left, self.width  = 0.1, 0.8
        self.normalfontsize = 9
        self.smallfontsize = 6
        self.ax_ticks = []
        if not self.extra_bar:
            rect1 = [self.left, 0.7, self.width, 0.2]
            rect2 = [self.left, 0.3, self.width, 0.4]
            rect3 = [self.left, 0.1, self.width, 0.2]
            self.figure = plt.figure(facecolor=maincolor) 
            self.ax1    = self.figure.add_axes(rect1, facecolor=axcolor)
            self.ax2    = self.figure.add_axes(rect2, facecolor=axcolor, sharex=self.ax1)
            self.ax3    = self.figure.add_axes(rect3, facecolor=axcolor, sharex=self.ax1)
            self.ax_ticks = [self.ax1, self.ax2, self.ax3]
        else:
            rect1 = [self.left, 0.7, self.width, 0.2]
            rect2 = [self.left, 0.4, self.width, 0.3]
            rect3 = [self.left, 0.2, self.width, 0.2]
            rect4 = [self.left, 0.1, self.width, 0.1]
            self.figure = plt.figure(facecolor=maincolor) 
            self.ax1    = self.figure.add_axes(rect1, facecolor=axcolor)
            self.ax2    = self.figure.add_axes(rect2, facecolor=axcolor, sharex=self.ax1)
            self.ax3    = self.figure.add_axes(rect3, facecolor=axcolor, sharex=self.ax1)
            self.ax4    = self.figure.add_axes(rect4, facecolor=axcolor, sharex=self.ax1)
            self.ax_ticks = [self.ax1, self.ax2, self.ax3, self.ax4]
        register_matplotlib_converters()

    def _ColorStyle(self):
        maincolor = 'white'
        axcolor   = '#f6f6f6'
        return maincolor, axcolor
    
    def _DrawRSI(self, ax, n):
        closes = self.mpldata[kValueKeyClose[kDataEngineMPLFinance]].values.astype('float').tolist()
        rsi = relative_strength(closes, n)
        ax.plot(self.mpldata.index, rsi, color='#a8a8a8')
        ax.axhline(70, color = 'r')
        ax.axhline(30, color = 'g')
        ax.fill_between(self.mpldata.index, rsi, 70,
            where=(rsi >= 70), facecolor='r', edgecolor='r')
        ax.fill_between(self.mpldata.index, rsi, 30,
            where=(rsi <= 30), facecolor='g', edgecolor='g')
        ax.text(0.025, 0.95, 'RSI({circle})'.format(circle=n), va='top',
            transform=ax.transAxes, fontsize=self.normalfontsize)
        ax.text(0.6, 0.9, '> 70 = overbout', va = 'top', 
            transform=ax.transAxes, fontsize=self.normalfontsize)
        ax.text(0.6, 0.1, '< 30 = oversold', 
            transform=ax.transAxes, fontsize=self.normalfontsize)
        ax.set_yticks([30, 70])
        ax.set_ylim(0, 100)

    def _DrawKDJ(self, ax, n):
        closes = self.mpldata[kValueKeyClose[kDataEngineMPLFinance]].values.astype('float').tolist()
        highs  = self.mpldata[kValueKeyHigh[kDataEngineMPLFinance]].values.astype('float').tolist()
        lows   = self.mpldata[kValueKeyLow[kDataEngineMPLFinance]].values.astype('float').tolist()
        kdj = stochastics(highs, lows, closes, n)
        k_line, = ax.plot(self.mpldata.index, kdj['K'], color='#00ff7f', label='K')
        d_line, = ax.plot(self.mpldata.index, kdj['D'], color='#ff7f00', label='D')
        j_line, = ax.plot(self.mpldata.index, kdj['J'], color='#ff0000', label='J')
        ax.set_yticks([30, 70])
        ax.set_ylim(-10, 100)
        ax.text(0.025, 0.95, 'KDJ({circle})'.format(circle=n), va='top',
            transform=ax.transAxes, fontsize=self.normalfontsize)
        ax.legend(handles=[k_line, d_line, j_line], loc='lower center', ncol=3, fontsize=self.smallfontsize)

    def _DrawCandlestick(self, ax, ma = [5, 14, 21]):
        assert len(ma) <= len(_random_colors)
        opens  = self.mpldata[kValueKeyOpen[kDataEngineMPLFinance]].values.astype('float')
        closes = self.mpldata[kValueKeyClose[kDataEngineMPLFinance]].values.astype('float')
        highs  = self.mpldata[kValueKeyHigh[kDataEngineMPLFinance]].values.astype('float')
        lows   = self.mpldata[kValueKeyLow[kDataEngineMPLFinance]].values.astype('float')
        candlestick_ohlc(ax, zip(date2num(self.mpldata.index), opens, highs, lows, closes), width=0.6, colorup='r', colordown='g')
        ax.autoscale_view()

        ma_handles = []
        ma_colors  = _GenerateRandomColor(len(ma))
        for i in range(len(ma)):
            color      = ma_colors[i]
            ma_val     = moving_average(closes, ma[i])
            ma_handle, = ax.plot(self.mpldata.index, ma_val, color=color, label='ma({circle})'.format(circle=ma[i]))
            ma_handles.append(ma_handle)
        ax.legend(handles=ma_handles, loc='best',ncol=len(ma), fontsize=self.smallfontsize)


        axt = ax.twinx()
        volumes = self.mpldata[kValueKeyClose[kDataEngineMPLFinance]].values.astype('float') * \
                  self.mpldata[kValueKeyVolume[kDataEngineMPLFinance]].values.astype('float') / 1e6
        axt.bar(self.mpldata.index, volumes * (closes > opens), width=0.1, label='volume', facecolor='r', edgecolor='r')
        axt.bar(self.mpldata.index, volumes * (closes == opens), width=0.1, label='volume', facecolor='black', edgecolor='black')
        axt.bar(self.mpldata.index, volumes * (closes < opens), width=0.1, label='volume', facecolor='g', edgecolor='g')
        axt.set_ylim(0, 5 * max(volumes))
        axt.set_yticks([])
        self.ax_ticks.append(axt)

    def _DrawExtraQuotas(self, ax, extra_series):
        extra_title   = extra_series['title']
        extra_quotas  = extra_series['content']
        extra_handles = []
        for extra_quota in extra_quotas:
            x, y, name, color = extra_quota['x'], extra_quota['y'], extra_quota['name'], extra_quota['color']
            plot_curve,    = ax.plot(x, y, color=color, label=name)
            extra_handles.append(plot_curve)

        ax.legend(handles=extra_handles, loc='best',ncol=len(extra_handles), fontsize=self.smallfontsize)
        ax.text(0.025, 0.95, extra_title, va='top',
                transform=ax.transAxes, fontsize=self.normalfontsize)


    def Capture(self, offset, capturelen = 30, axtype = {'upper' : 'rsi', 'lower': 'kdj'}, extra_series = {}):
        self._DrawRSI(self.ax1, 14)
        self._DrawCandlestick(self.ax2)
        self._DrawKDJ(self.ax3, 9)
        if(self.extra_bar and extra_series):
            self._DrawExtraQuotas(self.ax4, extra_series)
        for ax in self.ax_ticks:
            if ax != (self.ax4 if self.extra_bar else self.ax3):
                for label in ax.get_xticklabels():
                    label.set_visible(False)
            else:
                for label in ax.get_xticklabels():
                    label.set_rotation(30)
                    label.set_horizontalalignment('right')
            ax.fmt_xdata = DateFormatter('%Y-%m-%d')
        
        plt.show()


