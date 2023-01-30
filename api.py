from fastapi import FastAPI, HTTPException,Request
import subprocess
from pprint import pprint
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/run-script1/")
async def run_script(request: Request):
    json_data = await request.json()
    print(json_data['text'])
    mydata = json_data['text']
    f = open("text.txt", "w")
    f.write(mydata)
    f.close()

@app.get("/run-script2")
def run_script():
    try:
        result = subprocess.run(["python", "plot_based_movie_recsystem.py", "text.txt"], capture_output=True)
        output = result.stdout.decode()

        # remove the leading "b" and trailing "\" characters
        output = output.strip("b\"")
        output = output.strip("\\r\\n\"")
        output = output.strip("\r\n\"")

        # remove the brackets and quotes from the string and split it into a list
        output = output.strip("[")
        output = output.strip("]")
        output = output.strip("\'")
        output = output.split("\',\'")

        print(output)

        # Return the output as the API response
        return output

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))