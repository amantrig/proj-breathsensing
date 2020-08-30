# Read WAV and MP3 files to array
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
import plotly
from scipy.signal.filter_design import butter, buttord
from scipy.signal import lfilter, hilbert, chirp,find_peaks,filtfilt, find_peaks_cwt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import peakdetect


# read WAV file using scipy.io.wavfile
fs_wav, data_wav = wavfile.read("/home/aman/Proj-healthmask/test60_4s.wav")
print(fs_wav)


# # read MP3 file using pudub
# audiofile = AudioSegment.from_file("data/music_8k.mp3")
# data_mp3 = np.array(audiofile.get_array_of_samples())
# fs_mp3 = audiofile.frame_rate

# print('Sq Error Between mp3 and wav data = {}'.
#       format(((data_mp3 - data_wav)**2).sum()))

print('Signal Duration = {} seconds'.
      format(data_wav.shape[0] / fs_wav))

duration = (data_wav.shape[0] / fs_wav)
print(duration, " Duration")
count_minutes = int(duration/60)
print(count_minutes, " minutes")

data_wav_norm = data_wav
time_wav = np.arange(0, len(data_wav)) / fs_wav
# plotly.offline.plot({"data": [go.Scatter(x=time_wav,
#                                            y=data_wav_norm,
#                                            name='normalized audio signal')]},filename='file.html')


# Applying Low-pass Butter filter
b, a = butter(3, 0.9/(fs_wav*0.5), btype = 'low', analog=False)
filtered = lfilter(b, a, data_wav_norm)
data_wav_lp = filtered
print(len(data_wav_lp), "Length")
data_wav_lp = data_wav_lp/ (2**15)


#Applying hilbert Transformation to get envelope of the signal
analytic_signal = hilbert(data_wav_lp)
amplitude_envelope = np.abs(analytic_signal)
instantaneous_phase = np.unwrap(np.angle(analytic_signal))


#getting Properties of the envelope
peaks, prop = find_peaks(amplitude_envelope,height=0, distance=5000)
peak_graph = prop["peak_heights"]
time_peak = []
max_peak = np.amax(peak_graph)
for i in peaks:
	time_peak.append(time_wav[i])


#normalise as per max amplitude
data_wav_lp =  data_wav_lp/max_peak
amplitude_envelope = amplitude_envelope/max_peak
peak_graph = peak_graph/max_peak

print(np.average(peak_graph), " Numpy Average")
Average_peak = np.average(peak_graph)


max_peak_tmp, min_peak_tmp = peakdetect.peakdet(amplitude_envelope,0.09)
print(len(max_peak_tmp), " Max Peak Count")
print(len(min_peak_tmp), " Min Peak Count")
# print(max_peak_tmp, " max peak tmp value", len(max_peak_tmp))
# print(" Peak Properties ",peak_graph, " length", len(peak_graph))
# print(min_peak_tmp, " min peak tmp value", len(min_peak_tmp))

max_peak_tmp_time = []
max_peak_tmp_value = []
for i in max_peak_tmp:
	max_peak_tmp_time.append(time_wav[int(i[0])])
	max_peak_tmp_value.append(i[1])

min_peak_tmp_time = []
min_peak_tmp_value = []
for i in min_peak_tmp:
	min_peak_tmp_time.append(time_wav[int(i[0])])
	min_peak_tmp_value.append(i[1])	

# plotly.offline.plot({"data": [go.Scatter(x=time_wav,y=data_wav_lp,name='Data Butter Filter')]},filename='file.html')
plotly.offline.plot({"data": [go.Scatter(x=time_wav,y=data_wav_lp,name='Data Butter Filter'), go.Scatter(x=time_wav,y=amplitude_envelope,name='Signal Envelope'),go.Scatter(x=max_peak_tmp_time,y=max_peak_tmp_value,mode='markers',name='Max Peak'),go.Scatter(x=min_peak_tmp_time,y=min_peak_tmp_value,mode='markers',name='Min Peaks')]},filename='file.html')
#plotly.offline.plot({"data": [go.Scatter(x=time_wav,y=amplitude_envelope,name='Signal Envelope'),go.Scatter(x=time_peak,y=peak_graph,mode='markers',name='Signal Envelope')]},filename='file.html')
