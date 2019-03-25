__author__ = "Anand Krishnan Prakash"
__email__ = "anandkp92@gmail.com"

import argparse
from random import randint
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def create_wall_drawing273(dim, lines_in_wall, wall_num=None):
	mid = dim/2

	wall_dict = {
		1: ['midpoints'],
		2: ['corners'],
		3: ['center'],
		4: ['midpoints', 'corners'],
		5: ['midpoints', 'center'],
		6: ['corners', 'center'],
		7: ['midpoints', 'corners', 'center']
	}

	complete_points_dict = {
		'corners'  : {
			'color': 'blue',
			'coord': [(0,0), (0,dim), (dim,0), (dim,dim)]
		},
		'midpoints': {
			'color': 'red',
			'coord': [(0,mid), (mid,0), (dim,mid), (mid,dim)]
		},
		'center'  : {
			'color': 'yellow',
			'coord': [(mid, mid)]
		}
	}
	
	if not os.path.isdir("paintings"):
		os.mkdir("paintings")

	if wall_num!=None:
		walls = [wall_num]
	else:
		walls = np.arange(1,8,1)
	
	for wall in walls:
		plt.figure(figsize=(20,20))
		plt.grid(True, color='gray', linestyle='--')
		plt.xticks(np.arange(0, dim+1, 1))
		plt.yticks(np.arange(0, dim+1, 1))
		plt.xlim([0, dim+1])
		plt.ylim([0, dim+1])
		
		points_dict = {k: complete_points_dict[k] for k in wall_dict[wall]}
		
		total_num_points = 0
		if 'corners' in points_dict:
			total_num_points += 4
		if 'midpoints' in points_dict:
			total_num_points += 4
		if 'center' in points_dict:
			total_num_points += 1
		max_lines_per_point = lines_in_wall - total_num_points + 1

		current_point_count = 0
		current_line_count = 0
		
		for point_type in points_dict:
			points = points_dict[point_type]['coord']
			color = points_dict[point_type]['color']
			slope_list = []
			for point in points:
				x=[]
				y=[]
				x_point = point[0]
				y_point = point[1]
				points_list=[]
				
				if (lines_in_wall - current_line_count) <= total_num_points-current_point_count:
					lines = 1
				else:
					lines = randint(1, lines_in_wall-current_line_count-(total_num_points-current_point_count))
					
				if total_num_points-current_point_count == 1:
					lines = lines_in_wall-current_line_count
						
				current_line_count+=lines
				current_point_count+=1

				for i in range(2*lines):
					if i%2==0:
						x.append(x_point)
						y.append(y_point)
					else:
						x_coord = randint(0,dim-1)
						y_coord = randint(0,dim-1)
						if x_point == x_coord:
							slope = np.inf
						else:
							slope = round((y_point-y_coord)/(x_point-x_coord), 2)
						while (x_coord, y_coord) in points_list or slope in slope_list:
							x_coord = randint(0,dim-1)
							y_coord = randint(0,dim-1)
							if x_point == x_coord:
								slope = np.inf
							else:
								slope = round((y_point-y_coord)/(x_point-x_coord), 2)
						points_list.append((x_coord, y_coord))
						slope_list.append(slope)
						x.append(x_coord)
						y.append(y_coord)
				df = pd.DataFrame(data={'x':x, 'y':y}, index=np.arange(2*lines))
				plt.plot(df.x, df.y, color=color)
				plt.savefig('paintings/wall%d.png'%wall)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='configure parameters')
	parser.add_argument("-num_lines", help="number of lines in each chart", type=int, default=20, nargs='?')
	parser.add_argument("-size", help="dimension of each chart", type=int, default=10, nargs='?')
	parser.add_argument("-wall_num", help="input a wall number if you want to paint just one wall", type=int, default=None, nargs='?')
	
	try:
		N =  parser.parse_args().size * 2
		lines_per_wall = parser.parse_args().num_lines
		wall_num = parser.parse_args().wall_num
		if wall_num != None:
			if wall_num > 7 or wall_num < 1:
				raise Exception()
	except Exception as e:
		raise Exception("Incorrect arguments")

	create_wall_drawing273(dim=N, lines_in_wall=lines_per_wall, wall_num=wall_num)
	