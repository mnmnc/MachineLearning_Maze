from PIL import Image
import math

def print_graph_as_x_matrix(graph):
	for row in graph:
		for point in row:
			if point == 1:
				print("XX", end="")
			elif point == 1.01:
				print("--", end="")
			else:
				print("  ",end="")
		print(" ")

def print_graph_special(graph, point_x, point_y):
	for i in range(len(graph)):
		for j in range(len(graph[i])):
			if graph[i][j] == 1:
				print("XX", end="")
			elif i == point_x and j == point_y:
				print("OO", end="")
			else:
				print("  ",end="")
		print(" ")

def parse_cords_file(filename):
	parsed_cords = []
	with open(filename,"r") as input:
		for row in input:
			cords = list(row.split(" "))
			cords_list = [ int(cords[0])*2, int(cords[1])*2, int(cords[2]) ]
			parsed_cords.append(cords_list)
	return parsed_cords

def find_biggest(parsed_cords):
	biggest = -1
	for node in parsed_cords:
		if node[0] > biggest:
			biggest = node[0]
	return biggest

def create_empty_graph(biggest):
	graph = []
	for i in range(biggest+3):
		ys = []
		for i in range(biggest+3):
			ys.append(0)
		graph.append(ys)
	return graph

def set_graph_values(graph, parsed_cords):
	for coord in parsed_cords:
		if coord[2] == 0:
			graph[coord[0]][coord[1]] = 1
			graph[(coord[0])+1][coord[1]] = 1
			graph[coord[0]][coord[1]+1] = 1
		if coord[2] == 1:
			graph[coord[0]][coord[1]] = 1
			graph[coord[0]][coord[1]+1] = 1
		if coord[2] == 2:
			graph[coord[0]][coord[1]] = 1
			graph[coord[0]+1][coord[1]] = 1
		if coord[2] == 3:
			graph[coord[0]][coord[1]] = 1

def fix_graph_frames(graph):
	graph_trans = []
	for i in range(len(graph)):
		xs = []
		for j in range(len(graph[i])):
			xs.append(graph[j][i])
		graph_trans.append(xs)

	for i in range(len(graph_trans)):
		if i == len(graph_trans)-1:
			for j in range(len(graph_trans[i])):
				graph_trans[i][j] = 1
		for j in range(len(graph_trans[i])):
			if j == len(graph_trans[i])-1:
				graph_trans[i][j] = 1

	return graph_trans

def create_image(size):
	im = Image.new("RGB", (size, size), color=(255,255,255))
	return im

def show_image(image):
	image.show()

def save_image(image, filename):
	image.save(filename, "PNG")



def draw_graph_on_image(image, graph):

	start_color = (127,31,25)
	end_color = (127,31,25)
	final_path_color = (127,31,25)
	wall_color = (127,117,116)
	dead_end_color = (255,134,126)
	default_color = (255,255,255)

	for i in range(len(graph)):
		for j in range(len(graph[i])):
			if graph[i][j] == 0:
				image.putpixel((i*2,j*2), default_color)
				image.putpixel((i*2+1,j*2), default_color)
				image.putpixel((i*2,j*2+1), default_color)
				image.putpixel((i*2+1,j*2+1), default_color)
			elif graph[i][j] == 1.01:
				image.putpixel((i*2,j*2), dead_end_color)
				image.putpixel((i*2+1,j*2), dead_end_color)
				image.putpixel((i*2,j*2+1), dead_end_color)
				image.putpixel((i*2+1,j*2+1), dead_end_color)
			elif graph[i][j] == 0.02:
				image.putpixel((i*2,j*2), start_color)
				image.putpixel((i*2+1,j*2), start_color)
				image.putpixel((i*2,j*2+1), start_color)
				image.putpixel((i*2+1,j*2+1), start_color)
			elif graph[i][j] == 0.03:
				image.putpixel((i*2,j*2), end_color)
				image.putpixel((i*2+1,j*2), end_color)
				image.putpixel((i*2,j*2+1), end_color)
				image.putpixel((i*2+1,j*2+1), end_color)
			elif graph[i][j] == 0.04:
				image.putpixel((i*2,j*2), final_path_color)
				image.putpixel((i*2+1,j*2), final_path_color)
				image.putpixel((i*2,j*2+1), final_path_color)
				image.putpixel((i*2+1,j*2+1), final_path_color)
			else:
				image.putpixel((i*2,j*2), wall_color)
				image.putpixel((i*2+1,j*2), wall_color)
				image.putpixel((i*2,j*2+1), wall_color)
				image.putpixel((i*2+1,j*2+1), wall_color)

def dead_end_filler(graph, begin_x, begin_y, end_x, end_y):
	changes = 1
	first_pass = 1
	counter = 0
	while changes != 0 or first_pass == 1:
		first_pass = 0
		changes = 0
		counter+=1
		for i in range(len(graph)):
			for j in range(len(graph[i])):
				if not (i == begin_x and j == begin_y) and not ( i == end_x and j == end_y):
					if graph[i][j] == 0:
						neigh_1 = int(graph[i+1][j])
						neigh_2 = int(graph[i][j+1])
						neigh_3 = int(graph[i-1][j])
						neigh_4 = int(graph[i][j-1])

						sum = neigh_1 + neigh_2 + neigh_3 + neigh_4
						if sum > 2:
							graph[i][j] = 1.01
							changes += 1
				else:
					if i == begin_x and j == begin_y:
						graph[i][j] = 0.02
					if i == end_x and j == end_y:
						graph[i][j] = 0.03
	return graph

def highlight_path(graph):
	for i in range(len(graph)):
		for j in range(len(graph[i])):
			if graph[i][j] == 0:
				graph[i][j] = 0.04

def main():

	# VARIABLES
	input_file = "maze_128x128.txt"
	output_file = "dead_end_filler.png"
	small_input_file = "maze_16x16.txt"


	# PARSING FILE
	parsed_cords = parse_cords_file(input_file)

	# CORRECTING
	biggest = find_biggest(parsed_cords)

	# CREATING EMPTY GRAPH
	graph = create_empty_graph(biggest)

	# SETTING VALUES IN GRAPH BASED ON CORDS
	set_graph_values(graph, parsed_cords)

	# FIXING FRAMES
	graph = fix_graph_frames(graph)

	# PRINT RESULT
	#print_graph_as_x_matrix(graph)

	# CREATING IMAGE
	im = create_image(len(graph)*2)

	# DRAWING EMPTY GRAPH
	# draw_graph_on_image(im, graph)

	# SHOWING GRAPH
	#show_image(im)

	# DEAD END FILLER
	graph = dead_end_filler(graph, 1, 1, 255, 255)
	#graph = dead_end_filler(graph, 1, 1, 31, 31)

	# MARK PATH
	highlight_path(graph)

	# DRAW MAZE
	draw_graph_on_image(im, graph)

	# SAVE IMAGE
	save_image(im, output_file)

if __name__ == "__main__":
	main()