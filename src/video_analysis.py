########################################################
#
#  attualmente 1BecNByKUqYJJo1VwM01C2DeFIwokD6ab contiene solo 2 video.... quindi non è il massimo
#
########################################################






import os
import numpy as np
import matplotlib.pyplot as plt
import openface
import openface.parts as parts
from gdrive import GoogleDriveDownloader as gdd

DIR = '../test_data/fake_vs_real'

########## DEFINE COLUMNS TO CHECK

AU = ['AU01_c']
COLS = AU

######## Create Directory & Download Videos

os.system(f'mkdir -d {DIR}')
gdd.download_file_from_google_drive(file_id='1BecNByKUqYJJo1VwM01C2DeFIwokD6ab',    # my GDrive
                                    dest_path=DIR+'/data.zip',
                                    unzip=True)


######## Analysis of the Videos

api = openface.OpenFaceAPI()
results = {}
subfold = os.listdir(DIR)

# results['fake']['obama_vid.mp4'] = DataExtractor(out_dir+obama_vid)
for s in subfold:
    results[s] = api.process_video(fdir=f'{DIR}/{s}', vtype='single')



######## Extract Graphs to Extract Best Features

avgs = {}
for s in subfold:
    avgs[s] = []
    for _, extractor in results[s].items():
        extractor = extractor.get_confidence(0.75).get_features(parts.AU)
        avgs[s].append(extractor.get_frame_avg())




def norm(X, mean, std):
    if std == 0:
        std = 0.1
    num =  np.exp(((X-mean)/std)**(1/2)/-2)
    denom = std*2.5066282
    return num/denom




######## Plot Results

NUM_OF_ROWS = 5
l = len(parts.AU)//NUM_OF_ROWS+1
fig, axs = plt.subplots(NUM_OF_ROWS,l)

for i, au in enumerate(parts.AU):
    a, b = i//l, i-(i//l)*l
    axs[a, b].set_title(au)
    for s, color in zip(subfold, ['red','blue','y','g']):
        values = np.array([x[i] for x in avgs[s]])
        mu, sigma = values.mean(), values.std()
        x = np.linspace(0,1, 100)
        y = norm(x, mu, sigma)
        print(x)
        print(y)
        print('--')
        axs[a, b].plot(x, y, f'tab:{color}')



for ax in axs.flat:
    ax.set(xlabel='fake vs real', ylabel='pd')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.show()
print(f'-----> RED = {subfold[0]}')