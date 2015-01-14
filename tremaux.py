from PIL import Image
import random
from time import sleep
import time

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


def get_field_count_by_value(graph, value):
	count = 0
	for row in graph:
		for ele in row:
			if ele == value:
				count += 1
	return count

def main():

	# FILE VARIABLES
	input_file = "maze_128x128.txt"
	output_file = "tremaux.png"
	small_input_file = "maze_16x16.txt"

	# PSEUDO-COLORS VALUES
	wall_value = 1
	unvisited_value = 0
	visited_once = 0.01
	visited_twice = 0.02

	# ENTRY AND EXIT
	begin = (1, 1)
	end = (255, 255)

	# OTHER VARIABLES
	iteration = 0
	exit_found = False
	debug = False

	# SET CURRENT POSITION
	current_position = (begin[0], begin[1])

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
	# print_graph_as_x_matrix(graph)

	# CREATING IMAGE OUTPUT
	im = create_image(len(graph)*2)

	start_time = time.time()
	# FINDING PATH
	while exit_found == False:
		iteration += 1

		# CHECK IF MR TREMAUX REACHED THE END
		if current_position == end:
			print("Time spent solving:", time.time() - start_time)
			print("Iterations counted:", iteration)
			print("Path lenght:", get_field_count_by_value(graph, visited_once))
			print("Dead ends lenght:", get_field_count_by_value(graph, visited_twice))
			exit_found = True

			draw_graph_on_image(im, graph)
			save_image(im, output_file)
			break

		# CHECK NUMBER OF WALLS AROUND
		count = count_neighbours_with_value(graph,current_position, wall_value)

		# IF MR TREMAUX HAS ONLY ONE WAY (THE WAY BACK)
		if count > 2 and current_position != begin and current_position != end:
			graph[current_position[0]][current_position[1]] += visited_twice
		else:
			# ELSE, IT'S A NORMAL AFTERNOON WALK
			graph[current_position[0]][current_position[1]] += visited_once

		# GET ALL POSSIBLE MOVES IN NEXT STEP
		next_moves = get_available_moves(graph,current_position, [unvisited_value, visited_once])

		# IF WE ARE ON A CROSSROADS, PREVENT FROM MARKING IT AS DEAD END
		if len(next_moves) > 1:
			graph[current_position[0]][current_position[1]] = visited_once

		# SPLIT NEXT MOVES BASED ON PREVIOUS VISITS
		visited =[]
		unvisited = []
		for move in next_moves:
			if move[2] == unvisited_value:
				unvisited.append(move)
			if move[2] == visited_once:
				visited.append(move)

		# MOVE CHOICE
		# UNVISITED PATHS HAVE HIGHER PRIORITY
		# IF MULTIPLE STEPS ARE AVAILABLE - CHOOSE RANDOMLY
		selected_move = []
		if len(unvisited) > 0:
			if len(unvisited) > 1:
				random_number = random.randint(0, len(unvisited)-1)
				selected_move = unvisited[random_number]
			else:
				selected_move = unvisited[0]
		else:
			if len(visited) > 1:
				random_number = random.randint(0, len(visited)-1)
				selected_move = visited[random_number]
			else:
				selected_move = visited[0]

		# TAKE THE STEP
		current_position = (selected_move[0], selected_move[1])

		# OPTIONAL LIVE UPDATE
		if debug and iteration % 100 == 0:
			try:
				draw_graph_on_image(im, graph)
				save_image(im, output_file)
			except:
				pass


if __name__ == "__main__":
	main()