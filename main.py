#!/usr/bin/python
import os
import configparser
import yaml
import json
import mysql.connector
from pprint import pprint
import shutil

type_option = 0


## Show menu ##
def show_main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print (30 * '-')
    print ("   M A I N - M E N U")
    print (30 * '-')
    print ("1. Generate PHP/CI3 3.1.11")
    print ("2. Generate NodeJS")
    print ("3. Generate Flask")
    print ("4. Train Model")
    print ("9. Exit")
    print (30 * '-')
    await_choice_main()

def await_choice_main():
    global type_option
    choice = input('Enter your choice [1-4] : ')
    choice = int(choice)
    if choice == 1:
            type_option = 1
    elif choice == 2:
            type_option = 2
    elif choice == 3:
            type_option = 3
    elif choice == 4:
            print("Model Training not implemented at this stage")
            quit()
    elif choice == 9:
            print ("Exiting ---------")
            quit()
    else:    ## default ##
            show_main_menu()




show_main_menu()
query = ""
#### Reading config files ######
config = configparser.RawConfigParser()
config.read('config.cfg')
details_dict = dict(config.items('DATABASE'))

##read demo yaml fle
file_yaml = input("Name of the YAML file [demo.yaml]:")
if file_yaml == "":
    file_yaml = "demo.yaml"
