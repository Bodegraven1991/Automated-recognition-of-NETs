create a new project ex, complete_detectron2

#set up virtual environment #activate environemnt

python -m venv .detectron2-env
source .detectron2-env/bin/activate

#
pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cu110/torch_stable.html
pip install cython

git clone git@github.com:facebookresearch/detectron2.git
cd detectron2  # will go to detectron 2 folder
pip install -e .

pip install opencv-python
pip install pandas

cd .. # go to complete dectron folder


