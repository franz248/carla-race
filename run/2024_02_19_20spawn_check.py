import carla, time, queue, shutil, os

def actor_list_destroy(actor_list):
    [x.destroy() for x in actor_list]
    return []

def main():
    '''Make sure CARLA Simulator 0.9.14 is running'''
    actor_list = []
    dir_outptut = '_out_20spawn_check_custom'

    if os.path.exists(dir_outptut):
        shutil.rmtree(dir_outptut)
    os.makedirs(dir_outptut)
    
    try:
        # Connect to the CARLA Simulator
        client = carla.Client('localhost', 2000)
        client.set_timeout(120.0)

        # Get the world object
        world = client.get_world()
        world = client.load_world('Town06_Opt')

        # Set synchronous mode
        settings = world.get_settings()
        settings.synchronous_mode = True # Enables synchronous mode
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        # Define the blueprint of the vehicle you want to spawn
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.find('vehicle.tesla.model3')

        # Now we need to give an initial transform to the vehicle. We choose a
        # random transform from the list of recommended spawn points of the map.
        # print(f'len(world.get_map().get_spawn_points()): {len(world.get_map().get_spawn_points())}')
        # print(f'type(world.get_map().get_spawn_points()): {type(world.get_map().get_spawn_points())}')
        height = 0.1
        spawn_start_left = carla.Transform(carla.Location(x=19.7, y=240.9, z=height), carla.Rotation())
        spawn_start_center = carla.Transform(carla.Location(x=19.7, y=244.4, z=height), carla.Rotation())
        spawn_start_right = carla.Transform(carla.Location(x=19.7, y=247.9, z=height), carla.Rotation())
        spawn_destination = carla.Transform(carla.Location(x=581.2, y=244.6, z=height), carla.Rotation())
        list_spawn = [spawn_start_left, spawn_start_center, spawn_start_right, spawn_destination]

        # for idx_spawn_point in range(len(world.get_map().get_spawn_points())):
        for idx_spawn_point in range(len(list_spawn)):
            transform = list_spawn[idx_spawn_point]

            # So let's tell the world to spawn the vehicle.
            vehicle = world.spawn_actor(vehicle_bp, transform)

            # It is important to note that the actors we create won't be destroyed
            # unless we call their "destroy" function. If we fail to call "destroy"
            # they will stay in the simulation even after we quit the Python script.
            # For that reason, we are storing all the actors we create so we can
            # destroy them afterwards.
            actor_list.append(vehicle)
            # print('created %s' % vehicle.type_id)

            # Let's put the vehicle to drive around.
            vehicle.set_autopilot(False)

            # Let's add now a "depth" camera attached to the vehicle. Note that the
            # transform we give here is now relative to the vehicle.
            camera_bp = blueprint_library.find('sensor.camera.rgb')
            camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
            camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
            actor_list.append(camera)

            # Now we register the function that will be called each time the sensor
            # receives an image. In this example we are saving the image to disk.
            # camera.listen(lambda image: image.save_to_disk('_out/%06d.png' % image.frame, cc))
            # camera.listen(lambda image: image.save_to_disk(f'{dir_outptut}/{idx_spawn_point:03d}_{image.frame:06d}.png'))
            camera.listen(lambda image: image.save_to_disk(f'{dir_outptut}/{idx_spawn_point:03d}_{vehicle.get_location().x:05.1f}_{vehicle.get_location().y:05.1f}_{vehicle.get_location().z:05.1f}.png'))

            world.tick()
            time.sleep(5e-1)
            actor_list = actor_list_destroy(actor_list)
            print(f'spawned {idx_spawn_point+1} of {len(world.get_map().get_spawn_points())}')

    finally:
        actor_list_destroy(actor_list)
        print('done')

if __name__ == '__main__':
    main()