import omni.replicator.core as rep

with rep.new_layer():

    stage = omni.usd.get_context().get_stage()

    # Load in example asset from S3
    TABLE_USD ="/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_EastRural_Table/EastRural_Table.usd"
    SPOON_SMALL_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Spoon_Small/Spoon_Small.usd"
    SPOON_BIG_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Spoon_Big/Spoon_Big.usd"
    FORK_SMALL_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Fork_Small/Forked_Small.usd"
    FORK_BIG_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Fork_Big/Fork_Big.usd"
    KNIFE_USD = "/home/george/Documents/synthetic_data_with_nvidia_replicator_and_edge_impulse/asset/Collected_Knife/Knife.usd"

   def spoon_props(size=50):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS), size=size, mode='point_instance')
        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-500, 0, -500), (500, 0, 500)),
                rotation=rep.distribution.uniform((-90,-180, 0), (-90, 180, 0)),
            )
        return instances.node

   def fork_props(size=50):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS), size=size, mode='point_instance')
        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-500, 0, -500), (500, 0, 500)),
                rotation=rep.distribution.uniform((-90,-180, 0), (-90, 180, 0)),
            )
        return instances.node


   def knife_props(size=50):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS), size=size, mode='point_instance')
        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-500, 0, -500), (500, 0, 500)),
                rotation=rep.distribution.uniform((-90,-180, 0), (-90, 180, 0)),
            )
        return instances.node


    def table():
        rep.create.from_usd(TABLE_USD, semantics=[('class', 'table')])

        with table:
            rep.modify.pose(
                # position=(-135.39745, 0, -140.25696),
                position=rep.distribution.uniform((-135.39745, 0, -140.25696),(-135.39745, 0, -140.25696)),
                # rotation=(0,-90,-90)
            )
        return table

    # Register randomization 
    rep.randomizer.register(table)

    # Setkup the static element 
    # table = rep.create.from_usd(TABLE_USD)
    camera = rep.create.camera(focus_distance=500,f_stop=4)
    render_product  = rep.create.render_product(camera, (1024, 1024))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(output_dir="/home/george/Documents/omniverse_ei/storage", rgb=True, bounding_box_2d_tight=False)
    writer.attach([render_product])

    with rep.trigger.on_frame(num_frames=10):
        rep.randomizer.table()
        with camera:
            rep.modify.pose(position=rep.distribution.uniform((-500, 200, -500), (500, 500, 500)), look_at=(0,0,0))

    rep.orchestrator.run()