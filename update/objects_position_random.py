import omni.replicator.core as rep

with rep.new_layer():
    
    # Load in asset
    local_path = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/"
    TABLE_USD =f"{local_path}/asset/Collected_EastRural_Table/EastRural_Table.usd"
    SPOON_SMALL_USD = f"{local_path}/asset/Collected_Spoon_Small/Spoon_Small.usd"
    SPOON_BIG_USD = f"{local_path}/asset/Collected_Spoon_Big/Spoon_Big.usd"
    FORK_SMALL_USD = f"{local_path}/asset/Collected_Fork_Small/Fork_Small.usd"
    FORK_BIG_USD = f"{local_path}/asset/Collected_Fork_Big/Fork_Big.usd"
    KNIFE_USD = f"{local_path}/asset/Collected_Knife/Knife.usd"

    # Camera paramters
    cam_position = (46, 200 , 25) 
    cam_position2 = (46, 120 , 25) 
    cam_position_random = rep.distribution.uniform((0,181,0), (0, 300, 0))
    cam_rotation = (-90,0,0) 
    focus_distance = 114 
    focus_distance2 = 39.1 
    focal_length = 27
    focal_length2 = 18.5
    f_stop = 1.8
    f_stop2 = 1.8
    focus_distance_random = rep.distribution.normal(500.0, 100)

    # Cultery path 
    current_cultery = SPOON_SMALL_USD # Change the item here e.g KNIFE_USD
    output_path = current_cultery.split(".")[0].split("/")[-1]

    def rect_lights(num=1):
        lights = rep.create.light(
            light_type="rect",
            temperature=rep.distribution.normal(6500, 500),
            intensity=rep.distribution.normal(0, 5000),
            position=(45,110,0),
            rotation=(-90,0,0),
            scale=rep.distribution.uniform(50, 100),
            count=num
        )
        return lights.node 
    
    def dome_lights(num=3):
        lights = rep.create.light(
            light_type="dome",
            temperature=rep.distribution.normal(6500, 500),
            intensity=rep.distribution.normal(0, 1000),
            position=(45,120,18),
            rotation=(225,0,0),
            count=num
        )
        return lights.node      

    def table():
        table = rep.create.from_usd(TABLE_USD, semantics=[('class', 'table')])

        with table:
            rep.modify.pose(
                position=(46, -0.0, 20),
                rotation=(0,-90,-90),
            )
        return table 
    
    # Define randomizer function for CULTERY assets. This randomization includes placement and rotation of the assets on the surface.
    def cutlery_props(size=15):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(current_cultery), size=size, mode='point_instance')
      
        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((0, 76.3651, 0), (90, 76.3651, 42)),
                rotation=rep.distribution.uniform((-90,-180, -90), (90, 180, 90)),
            )
        return instances.node

    # Register randomization 
    rep.randomizer.register(table)
    rep.randomizer.register(cutlery_props)
    rep.randomizer.register(rect_lights)
    rep.randomizer.register(dome_lights)

    # Multiple setup cameras and attach it to render products
    camera = rep.create.camera(focus_distance=focus_distance, focal_length=focal_length, position=cam_position, rotation=cam_rotation, f_stop=f_stop)
    camera2 = rep.create.camera(focus_distance=focus_distance2, focal_length=focal_length2, position=cam_position2, rotation=cam_rotation, f_stop=f_stop)

    # Will render 1024x1024 images and 512x512 images
    render_product  = rep.create.render_product(camera, (1024, 1024))
    render_product2  = rep.create.render_product(camera2, (512, 512))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(output_dir=f"{local_path}/data/random/{output_path}", rgb=True, bounding_box_2d_tight=False, semantic_segmentation=False)
    writer.attach([render_product, render_product2])

    with rep.trigger.on_frame(num_frames=25):
        rep.randomizer.table()
        rep.randomizer.rect_lights(1)
        rep.randomizer.dome_lights(1)
        rep.randomizer.cutlery_props(5)

    # Run the simulation graph
    rep.orchestrator.run()

