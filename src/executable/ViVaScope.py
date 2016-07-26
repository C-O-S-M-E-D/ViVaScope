import Prep
import Process
import easygui
import sys

defaultPath = ""
while(1):
	if defaultPath == "":
		path = easygui.fileopenbox(title = "ViVaScope: Choose File" )
	else:
		path = easygui.fileopenbox(title = "ViVaScope: Choose File", default = defaultPath )
		
	if( path == None ):
		sys.exit(1)

	i = len(path)-1
	while( path[i] != "/" ):
		i = i - 1;

	name = path[i+1:]

	defaultPath = path[0:i+1]
	
	total_wells, count, bubbles, resultImg = Prep.launch(path,1000);

	textmsg = "Total Wells: " + str(total_wells) + \
		"\n\nPositive Events: " + str(count)

	easygui.msgbox(msg=name, title="ViVaScope Analysis", ok_button='See Results', image=resultImg, root=None)
	easygui.textbox(msg=name, title="ViVaScope Results", text=textmsg, codebox=0, )
	

