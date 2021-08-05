#import modules
import sys
import json
#array initialisation
resources = []
searches = ["$OS$","$CPU$","$RAM$","$HDD$","$TIME$","$IMAGE$"]

#reads in json file of resources needed for VM's
def file_reader():
    #takes input from a command line argument
    #input = sys.argv[1]
    #for testing input
    input = ("centos7")
    #read file into file object
    read_file = open("resources.json","r")
    #convert file into list of dictionaries
    read_json = json.load(read_file)
    read_file.close()
    #loop through each dictionary
    for i in range(len(read_json)):
        #match input to OS tag of current iteration
        if (read_json[i]["$OS$"] == (input)):
            #break when found
            break
    #loop through each json tag
    for j in range(len(searches)):
        #append relevant tags to a list
        resources.append(read_json[i][searches[j]])
    with open("lab_data.json","w") as lab_data:
        json.dump(read_json[i],lab_data,sort_keys=True,indent = 4,ensure_ascii=False)
        
#writes relevant data to terraform file
def file_writer():
    #read terraform file into file object
    write_file = open("replace.tf","r")
    #turns file object into one string
    data = write_file.read()
    write_file.close()
    i = 0
    #for each data tag
    for i in range(len(searches)):
        #go through gile and replace each instance of a tag with the relevant data
        data = data.replace(searches[i],resources[i])
    #reopen file
    write_file = open("replace.tf","w")
    #write the data to the terraform file
    write_file.write(data)
    write_file.close()

    

#run the methods
file_reader()
file_writer()
