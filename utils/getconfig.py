import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get():
    if not os.path.isfile('config.yml'):
        with open('config.yml','x+') as file:
            file.write('''---
tokens:
  catch: 

  storage:

  own1: 
  own2: 
  own3: 
  own4: 

your_user_id: 

servers1:
 - 
 - 
 - 
 - 
 - 

servers2:
 - 
 - 
 - 
 - 
 - 

servers3:
 - 
 - 
 - 
 - 
 - 

servers4:
 - 
 - 
 - 
 - 
 - 
''')
        print('\nconfig.yml has been generated. fill it out and run the program again\n')
        quit()
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config