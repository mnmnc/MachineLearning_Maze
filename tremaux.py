from PIL import Image
import random

def create_image(size):
	im = Image.new("RGB", (size, size), color=(255,255,255))
	return im

def save_image(image, filename):
	image.save(filename, "PNG")

def print_graph_as_x_matrix(graph):
	for row in graph:
		for point in row:
			if point == 1:
				print("XX", end="")
			elif point == 0.01:
				print("..", end="")
			elif point == 0.02:
				print("++", end="")
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

def count_neighbours_with_value(graph, cords, value):
	count = 0

	x = cords[0]
	y = cords[1]

	if graph[x-1][y] == 1:
		count += 1
	if graph[x][y-1] == 1:
		count += 1
	if graph[x][y+1] == 1:
		count += 1
	if graph[x+1][y] == 1:
		count += 1

	#print(count)
	return count


def get_available_moves(graph, cords, values_allowed):
	result = []

	x = cords[0]
	y = cords[1]

	if graph[x-1][y] in values_allowed:
		result.append([x-1, y, graph[x-1][y]])
	if graph[x][y-1] in values_allowed:
		result.append([x, y-1, graph[x][y-1]])
	if graph[x][y+1] in values_allowed:
		result.append([x, y+1, graph[x][y+1]])
	if graph[x+1][y] in values_allowed:
		result.append([x+1, y, graph[x+1][y]])

	return result

def draw_graph_on_image(image, graph):

	start_color = (100,100,200)
	end_color = (100,200,100)
	final_path_color = (200,200,100)
	wall_color = (0,0,0)
	dead_end_color = (200,200,200)
	default_color = (255,255,255)

	for i in range(len(graph)):
		for j in range(len(graph[i])):
			if graph[i][j] == 0:
				image.putpixel((i*2,j*2), default_color)
				image.putpixel((i*2+1,j*2), default_color)
				image.putpixel((i*2,j*2+1), default_color)
				image.putpixel((i*2+1,j*2+1), default_color)
			elif graph[i][j] == 0.02:
				image.putpixel((i*2,j*2), dead_end_color)
				image.putpixel((i*2+1,j*2), dead_end_color)
				image.putpixel((i*2,j*2+1), dead_end_color)
				image.putpixel((i*2+1,j*2+1), dead_end_color)
			elif graph[i][j] == 7.02:
				image.putpixel((i*2,j*2), start_color)
				image.putpixel((i*2+1,j*2), start_color)
				image.putpixel((i*2,j*2+1), start_color)
				image.putpixel((i*2+1,j*2+1), start_color)
			elif graph[i][j] == 7.03:
				image.putpixel((i*2,j*2), end_color)
				image.putpixel((i*2+1,j*2), end_color)
				image.putpixel((i*2,j*2+1), end_color)
				image.putpixel((i*2+1,j*2+1), end_color)
			elif graph[i][j] == 0.01:
				image.putpixel((i*2,j*2), final_path_color)
				image.putpixel((i*2+1,j*2), final_path_color)
				image.putpixel((i*2,j*2+1), final_path_color)
				image.putpixel((i*2+1,j*2+1), final_path_color)
			else:
				image.putpixel((i*2,j*2), wall_color)
				image.putpixel((i*2+1,j*2), wall_color)
				image.putpixel((i*2,j*2+1), wall_color)
				image.putpixel((i*2+1,j*2+1), wall_color)

def main():

	# VARIABLES
	input_file = "labirynth_cords.txt"
	output_file = "maze2.png"
	small_input_file = "small_maze.txt"

	# PARSING FILE
	parsed_cords = parse_cords_file(small_input_file)

	# CORRECTING
	biggest = find_biggest(parsed_cords)

	# CREATING EMPTY GRAPH
	graph = create_empty_graph(biggest)

	# SETTING VALUES IN GRAPH BASED ON CORDS
	set_graph_values(graph, parsed_cords)

	# FIXING FRAMES
	graph = fix_graph_frames(graph)

	# PRINT RESULT
	print_graph_as_x_matrix(graph)

	# VARIABLES
	wall_value = 1
	unvisited_value = 0
	visited_once = 0.01
	visited_twice = 0.02
	begin_x = 1
	begin_y = 1
	end_x = 31
	end_y = 31
	begin = (begin_x, begin_y)
	end = (end_x, end_y)
	current_position = (begin[0], begin[1])

	debug_counter = 0
	exit_found = False

	count_neighbours_with_value(graph,current_position, wall_value)


	while debug_counter < 2:
		debug_counter += 1

		print(current_position)

		count = count_neighbours_with_value(graph,current_position, wall_value)
		print("count:", count)

		if current_position == end:
			exit_found = True
			print_graph_as_x_matrix(graph)
			im = create_image(len(graph)*2)
			draw_graph_on_image(im, graph)
			save_image(im, output_file)
			print("exit found")
		elif count > 2 and current_position != begin and current_position != end:
			graph[current_position[0]][current_position[1]] += visited_twice
		else:
			graph[current_position[0]][current_position[1]] += visited_once

		next_moves = get_available_moves(graph,current_position, [unvisited_value, visited_once])

		if len(next_moves) > 1:
			graph[current_position[0]][current_position[1]] = visited_once

		print_graph_as_x_matrix(graph)

		unvisited_paths = []
		visited_paths = []

		for move in next_moves:
			print(move)
		exit_found = True
		# lowest_value = 9
		# selected_moves = []
		# selected_move = []
		# for move in next_moves:
		# 	if move[2] <= lowest_value:
		# 		lowest_value = move[2]
		#
		# equal_moves = 0
		# for move in next_moves:
		# 	if move[2] == lowest_value:
		# 		equal_moves += 1
		#
		# if equal_moves > 1:
		# 	equal_moves_list = []
		# 	for move in next_moves:
		# 		if move[2] == lowest_value:
		# 			equal_moves_list.append(move)
		# 	random_number = random.randint(0, len(equal_moves_list)-1)
		# 	print("Random choice:",  random_number)
		# 	selected_move = equal_moves_list[random_number]


		#current_position = (selected_move[0], selected_move[1])

		#print_graph_as_x_matrix(graph)





if __name__ == "__main__":
	main()