# MVC-GEN

MVC-GEN is a python tool designed to help developers get rid of the initial phase of a backend dev.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

## Usage

1. Edit the config.cfg files and enter the Databse connection details.
2. Edit the demo.yaml file - similar to openAPI - with your own models and parameters. Please pay attention to the identation format.


3. Run it:
```python
python main.py
```

## YAML File
- OpenAPI - identation and structure
- Structure example
``` yaml
openapi: 3.0.3
info:
title: YourTitle  #do not use spaces in name
description: Your Description
version: 1.0.0
models:
	your_model_name:
		id_your_model_name: #the first param needs to be id_[model_name] and has to be the first one in order
			type: int ## type can be: int, string
			autoincrement: True
			primary_key: True
			nullable: False
		user_name:
			type: string
			nullable: False
			default: "'some text here'" #default value has to be inside "" (ex: "3", "'text'", "123") -> string needs also ''
		user_mail:
			type: string
			nullable: False
			unique: True
	second_model:
		id_second_model:
			type: int
			autoincrement: True
			primary_key: True

``` 
###### Also, there is an example file in the folder: demo.yaml

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)