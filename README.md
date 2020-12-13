# COD-MW-2019-DNN
Deep Neural Networks for Call Of Duty Modern Warfare 2019  
Contained are the scripts, training data, validation data as well as the .h5 model files for various Call of Duty Modern Warfare Neural Networks  
Train Dataset > 5 GB  
Validation Dataset > 200 MB  

# Enemy Detector
### Intent
Look at a 200x200 pixel block at the center of the uers screen, determine if there is an enemy somewhere in that block. If you have ever played COD, then there is a high chance that by just looking at the below, you would agree if there is an enemy in these images. Realisticly, this is a neural network trained on successfully detecting Gamertags in a 200x200 block.    
![](https://imgur.com/5Fowghj.png) ![Targets](Misc/targets.gif)  
Model Here: https://www.kaggle.com/darkmatter2222/codmw2019dnnmodels?select=CODV7.h5  
Model Here: https://www.kaggle.com/darkmatter2222/codmw2019dnnmodels?select=CODV9.h5  
Training Images: https://www.kaggle.com/darkmatter2222/codmw2019dnnmodels?select=Training+Images  
Validation Images: https://www.kaggle.com/darkmatter2222/codmw2019dnnmodels?select=Validation+Images  


# Head hunter
### Intent
Look at a 200x200 pixel block at the center of the uers screen, break the image into a 10x10 grid of 20x20 in each cell. Clasify what cell the head of the enemy is in, place a crosshair on the head of the enemy. Neutral and Unknown as catch all calssifications (102 classifications total)  
![](https://imgur.com/GtAAOek.png) ![](https://imgur.com/WsqYmmp.png)  
Model Here: https://www.kaggle.com/darkmatter2222/codmw2019dnnmodels?select=MultiClassV2.h5  
Classes Here: https://www.kaggle.com/darkmatter2222/codmw2019dnnmodels?select=Classes.json  


There are some cases in COD, where just loooking at a 200x200 block, its impossible to tell if its friend or foe. Take the scenerio that the user has been flashbanged. The user doesent see the colord indicator above the player.  




So realisticly, this is a neural network trained on successfully detecting Gamertags in a 200x200 block  


### How To Run
1. Clone
2. Download Models listed above.
3. Set up your venv. (Using Tensorflow 2.0)
4. Run https://github.com/darkmatter2222/COD-MW-2019-DNN/blob/master/EnemyDetector/Scripts/Run.py
5. Run COD at full screen (1080p)

If you can run Tensorflow off your GPU, Highly recomend you do so. Its the difference of 2 FPS (i7 3770K) and 12 FPS (GTX 1080 TI). Good instructions here: https://www.tensorflow.org/install/gpu and here https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/

### What does 'EnemyDetector/Scripts/Run.py' do?
Grab the center 200x200 pixel block, and run it through the Neural Network. It will print to the console any time it is > 95% confident that it sees an enemy. 

### What does 'EnemyDetector/Scripts/Overlay.py' do?
Grab the center 200x200 pixel block, and run it through the Neural Network. It will also render a crude transparrent window over COD/Twitch showing you real time values.  
![Sample Gif Here](Misc/SampleOverlay.gif)  
[Sample Video Here](https://youtu.be/Qif8g2Ib5pI)  

### What does 'EnemyDetector/Scripts/NetworkDataCollection.py' do?
This is the "Self Training" Script that runs nearly all day on a server in my basement. It watches Twitch streams of COD in 1080p and grabs screens and stores them by % Confidence into an external 1TB SSD (Sacrificial V-NAND Flash)  
Once a day, I run through and sort the Targets and Neutral Images (takes 20 minutes for 1GB of Data)  
It helps that 99% of the images in the 100% folder are all targets  
I then restart the training with this new data appended to the existing training set. 
![Servers](https://imgur.com/nGzgMBE.png)  

### What does 'EnemyDetector/Scripts/Train.py' do?
This is where the magic happens  
The most simple thing, Pull in a boat load of images from 4 directories (2 train (Neutral and Targets), 2 validation (Neutral and Targets)) and start trainging!  
I provided some validation data zipped up, unzip and run .predict  
**OR**  
Run EnemyDetector/Scripts/Run.py and take one of those Validation images and drag it around on your screen (roughtly center) and watch as the nextwork detects it present.



