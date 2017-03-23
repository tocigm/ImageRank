### Setup ENV


conda create --name tf1

source activate tf1

conda install -c conda-forge tensorflow=1.0.0

pip install scipy

pip install Pillow

### data
mkdir data
put the training data to this folder

### run code


python vgg16.py 
