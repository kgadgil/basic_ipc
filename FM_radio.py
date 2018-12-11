#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fm Radio
# Generated: Mon Dec 10 23:46:28 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class FM_radio(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Fm Radio")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1.024e6
        self.noise_amplitude = noise_amplitude = 0.01
        self.mode = mode = 0
        self.decim = decim = 4
        self.audio_gain = audio_gain = 1
        self.WBFM_frequency = WBFM_frequency = 92.3e6
        self.NBFM_frequency = NBFM_frequency = 162.475e6

        ##################################################
        # Blocks
        ##################################################
        self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "FFT Plot")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "Waterfall Plot")
        self.Add(self.notebook_0)
        _noise_amplitude_sizer = wx.BoxSizer(wx.VERTICAL)
        self._noise_amplitude_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_noise_amplitude_sizer,
        	value=self.noise_amplitude,
        	callback=self.set_noise_amplitude,
        	label='noise_amplitude',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._noise_amplitude_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_noise_amplitude_sizer,
        	value=self.noise_amplitude,
        	callback=self.set_noise_amplitude,
        	minimum=0,
        	maximum=0.1,
        	num_steps=500,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_noise_amplitude_sizer, 2, 26, 2, 24)
        self._mode_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.mode,
        	callback=self.set_mode,
        	label='mode',
        	choices=[0,1],
        	labels=['WBFM','NBFM'],
        	style=wx.RA_VERTICAL,
        )
        self.GridAdd(self._mode_chooser, 0, 0, 1, 2)
        _audio_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._audio_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_audio_gain_sizer,
        	value=self.audio_gain,
        	callback=self.set_audio_gain,
        	label='audio_gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._audio_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_audio_gain_sizer,
        	value=self.audio_gain,
        	callback=self.set_audio_gain,
        	minimum=0,
        	maximum=10,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_audio_gain_sizer, 2, 2, 2, 24)
        _WBFM_frequency_sizer = wx.BoxSizer(wx.VERTICAL)
        self._WBFM_frequency_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_WBFM_frequency_sizer,
        	value=self.WBFM_frequency,
        	callback=self.set_WBFM_frequency,
        	label='WBFM_frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._WBFM_frequency_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_WBFM_frequency_sizer,
        	value=self.WBFM_frequency,
        	callback=self.set_WBFM_frequency,
        	minimum=88.1e6,
        	maximum=108.1e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_WBFM_frequency_sizer, 0, 2, 2, 24)
        _NBFM_frequency_sizer = wx.BoxSizer(wx.VERTICAL)
        self._NBFM_frequency_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_NBFM_frequency_sizer,
        	value=self.NBFM_frequency,
        	callback=self.set_NBFM_frequency,
        	label='NBFM_frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._NBFM_frequency_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_NBFM_frequency_sizer,
        	value=self.NBFM_frequency,
        	callback=self.set_NBFM_frequency,
        	minimum=146e6,
        	maximum=170e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_NBFM_frequency_sizer, 0, 26, 2, 24)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.notebook_0.GetPage(1).GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        	size=(480, 360),
        )
        self.notebook_0.GetPage(1).Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.notebook_0.GetPage(0).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate/decim,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        	size=(480, 360),
        )
        self.notebook_0.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=8,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "rtl=0" )
        self.osmosdr_source_0.set_time_source("gpsdo", 0)
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(WBFM_frequency if mode==0 else NBFM_frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(25, 0)
        self.osmosdr_source_0.set_if_gain(24, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((audio_gain, ))
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blks2_selector_1 = grc_blks2.selector(
        	item_size=gr.sizeof_float*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=mode,
        	output_index=0,
        )
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=1,
        	num_outputs=2,
        	input_index=0,
        	output_index=mode,
        )
        self.audio_sink_0 = audio.sink(32000, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=256e3,
        	audio_decimation=8,
        )
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise_amplitude, 0)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=32000,
        	quad_rate=32000,
        	tau=75e-6,
        	max_dev=5e3,
          )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blks2_selector_1, 1))    
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.blks2_selector_1, 0))    
        self.connect((self.blks2_selector_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.blks2_selector_0, 1), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.blks2_selector_1, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.blks2_selector_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.wxgui_waterfallsink2_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_nbfm_rx_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate/self.decim)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)

    def get_noise_amplitude(self):
        return self.noise_amplitude

    def set_noise_amplitude(self, noise_amplitude):
        self.noise_amplitude = noise_amplitude
        self.analog_noise_source_x_0.set_amplitude(self.noise_amplitude)
        self._noise_amplitude_slider.set_value(self.noise_amplitude)
        self._noise_amplitude_text_box.set_value(self.noise_amplitude)

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
        self.blks2_selector_0.set_output_index(int(self.mode))
        self.blks2_selector_1.set_input_index(int(self.mode))
        self.osmosdr_source_0.set_center_freq(self.WBFM_frequency if self.mode==0 else self.NBFM_frequency, 0)
        self._mode_chooser.set_value(self.mode)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate/self.decim)

    def get_audio_gain(self):
        return self.audio_gain

    def set_audio_gain(self, audio_gain):
        self.audio_gain = audio_gain
        self.blocks_multiply_const_vxx_0.set_k((self.audio_gain, ))
        self._audio_gain_slider.set_value(self.audio_gain)
        self._audio_gain_text_box.set_value(self.audio_gain)

    def get_WBFM_frequency(self):
        return self.WBFM_frequency

    def set_WBFM_frequency(self, WBFM_frequency):
        self.WBFM_frequency = WBFM_frequency
        self.osmosdr_source_0.set_center_freq(self.WBFM_frequency if self.mode==0 else self.NBFM_frequency, 0)
        self._WBFM_frequency_slider.set_value(self.WBFM_frequency)
        self._WBFM_frequency_text_box.set_value(self.WBFM_frequency)

    def get_NBFM_frequency(self):
        return self.NBFM_frequency

    def set_NBFM_frequency(self, NBFM_frequency):
        self.NBFM_frequency = NBFM_frequency
        self.osmosdr_source_0.set_center_freq(self.WBFM_frequency if self.mode==0 else self.NBFM_frequency, 0)
        self._NBFM_frequency_slider.set_value(self.NBFM_frequency)
        self._NBFM_frequency_text_box.set_value(self.NBFM_frequency)


def main(top_block_cls=FM_radio, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
