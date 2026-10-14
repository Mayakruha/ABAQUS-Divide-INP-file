# command line - python Divide_INPfile.py [file name]
# file name - a file with nodes coordinates, elements and sets 
#
import sys
from meshio import read
float_fmt = '.16e'
nnl = 16
#
mesh=read(sys.argv[1])
FileName=sys.argv[1][:sys.argv[1].rfind('.')]
#--------File of Nodes--------
f=open(FileName+'_nodes.inc','w')
f.write("*NODE\n")
fmt = ", ".join(["{}"] + ["{:" + float_fmt + "}"] * mesh.points.shape[1]) + "\n"
for k, x in enumerate(mesh.points):
    if 'Node_Ids' in mesh.point_data:
        f.write(fmt.format(mesh.point_data['Node_Ids'][k], *x))
    else:
        f.write(fmt.format(k + 1, *x))
f.close()	
#---------File of elements--------
files={}
for ic in range(len(mesh.cells)):
    cell_type = mesh.cells[ic].type
    if not cell_type in files:
	    files[cell_type]=open(FileName+'_elms_'+cell_type+'.inc','w')
    node_idcs = mesh.cells[ic].data
    for ir in range(len(node_idcs)):
        row=node_idcs[ir]
        if 'Element_Ids' in mesh.cell_data:
            eid = mesh.cell_data['Element_Ids'][ic][ir]
        else:
            eid += 1
        nums=[str(eid)]
        if 'Node_Ids' in mesh.point_data:
            nids_strs = (str(mesh.point_data['Node_Ids'][nid]) for nid in row.tolist())
        else:
            nids_strs = (str(nid + 1) for nid in row.tolist())
        nums += nids_strs
        files[cell_type].write(",\n".join(",".join(nums[i : i + nnl]) for i in range(0, len(nums), nnl)) + "\n")
for cell_type in files:
    files[cell_type].close() 
#----------File of sets---------------
f=open(FileName+'_sets.inc','w')
offset = 0
for k, v in mesh.cell_sets.items():
    f.write(f"*ELSET, ELSET={k}\n")
    nums=[]
    for ic in range(len(mesh.cells)):
        if len(v[ic]) > 0:
            if 'Element_Ids' in mesh.cell_data:
                for i in v[ic]: nums.append(str(mesh.cell_data['Element_Ids'][ic][i]))
            else:
                for i in v[ic]: nums.append(str(i + 1 + offset))
        offset += len(mesh.cells[ic].data)
    f.write(",\n".join(",".join(nums[i : i + nnl]) for i in range(0, len(nums), nnl)) + "\n")
for k, v in mesh.point_sets.items():
    if 'Node_Ids' in mesh.point_data:
        nums = [str(mesh.point_data['Node_Ids'][i]) for i in v]
    else:
        nums = [str(i + 1) for i in v]
    f.write(f"*NSET, NSET={k}\n")
    f.write(",\n".join(",".join(nums[i : i + nnl]) for i in range(0, len(nums), nnl)) + "\n")
if hasattr(mesh, 'faces'):
    for k, v in mesh.faces.items():
        f.write(f"*SURFACE, TYPE=ELEMENT, NAME={k}\n")
        for face in v:
            f.write(face+','+' S'+str(v[face]+1)+'\n')
f.close()
