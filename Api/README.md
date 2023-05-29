1- miniConda must be installed

2- Create a folder to store the API

3- Create a .py file that will be the code for the website

4- Create a requeriments.txt file with the following content

    gunicorn==19.9.0
    Flask==1.1.1
    numpy==1.20.3
    pandas==1.3.5
    scikit-learn==1.0.2
    streamlit==0.82.0
    
5- Create a folder 'models' to store models and scalers exported from training.

6- Opens the folder location in the miniConda command console (Anaconda Prompt)

7- Enter the following commands:

    7.1- create and activate the environment
    conda create -n siticleta
    conda activate siticleta

    7.2- install dependencies
    conda install python=3.7
    pip install -r requeriments.txt
    pip install protobuf==3.20.*
    pip uninstall flask
    pip install flask
    pip uninstall click
    pip install click==8.0.3
    pip install lightgbm

    7.3- start server
    streamlit run appsiticleta.py


folder view:

    - requeriments.txt
    - appsiticleta.py
    - models (folder --> API_Siticleta.pkl, Escalador.pkl)
