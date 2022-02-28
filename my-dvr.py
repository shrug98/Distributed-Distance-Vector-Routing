import threading as t
import time
import numpy as np 

nodematrix_outer = dict()
nodenames = ['A','B','C','D','E']
nodestorage = []
my_dict = {'A':0, 'B':1, 'C' :2, 'D':3, 'E':4}

class nodeThread (t.Thread):
   def __init__(self, threadid, threadname,counter,neighbors, matrix):
   
      t.Thread.__init__(self)
      self.threadid = threadid
      self.threadname = threadname
      self.neighbors = neighbors
      self.counter = counter
      self.c_matrix = matrix
      self.curr_matrix = [] 
      #self.current_dv = current_dv(self.threadid, self.neighbors)
      #print(self.threadid)  
      #self.current_dv = current_dv(self.threadid, self.neighbors) 

   def run(self):
      print("Starting " + self.threadname)
      print_time(self.threadname, 3, self.counter)
      print("Exiting " + self.threadname)
      
   def get_current_matrix(self):
      #print('hello') 
      dv_matrix = [] 
       
      for i in range(len(nodestorage)):
        #print(nodestorage) 
        if i != (self.threadid-1):
          curr_matrix = [999]*(len(nodestorage))
          dv_matrix.append(curr_matrix)
        else :
          arr = [999]*(len(nodestorage))
          for i in self.neighbors:
            arr[my_dict[(i[0])]] = int(i[1])  
          dv_matrix.append(arr) 
      for r in range(len(dv_matrix)):
        for c in range(len(dv_matrix[r])):
          if r == c:
            dv_matrix[r][c] = 0 
      self.curr_matrix = dv_matrix
      #np.fill_diagonal(dv_matrix, 0) 
      
  
      
          
     
      return dv_matrix
      
   def updated_matrix(self, matrix, node_sent) :
      sent_row = matrix[my_dict[node_sent.threadname]]
      my_row = matrix[my_dict[self.threadname]]
      value = matrix [my_dict[self.threadname]][my_dict[node_sent.threadname]]
      for i in range(len(sent_row)):
        sum = sent_row[i]+value
        if(sum < my_row[i]) :
            my_row[i] = sum
      matrix[my_dict[self.threadname]] = my_row
      self.curr_matrix = matrix  
      return matrix 
	  
   def set_c_matrix(self, matrix) :
      self.c_matrix = matrix 	
      
      
      
   

def print_time(threadname, counter, delay):
    while counter:
        if counter == 0:
            threadname.exit()
        else:
            time.sleep(delay)
            print("%s: %s" % (threadname, time.ctime(time.time())))
            counter = counter - 1

def read_top():
    with open('network1.txt','r') as f:
        file = f.readlines()
        counter_outer = 0
        for line in file:
            line = " ".join(line.split()).split()
            counter_inner = 0
            nodematrix_inner = dict()
            for num in line:
                nodematrix_inner[nodenames[counter_inner]] = num
                counter_inner = counter_inner + 1
            nodematrix_outer[nodenames[counter_outer]] = nodematrix_inner
            counter_outer = counter_outer + 1
        print(nodematrix_outer)
        return nodematrix_outer

def get_neighbors(nodeChar):
    neighbors = []
    row = nodematrix_outer[nodeChar]
    for i in row:
        if row.get(i)!= '0':
            neighbors.append((i,row.get(i)))
    return neighbors
    

    
def send_message(node_curr, curr_neighbor):
    #print(node_curr.threadname) 
    node_curr_matrix = node_curr.curr_matrix
    for node in nodestorage:
        if curr_neighbor == node.threadname:
            matrix = node.curr_matrix[:]
            #print(matrix[my_dict[node_curr.threadname]]) 
            #print(node_curr_matrix[my_dict[node_curr.threadname]])
            matrix[my_dict[node_curr.threadname]] = node_curr_matrix[my_dict[node_curr.threadname]][:]
            #print(matrix)
            u_matrix = node.updated_matrix(matrix, node_curr)
    #print(u_matrix) 
    return u_matrix
        
    
def matrix_form(matrix) :
	for r in matrix:
		print(str(r) + '\n')
		
def originial_matrix():
	matrix = []
	for r in range(len(nodematrix_outer)):
		 inside_matrix = [999]*(len(nodematrix_outer))
		 matrix.append(inside_matrix)
	for r in range(len(matrix)):
		for c in range(len(matrix[r])):
			if r == c:
				matrix[r][c] = 0 
	return matrix 
	
		 
	 

def network_init():
	matrix = originial_matrix()
	print(np.matrix(matrix)) 
	threadstorage = {}
	threadA = nodeThread(1, "A",1,get_neighbors("A"), matrix)
	threadB = nodeThread(2, "B",1,get_neighbors("B"), matrix)
	threadC = nodeThread(3, "C",1,get_neighbors("C"), matrix)
	threadD = nodeThread(4, "D",1,get_neighbors("D"), matrix)
	threadE = nodeThread(5, "E",1,get_neighbors("E"), matrix)
	nodestorage.extend((threadA,threadB,threadC,threadD,threadE))
	threadA.get_current_matrix() 
	threadB.get_current_matrix() 
	threadC.get_current_matrix() 
	threadD.get_current_matrix() 
	threadE.get_current_matrix() 


def dvr():
	converge = False 
	count = 0 
	while (converge == False) :

		for v,node in enumerate(nodestorage,start=1):
			print("\nRound "+str(v)+" : "+node.threadname)
			#node.get_current_matrix() 
			print("Current DV Matrix = ")
			print(np.matrix(node.curr_matrix))
			print("\n")
			print("Last DV Matrix = ")
			print(np.matrix(node.c_matrix))	
			print("\n")
			print("Updated from last DV matrix or the same? " )
			if(node.curr_matrix == node.c_matrix) :
			  print("Same" + "\n")
			  converge = True 
			else :
			  print("Updated" + "\n") 
			node.set_c_matrix(node.curr_matrix) 			  
			for neighbor in node.neighbors:
				print("Sending DV to Node " + neighbor[0])
				print("Node " + neighbor[0] + " received DV from " + node.threadname)
				print("Updating DV matrix at Node " + neighbor[0]) 
				print("New DV matrix at Node " + neighbor[0] + " = " + "\n")
				print(np.matrix(send_message(node, neighbor[0])));

		count += 1 
		print("--------") 
	print("Final ouput\n")
	for node in nodestorage:
		print("Node "+node.threadname+" DV = " + str(node.curr_matrix[my_dict[node.threadname]]))
		
	print("Number of rounds till convergence (Round # when one of the nodes last updated its DV) = " + str(count))
	print("-------")
     

def run():
    read_top()
    network_init()
    dvr()

run()
