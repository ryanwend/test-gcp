
# test-gcp

This repo was created to test DevOps Pipelines and how we can automate scripts from Pipelines that interact with GCP. 

The main.py script here is generating a sample parquet file and saving it to a GCP storage bucket. In order to access that storage bucket from the DevOps pipeline a service account had to be created in GCP with proper access, and then a key was generated for that service account. This key is a .json file that is saved as a secret enviromental variable in the DevOps pipeline, in this case called "GOOGLE_APPLICATION_CREDENTIALS".  

That's it! Very simply in concept but getting access and role managment properly configured in GCP was a massive pain point even for this small example. 
