import pprint
import os
import json
import uuid
import glob
betweenEvents=20*90
states={}
debug=True
packName="chaos"
def addState(functionName,states,index,totalCount):
    functionName=functionName.replace(".mcfunction","")
    states[functionName]={}
    states["default"]["transitions"].append({functionName:"math.die_roll_integer(1, 0, {})=={}".format(totalCount-1,index)})
    states[functionName]["on_entry"]=["/function {}".format(functionName)]
    states[functionName]["transitions"]=[{"default":"math.mod(query.time_stamp,{})==1".format(betweenEvents)}]

    if debug:
        states[functionName]["on_entry"].append("/say function {}".format(functionName))
controller={}
controller["format_version"]="1.10.0"
controller["animation_controllers"]={}
controller["animation_controllers"]["controller.animation.chaos_ctl"]={}
controller["animation_controllers"]["controller.animation.chaos_ctl"]["initial_state"]= "default"
controller["animation_controllers"]["controller.animation.chaos_ctl"]["states"]=states
states["default"]={"transitions":[]}
functions=list(map(os.path.basename,glob.glob("chaos/functions/*.mcfunction")))
print(functions)

for i in range (len(functions)):
    addState(functions[i],states,i,len(functions))
fileName="{}/animation_controllers/chaos.json".format(packName)
os.makedirs(os.path.dirname(fileName), exist_ok=True)
with open(fileName,"w+") as json_file:
    json.dump(controller,json_file,indent=2)
