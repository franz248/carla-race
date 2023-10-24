import carla

def main():
	'''Make sure CARLA Simulator 0.9.14 is running'''
	
	# Connect to the CARLA Simulator
	client = carla.Client('localhost', 2000)
	client.set_timeout(20.0)

	# Get the world object
	world = client.get_world()
	world = client.load_world('Town04_Opt')

if __name__ == '__main__':
    main()