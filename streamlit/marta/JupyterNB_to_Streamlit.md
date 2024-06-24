# From Jupyter notebooks to a Streamlit app

**Content:**

1. Code refactoring: whys and hows;
2. Streamlit: website and documenation;
3. Streamlit, an example.

### 1. Code refactoring

Refactoring code is a crucial practice in software development that enhances reusability, readability, and maintainability. When we refactor, we restructure existing code without changing its external behavior, improving its internal structure. This process makes code easier to understand, debug, and extend. In data science, refactoring can transform ad-hoc exploratory code into well-organized, reusable scripts. Exploratory code, often found in Jupyter Notebooks, tends to be quick and dirty, focused on immediate results. Production code, in contrast, is more polished and structured, designed for long-term use and collaboration. Moving from exploratory to production code involves cleaning up, organizing, and modularizing your codebase.

**Identifying Refactoring Opportunities**

Refactoring begins with identifying parts of your code that can be improved. In a typical Jupyter Notebook, you'll encounter common patterns like data loading, data cleaning, visualization, and model training. Often, these tasks are repeated in multiple cells. For example, you might find multiple instances where data is being read from a file and cleaned. These repetitive pieces of code are prime candidates for refactoring into functions. By encapsulating these processes into functions, you can reduce redundancy, simplify your notebook, and make your code more modular and easier to test.

**Creating Python Scripts**

To refactor your Jupyter Notebook code into Python scripts, start by creating a new `.py` file. This file will house your refactored functions. Begin by moving code from your notebook cells into these functions. For instance, if you have code for loading and preprocessing data, you can create functions like `load_data(filepath)` and `preprocess_data(data)`. This not only organizes your code but also makes it reusable across different projects. Ensure that your script is logically organized: separate functions for data loading, preprocessing, and model training. This modular approach enhances clarity and maintainability, making it easier for others (and your future self) to understand and modify your code.

**Best Practices**

When refactoring code into Python scripts, adhere to best practices to ensure high-quality code:

1. **DRY (Don't Repeat Yourself):** Avoid redundancy by ensuring that each piece of knowledge is expressed once and only once in the codebase. If you find yourself writing similar code for data cleaning in multiple places, refactor it into a single function.

```python
# Before refactoring
data1 = data1.dropna()
data2 = data2.dropna()

# After refactoring
def clean_data(data):
    return data.dropna()

data1 = clean_data(data1)
data2 = clean_data(data2)
```

2. **Encapsulation:** Bundle data and methods that operate on the data within a single unit or class to keep them together.For example encapsulate data processing steps in a class.

```python
# Before refactoring
data = pd.read_csv('data.csv')
data = data.dropna()
model = train_model(data)

# After refactoring
class DataProcessor:
    def __init__(self, filepath):
        self.data = pd.read_csv(filepath)

    def preprocess(self):
        self.data = self.data.dropna()

    def get_data(self):
        return self.data

processor = DataProcessor('data.csv')
processor.preprocess()
data = processor.get_data()
model = train_model(data)
```

3. **YAGNI (You Aren't Gonna Need It):** Don't add functionality until it's necessary. Focus on the requirements at hand. Avoid writing code for features that might be needed in the future but aren't required now.

```python
# Before refactoring
def process_data(data, save=False, save_path=None):
    # Process data
    if save:
        save_data(data, save_path)

# After refactoring (assuming saving functionality is not needed yet)
def process_data(data):
    # Process data
```

4. Use **descriptive function names** and docstrings to make your code self-explanatory. For example, `def load_data(filepath):` is much clearer than `def ld(f):`. 
5. **Separate concerns** in your code: keep I/O operations, data processing, and business logic in distinct functions. This separation makes your code more modular and easier to test. 
6. **Avoid hardcoding values** within your functions. Instead, use parameters and arguments to allow for flexibility and reuse. For example, instead of hardcoding a file path, pass it as an argument to your function. 
```python  
#Before refactoring

def load_data():
return pd.read_csv('data.csv')

#After refactoring

def load_data(filepath):
return pd.read_csv(filepath)

data = load_data('data.csv')
```

### 2. Streamlit: website and documentation

Streamlit is an innovative open-source app framework designed to help data scientists and machine learning engineers create beautiful, interactive web applications with ease. One of Streamlit’s key strengths is its simplicity and efficiency, allowing users to build and deploy powerful data-driven apps using pure Python. With Streamlit, there’s no need for extensive front-end development knowledge; a few lines of Python code can create dynamic visualizations and interactive widgets.

### Streamlit Website

The [Streamlit website](https://streamlit.io/) serves as the central hub for everything related to Streamlit. It provides an overview of the framework’s capabilities, showcases use cases, and highlights the community and ecosystem around Streamlit. The website is divided into several key sections:

- **Community:** Here, users can connect with other Streamlit enthusiasts, explore community-created projects, and find inspiration for their own apps. It also includes links to forums and social media groups where users can ask questions and share ideas.
- **Blog:** The blog section contains articles and updates about new features, best practices, and real-world use cases. It's a great resource for staying up-to-date with the latest developments in the Streamlit ecosystem.
- **Gallery:** you can explore various project examples and find inspiration for your own projects. Each project typically includes a link to its GitHub repository, allowing you to review the code and understand how it was implemented.
- **Cloud:** you can deploy your app for free in the cloud.
- **Docs:** In the Streamlit documentation, under the "Develop" section and the "API Reference," you'll find one of the most usefull pages with extensive and detailed documentation along with user examples. This section provides comprehensive descriptions of all available functions and classes, complete with usage examples, parameter explanations, and return values. Additionally, it includes practical examples and sample code to help users understand how to effectively implement and utilize various features of Streamlit in their applications.

**Pros of Streamlit:**

- **Pythonic:** Allows for creating interactive apps using pure Python.
- **Simple to Use:** User-friendly and accessible for those with limited web development experience.
- **Extensive Documentation:** Offers detailed guides, API references, and practical examples.
- **Supportive Community:** Provides ample resources and assistance for users at all levels.
- **Easy Deployment:** Free deployment options available via Streamlit Cloud.

**Cons of Streamlit:**

- **Performance:** Can be slower compared to other frameworks, especially with large datasets or complex interactions.
- **Limited Customization:** Offers less flexibility for custom styling and UI customization.

### 3. Streamlit, an example

- To install streamlit:

`pip install streamlit`

- To check the installation

`streamlit hello`

You should get a streamlit page in your browser.

- Typical folder structure:

A typical folder structure for a repository with a Streamlit app usually includes organized directories for code, data, and other resources. Here is an example of a common folder structure:
```
my_streamlit_app/
├── [app.py](http://app.py/)    # Main Streamlit app script
├── requirements.txt    # Dependencies list
├── [README.md](http://readme.md/)  # Project description and 
instructions
├── .gitignore           # Git ignore file
├── data/                # Directory for datasets
│   ├── data.csv
│   └── ...
├── pages/               # Additional Streamlit app pages (if using multipage setup)
│   ├── [page1.py](http://page1.py/)
│   └── [page2.py](http://page2.py/)
├── utils/               # Utility functions and modules
│   ├── data_processing.py
│   ├── [visualization.py](http://visualization.py/)
│   └── ...
└── assets/              # Static files (images, stylesheets, etc.)
└── logo.png

```
- to run the streamlit app:

`streamlit run app.py`

and the app should be visualized in the browser.