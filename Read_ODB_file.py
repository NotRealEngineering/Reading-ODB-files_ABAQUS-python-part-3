#Property of Not Real Engineering 
#Copyright 2020 Not Real Engineering - All Rights Reserved You may not use, 
#           distribute and modify this code without the written permission 
#           from Not Real Engineering.
############################################################################
##             Reading the ODB file                                       ##
############################################################################


from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import random
from array import *
from odbAccess import openOdb
import odbAccess
import math
import numpy    
import os        # Operating system
import shutil    # copying or moving files

Max_iterations=11    # Set number of iterations

#Open text file to write results
sortie = open('Results_fromODB.txt' , 'w')
sortie.write('\t Property of Not Real Engineering')
sortie.write('\n')

isFirstIP = True
Average_Homogenized_E = 0.0

for q in range (1,Max_iterations):
 
    odbname='Job-%d' %(q)        # set odb name here
    path='./'                    # set odb path here (if in working dir no need to change!)
    myodbpath=path+odbname+'.odb'    
    odb=openOdb(myodbpath)

    allIPs = odb.steps['Step-1'].historyRegions.keys()
    
    Total_load = 0.0

    for integrationPoint in allIPs:
                
        if (isFirstIP == True):
            isFirstIP = False
            continue
                    
        tipHistories = odb.steps['Step-1'].historyRegions[integrationPoint]
    
        HistoryOutput_RF2 = tipHistories.historyOutputs['RF2'].data

        def column(matrix, i):
            return [row[i] for row in matrix]
            
            
        RF2_values=column(HistoryOutput_RF2,1)
        Time_values=column(HistoryOutput_RF2,0)
        
        Load = RF2_values[-1]
        
        Total_load += Load
       
    odb.close()
    Displacement = 1.0
    Area = 20.0
    Original_length = 20.0
    
    Stress = -Total_load/Area
    Strain = Displacement/Original_length
        
    Homogenized_E = Stress/Strain
    
    Average_Homogenized_E += Homogenized_E
    
    sortie.write('\n Homogenized Youngs Modulus E from Job-%d is: %f '%(q,Homogenized_E))

    isFirstIP = True

    sortie.write('\n')  
    
Average_Homogenized_E = Average_Homogenized_E/(Max_iterations-1)
sortie.write('\n Averaged Homogenized Youngs Modulus E is: %f '%(Average_Homogenized_E))  
sortie.write('\n')        
sortie.close()    

#Property of Not Real Engineering 
