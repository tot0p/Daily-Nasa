import os
import requests
DEL_START  ="<!--NASA-->"
DEL_END    ="<!--/NASA-->"
n = 0
readmefile=open('readme.md','r')
lines = readmefile.readlines()
readmefile.close()
start =-1
end = -1
for line in lines:
    if DEL_START in line:
        start = n
    if DEL_END in line:
        end = n
    n+=1
if start == -1 or end == -1:
    print("Error: Delimiter not found")
    exit(1)
partONe = lines[:start+1]
conttemp = lines[start+1:end]
partTwo = lines[end:]
cont = []
r = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
if r.status_code != 200:
    if r.status_code - 500 < 100:
        print("Error: NASA API is down")
        cont.append("## NASA API is down\n") # because the nasa api is down at this commit
        cont.append("[NASA API REQUEST](https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY)\n")
        cont.append("\n")
        cont.append("[NASA API REPO](https://github.com/nasa/apod-api)\n")
    else:
        print("Error: API request failed")
        exit(1)
else :
    r = r.json()
    cont.append("# "+r['title']+"\n")
    cont.append("## explaination :\n")
    cont.append("\n")
    cont.append(r['explanation']+"\n")
    cont.append("\n")
    cont.append("![NASA]("+r['url']+")\n")

if conttemp == cont:
    print("No new content")
    exit(0)
result = partONe + cont + partTwo
readmefile=open('readme.md','w')
readmefile.writelines(result)
readmefile.close()
os.system('git config --local user.email "github-actions[bot]@users.noreply.github.com"')
os.system('git config --local user.name "github-actions[bot]"')
os.system('git add .')
os.system('git commit -m "nasa picture was added"')
os.system('git push')