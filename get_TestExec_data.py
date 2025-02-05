import os 
from Suggester import get_ollama_suggestions

def get_templates(id = 0):
    # template_0 = "http://cb-logs-qe.s3-website-us-west-2.amazonaws.com//jenkins_logs/test_suite_executor-TAF/<replacement>/consoleText.txt"
    # template_1 = "http://cb-logs-qe.s3-website-us-west-2.amazonaws.com//jenkins_logs/test_suite_executor-TAF/<replacement>/config.xml"
    # template_2 = "http://cb-logs-qe.s3-website-us-west-2.amazonaws.com//jenkins_logs/test_suite_executor-TAF/<replacement>/jobinfo.json"
    
    template_0 = "http://cb-logs-qe.s3-website-us-west-2.amazonaws.com/<version_id>/jenkins_logs/test_suite_executor-TAF/<replacement>/consoleText.txt"
    template_1 = "http://cb-logs-qe.s3-website-us-west-2.amazonaws.com/<version_id>/jenkins_logs/test_suite_executor-TAF/<replacement>/config.xml"
    template_2 = "http://cb-logs-qe.s3-website-us-west-2.amazonaws.com/<version_id>/jenkins_logs/test_suite_executor-TAF/<replacement>/jobinfo.json"
    
    req_template = {
        0: template_0,
        1: template_1,
        2: template_2
    }
    if(id >2): return "Invalid id"
    return req_template[id]

def insert_id_in_url(job_id, id, version_id = '8.0.0-2476'):
    template = get_templates(id)
    if(template == "Invalid id"): return "template not found"
    template = template.replace("<replacement>", str(job_id))
    template = template.replace("<version_id>", str(version_id))
    return template

def get_data_from_url(job_id,version_id):
    # make a directory to save the data
    os.system("mkdir -p data/data{}".format(job_id))
    for i in range(0,3):
        url = insert_id_in_url(job_id ,i ,version_id)
        if(url == "template not found"):
            print("Invalid id")
            return 
        # a curl request to get the data from the url
        data_format_to_save = url.split('.')[-1]
        print("curl -o data/data{0}/data{0}_{1}.{2} ".format(job_id,i,data_format_to_save) + url)
        os.system("curl -o data/data{0}/data{0}_{1}.{2} ".format(job_id,i,data_format_to_save) + url)

    input_suggest = input("Do you want to get suggestions for the job? (y/n)")
    if input_suggest == 'y':
        get_ollama_suggestions(job_id)
    return


def main():
    while True:
        try: 
            job_id = input("Enter the job id: ")
            if(job_id == 'exit'): break
            change_version = input("Do you want to change the version? (y/n)")
            version_id = '8.0.0-2476'
            if change_version == 'y':
                version_id = input("Enter the version id: ")

            get_data_from_url(job_id,version_id)
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
