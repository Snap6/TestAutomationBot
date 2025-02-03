import ollama

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