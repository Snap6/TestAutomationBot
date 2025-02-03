import os 
import json 
import ollama 
import streamlit as st

def get_templates(id = 0):
    template_0 = "http://cb-logs-qe.s3-website-us-west-2.amazonaws.com/8.0.0-2476/jenkins_logs/test_suite_executor-TAF/<replacement>/consoleText.txt"
    template_1 = "http://cb-logs-qe.s3-website-us-west-2.amazonaws.com/8.0.0-2476/jenkins_logs/test_suite_executor-TAF/<replacement>/config.xml"
    template_2 = "http://cb-logs-qe.s3-website-us-west-2.amazonaws.com/8.0.0-2476/jenkins_logs/test_suite_executor-TAF/<replacement>/jobinfo.json"
    
    req_template = {
        0: template_0,
        1: template_1,
        2: template_2
    }
    if(id >2): return "Invalid id"
    return req_template[id]

def insert_id_in_url(job_id, id):
    template = get_templates(id)
    if(template == "Invalid id"): return "template not found"
    return template.replace("<replacement>", str(job_id))

def get_ollama_suggestions(job_id):
    print("loading the data")
    # read the data from the json files
    try:
        with open("data/data{}/data{}_0.txt".format(job_id, job_id)) as f:
            data = f.read()
    except:
        print("data not found")
        return
    # get the suggestions from the data
    print(data)
    # check if the data is there or it contains 404 error 
    if "404 Not Found" in data:
        return "Data not found"
    print("evaluating the data")
    response = ollama.chat(model='deepseek-r1:32b', messages=[
        {
        'role': 'user',
        'content': f'for the content below , think about the reasons why the test failed\n{data}, suggest me some fixes for this as well.'
        },
    ],  options={"temperature": 0} )
        
    return response["message"]["content"]

def get_data_from_url(job_id):
    # make a directory to save the data
    os.system("mkdir -p data{}".format(job_id))
    for i in range(0,3):
        url = insert_id_in_url(job_id, i)
        if(url == "template not found"):
            print("Invalid id")
            return 
        # a curl request to get the data from the url
        data_format_to_save = url.split('.')[-1]
        os.system("curl -o data{0}/data{0}_{1}.{2} ".format(job_id,i,data_format_to_save) + url)
    print(get_ollama_suggestions(job_id))


def main():
    while True:
        try: 
            job_id = input("Enter the job id: ")
            if(job_id == 'exit'): break
            get_data_from_url(job_id)
            print("Data is saved in data{}.json".format(job_id))
            print("Do you want to continue? (y/n)")
            if input() == 'n':
                break
        except:
            print("Invalid input")
            continue
    # st.title("Test Execution Data")
    # job_id = st.text_input("Enter the job id: ")
    # if st.button("Get Data"):
    #     get_data_from_url(job_id)
    #     st.write("Data is saved in data{}.json".format(job_id))
    #     # create a box to show the data that is downloaded
        


if __name__ == "__main__":
    main()
