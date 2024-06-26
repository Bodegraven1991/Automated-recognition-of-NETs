# My Streamlit App
To run this codes, kindly follow the steps outlined below.
## Create a Virtual Environment

1. Open your terminal or command prompt and navigate to your project directory:
> `cd /path/to/your/project`

2. Create the Virtual Environment:
You can create a virtual environment using venv, which is included with Python 3. To create a virtual environment named venv, run:
> `python3 -m venv venv`

This will create a directory named `venv` containing the virtual environment. 
## Activate the Virtual Environment
* If you are using Windows run this on shell:
> `venv\Scripts\activate`

* If you are on mac or linux, run this on your shell:
> `source venv/bin/activate`

After activation, you should see the name of your virtual environment in the terminal prompt, indicating that the virtual environment is active.


## Install Dependencies
1. Ensure pip is Updated:
It’s a good idea to make sure `pip` is up to date:
> `pip install --upgrade pip`

2. Install Dependencies from requirements.txt:
make sure you have a requirements.txt file in your project directory, run:
> `pip install -r requirements.txt`

Once all the requremments are successfully downloaded, you can proceed to run the streamlit app using:
> `streamlit run main.py`

3. Deactivating the Virtual Environment
Once you are done working in the virtual environment, you can deactivate it by running:

> `deactivate`

The end.