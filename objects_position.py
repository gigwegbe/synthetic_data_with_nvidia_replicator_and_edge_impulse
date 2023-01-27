import omni.replicator.core as rep

with rep.new_layer():

    # stage = omni.usd.get_context().get_stage()

    # Load in example asset from S3
    TABLE_USD ="/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_EastRural_Table/EastRural_Table.usd"
    SPOON_SMALL_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Spoon_Small/Spoon_Small.usd"
    SPOON_BIG_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Spoon_Big/Spoon_Big.usd"
    FORK_SMALL_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Fork_Small/Forked_Small.usd"
    FORK_BIG_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Fork_Big/Fork_Big.usd"
    KNIFE_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Knife/Knife.usd"

    cam_position = (-131,200,-134)
    cam_position_random = rep.distribution.uniform((0,181,0), (0, 300, 0))
    cam_rotation = (-90,0,0)
    focus_distance = 120
    focal_length = 11.4
    f_stop = 30
    focus_distance_random = rep.distribution.normal(500.0, 100)

    
    def table():
        table = rep.create.from_usd(TABLE_USD, semantics=[('class', 'table')])

        with table:
            rep.modify.pose(
                position=(-135.39745, 0, -140.25696),
                rotation=(0,-90,-90),
            )
        return table 
    
    def cutlery_props(size=50):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(SPOON_SMALL_USD), size=size, mode='point_instance')
        # instances = rep.randomizer.instantiate(rep.utils.get_usd_files(FORK_BIG_USD, recursive=True), size=size, mode='point_instance') #scene_instance.

        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-212, 76.2, -187), (-62, 76.2, -94)),
                rotation=rep.distribution.uniform((-90,-180, 0), (-90, 180, 0)),
            )
        return instances.node

    # Register randomization 
    rep.randomizer.register(table)
    rep.randomizer.register(cutlery_props)

    # Setup camera and attach it to render product
    camera = rep.create.camera(focus_distance=focus_distance, focal_length=focal_length, position=cam_position, rotation=cam_rotation, f_stop=f_stop)
    render_product  = rep.create.render_product(camera, (1024, 1024))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(output_dir="/home/george/Documents/omniverse_ei/storage", rgb=True, bounding_box_2d_tight=False)
    writer.attach([render_product])

    with rep.trigger.on_frame(num_frames=4):
        rep.randomizer.table()
        rep.randomizer.cutlery_props(70)

    rep.orchestrator.run()


# wget http://omniverse-content-production.s3-us-west-2.amazonaws.com/Materials/vMaterials_2/Wood/Laminate_Oak.mdl