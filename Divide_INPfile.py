# command line - python Divide_INPfile.py [Inp-file name]
# Inp-file - Abaqus inp-file with nodes coordinates, elements and sets 
#
import sys
#
f=open(sys.argv[1])
fn=open("Nodes.inc","w")
fs=open("Sets.inc","w")
#----------------
MaxNode=1
ElemM={}
while True:
	line=f.readline().strip()
	if not line:
		break
	line_l=line.lower()
	if line_l.startswith("*step"):
		break
	elif line_l.startswith("** part"):
		fn.write("** ----------------------------------------------------------------\n")
		fn.write("**\n")
		fn.write(line+"\n")
		fn.write("**\n")
	elif line_l.startswith("**"):
		if FlagElem != "":
			ElemM[FlagElem].append(line)
	elif line_l.startswith("*"):
		FlagSyst=False
		FlagNode=False
		FlagSet=False
		FlagElem=""		
#-----------------Determine of section
		if  line_l.startswith("*system"):
			FlagSyst=True
			fn.write(line+"\n")
		elif  line_l.startswith("*node"):
			FlagNode=True
			fn.write(line+"\n")
		elif  line_l.startswith("*element"):
			start=line.find("type")
			start=line.find("=",start)+1
			end=line.find(",",start)
			if end<0:
			       end=len(line)
			FlagElem=line[start:end].strip()
			if not FlagElem in ElemM:
				ElemM[FlagElem]=[]
		elif line_l.startswith(("*nset","*elset","*surface")):
			FlagSet=True
			fs.write(line+"\n")
	elif FlagSyst:
		fn.write(line+"\n")
	elif FlagNode:
		fn.write(line+"\n")
		TextValue=line.split(",")
		Value=int(TextValue[0])
		if Value>MaxNode:
			MaxNode=Value
	elif FlagElem != "":
		ElemM[FlagElem].append(line)
#		TextValue=line.split(",")
#		Value=[]
#		for i in TextValue:
#		   Value.append(int(i))
#		ElemM[FlagElem].append(Value)
	elif FlagSet:
		fs.write(line+"\n")		
#-------------------------
fs.write("*Nset, nset=NAll, generate\n")
fs.write("1, "+str(MaxNode)+", 1\n")
f.close()
fn.close()
fs.close
for i in list(ElemM):
	f=open("Elements_"+i+".inc", "w")
	for j in ElemM[i]:
		f.write(j+"\n")
	f.close()