with open(file_yaml) as stream:
    try:
        yml_data = (yaml.safe_load(stream))
        if len(yml_data["models"]) < 1:
            print("The file does not contain minimum of 1 model.")
            quit()
        else:
            ##databse connection
            try:

                cnx = mysql.connector.connect(host=details_dict['host'],password=details_dict['password'],user=details_dict['user'],database=details_dict['database'])
                print("Connected to database success!")

                cursor = cnx.cursor(dictionary=True)
                
                #print(cursor.fetchall())

                ### DATABASE CREATION ####
                for model in yml_data["models"]:
                    query = "CREATE TABLE %s (" % (model)
                    for elem in yml_data["models"][model]:
                        for test in yml_data["models"][model][elem]:

                            elem_type = ""
                            elem_null = ""
                            elem_autoincrement = ""
                            elem_primary_key = ""
                            elem_unique = ""
                            elem_default = ""

                            if yml_data["models"][model][elem]['type'] == "int":
                                elem_type = "int"
                            elif yml_data["models"][model][elem]['type'] == "string":
                                elem_type = "varchar(255)"
                            else:
                                elem_type = "varchar(255)"
                            

                            if yml_data["models"][model][elem]['nullable'] == False:
                                elem_null = "NOT NULL"
                            else:
                                elem_null = ""

                            try:
                                if yml_data["models"][model][elem]['autoincrement'] == True:
                                    elem_autoincrement = "AUTO_INCREMENT"
                                else:
                                    elem_autoincrement = ""
                            except Exception as e:
                                pass

                            try:
                                if yml_data["models"][model][elem]['primary_key'] == True:
                                    elem_primary_key = "PRIMARY KEY"
                                else:
                                    elem_primary_key = ""
                            except Exception as e:
                                pass

                            try:
                                if yml_data["models"][model][elem]['unique'] == True:
                                    elem_unique = "UNIQUE"
                                else:
                                    elem_unique = ""
                            except Exception as e:
                                pass

                            try:
                                if yml_data["models"][model][elem]['default']:
                                    elem_default = "DEFAULT " + yml_data["models"][model][elem]['default']
                                else:
                                    elem_default = ""
                            except Exception as e:
                                pass
                            
                        
                        subquery = "%s %s %s %s %s %s %s," % (elem, elem_type, elem_null, elem_autoincrement, elem_primary_key, elem_unique, elem_default)
                        query = query + subquery
                    
                    query = query[:-1] + ");"
                    ### CFREATE THE TABLES ###
                    try:
                        query = cursor.execute(query)
                        myresult = cursor.fetchall()
                        print("-------------------------------")
                        print("###    Database generated .....")
                        print("-------------------------------")
                    except Exception as e:
                        print(e)
         
                cnx.close()

                   #######     CODEIGNITER 3.x   ######
                if int(type_option) == 1:
                    print("-------------------------------")
                    print("### CI3 3.1.11 Generating Files")
                    print("-------------------------------")

                    if os.path.isdir("outputs/"+yml_data["info"]["title"]) == True:
                        print("!! Project path already exists. Cannot override !!")
                        print("-------------------------------")
                        print("--> Exiting")
                        quit()
                    try:
                        shutil.copytree("sources/codeigniter", "outputs/"+yml_data["info"]["title"])  
                        project_path = "outputs/"+yml_data["info"]["title"]

                        ##WRITE DB CONFIGS###
                        f = open(project_path+"/application/config/database.php",'r')
                        filedata = f.read()
                        f.close()
                        newdata = filedata.replace("@@host@@",details_dict['host'])
                        newdata = newdata.replace("@@username@@",details_dict['user'])
                        newdata = newdata.replace("@@password@@",details_dict['password'])
                        newdata = newdata.replace("@@database@@",details_dict['database'])
                        f = open(project_path+"/application/config/database.php",'w')
                        f.write(newdata)
                        f.close()
                        ###---------###
                        ##WRITE GENERAL CONFIGS###
                        base_url = input("Provide base url [http://127.0.0.1/]:")
                        if base_url == "":
                            base_url = "http://127.0.0.1/"
                        f = open(project_path+"/application/config/config.php",'r')
                        filedata = f.read()
                        f.close()
                        newdata = filedata.replace("@@base_url@@",base_url)
                        f = open(project_path+"/application/config/config.php",'w')
                        f.write(newdata)
                        f.close()
                        ###---###
                        print("")
                        ##WRITE MVC ###
                        for model in yml_data["models"]:
                            modelC = model.capitalize()
                            print(modelC)
                            ### CONTROLLER ###
                            f = open(project_path+"/generator_templates/Controller_template.php",'r')
                            filedata = f.read()
                            f.close()
                            newdata = filedata.replace("@@controller_name@@",model)
                            newdata = newdata.replace("@@controller_name_capitalize@@",modelC)
                            newdata = newdata.replace("@@view_name@@",model+"_view.php")
                            f = open(project_path+"/application/controllers/"+modelC+".php",'w')
                            f.write(newdata)
                            f.close()
                            ### MODEL ####
                            f = open(project_path+"/generator_templates/Model_template.php",'r')
                            filedata = f.read()
                            f.close()
                            newdata = filedata.replace("@@controller_name@@",model)
                            newdata = newdata.replace("@@controller_name_capitalize@@",modelC)
                            newdata = newdata.replace("@@id_field@@","id_"+model)
                            f = open(project_path+"/application/models/"+modelC+"_model.php",'w')
                            f.write(newdata)
                            f.close()
                            ##---###
                            ### VIEW ####
                            f = open(project_path+"/generator_templates/view_template.php",'r')
                            filedata = f.read()
                            f.close()
                            newdata = filedata.replace("@@title@@",modelC)
                            f = open(project_path+"/application/views/"+model+"_view.php",'w')
                            f.write(newdata)
                            f.close()
                            ##---###
                        print("-------------------------------")
                        print("          MVC generated       ")
                        print("-------------------------------")
                        
                        

                    except Exception as e:
                        print(e)

                elif int(type_option) == 2:
                    print("-------------------------------")
                    print("### NodeJS 3.1.11 Generating Files")
                    print("-------------------------------")
                    # try:
                    #     shutil.copytree("sources/codeigniter", "outputs/"+yml_data["info"]["title"])  
                    #     project_path = "outputs/"+yml_data["info"]["title"]
                    # except Exception as e:
                    #     print(e)

                elif int(type_option) == 3:
                    print("Flask")


                #########################################
                ##### END OF DIFFERENT LANGUAGES #####
                ######
                ###
                ##
                #
                project_path = "outputs/"+yml_data["info"]["title"]

                #### GENERATE SQL FILE  ###
                file_sql = open(project_path+"/sql_generate.sql", "a")
                file_sql.write(query)
                file_sql.close()
                print("-------------------------------")
                print("###  sql_generated.sql #### ")
                print("-------------------------------")

                ##WRITING THE SWAGGER FILE FOR ACCESS##
                #### SWAGGER GENERATOR ####
                try:
                    f = open(project_path+"/generator_templates/swagger_templates/baseline.yaml",'r')
                    baseline = f.read()
                    f.close()
                    baseline = baseline.replace("@@title@@",yml_data["info"]["title"])
                    baseline = baseline.replace("@@base_url@@",base_url)

                    f = open(project_path+"/generator_templates/swagger_templates/element.yaml",'r')
                    element_stock = f.read()
                    f.close()
                    element_final = ""

                    
                    f = open(project_path+"/generator_templates/swagger_templates/element_definitions.yaml",'r')
                    elem_definitions_stock = f.read()
                    f.close()
                    definitions = "definitions:\n"

                    ##Elem prop
                    f = open(project_path+"/generator_templates/swagger_templates/element_properties.yaml",'r')
                    elem_prop_stock = f.read()
                    f.close()

                        
                    for model in yml_data["models"]:
                        
                        element_aux = element_stock
                        element_aux = element_aux.replace("@@controller_name@@",model)
                        elem_definitions = elem_definitions_stock
                        elem_definitions = elem_definitions.replace("@@controller_name@@",model)
                        prop_final = ""

                        for prop in yml_data["models"][model]:
                            strcomp = "id_"+model
                            if prop != strcomp:##removing the first param: ID.
                                param_aux = elem_prop_stock
                                param_aux = param_aux.replace("@@prop_name@@",prop)
                                if(yml_data["models"][model][prop]["type"] == "int"):
                                    param_aux = param_aux.replace("@@prop_type@@","integer")
                                else:
                                    param_aux = param_aux.replace("@@prop_type@@",yml_data["models"][model][prop]["type"])
                                # if yml_data["models"][model][prop]["nullable"] == False:
                                #     param_aux = param_aux.replace("@@required_param@@","true")
                                # else:
                                #     param_aux = param_aux.replace("@@required_param@@","false")
                                prop_final = prop_final + param_aux + "\n"
                            
                        elem_definitions = elem_definitions.replace("@@element_properties@@",prop_final)
                        
                        definitions = definitions + elem_definitions + "\n"
                        element_final = element_final + element_aux + "\n"
                        
                    
                    f = open(project_path+"/swagger/swagger-generated.yaml",'w')
                    f.write(baseline + "\n" + element_final + "\n" + definitions)
                    f.close()
                    f = open("outputs/"+yml_data["info"]["title"]+"/swagger/index.html",'r')
                    filedata = f.read()
                    f.close()
                    newdata = filedata.replace("@@base_url@@",base_url)
                    f = open("outputs/"+yml_data["info"]["title"]+"/swagger/index.html",'w')
                    f.write(newdata)
                    f.close()
                    ###---###
                except Exception as e:
                    print(e)

                ###DELETING TEMPLATES FOLDER ####
                shutil.rmtree(project_path + "/generator_templates")
                #####
                print("-------------------------------")
                print("###  Swagger generated  #### ")
                print("-------------------------------")


                print("-> Exiting...")

            except mysql.connector.Error as err:
                print(err)
             
                 
                
    except yaml.YAMLError as exc:
        print(exc)

