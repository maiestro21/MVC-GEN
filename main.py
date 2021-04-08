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

#### Reading config files ######
config = configparser.RawConfigParser()
config.read('config.cfg')
details_dict = dict(config.items('DATABASE'))

##read demo yaml fle
with open("demo.yaml") as stream:
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
                        print("Exiting")
                    except Exception as e:
                        print(e)
                elif int(type_option) == 2:
                    print("NodeJS")
                elif int(type_option) == 3:
                    print("Flask")


            except mysql.connector.Error as err:
                print(err)
             
                 
                
    except yaml.YAMLError as exc:
        print(exc)

