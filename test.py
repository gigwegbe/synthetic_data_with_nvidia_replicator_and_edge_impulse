import omni.replicator.core as rep

#C:/Users/User/Documents/jetson/Jetson nano_fixed_085847/jetson nano_fixed/jetson_nano_v1.usd
with rep.new_layer():
    # PROPS = 'C:/Users/User/Documents/model/unzip/Jetson_041858/jetson/_42_13449_1000_a02_asm.usd'
    TABLE = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Residential/Furniture/DiningSets/EastRural/EastRural_Table.usd"
    # PROPS = "C:/Users/User/Documents/rpi/raspberry_pi_4_model_b.usd"
    # PROPS1 = "C:/Users/User/Documents/wio_terminal/wio_v30.usd"
    PROPS = "C:/Users/User/Documents/Fork/fork.usd"
    PROPS1 = "C:/Users/User/Documents/Spoon/spoon.usd"
    PROPS = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Residential/Kitchen/Kitchenware/Flatware/Spoon_Big.usd"
    PROPS1 = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Residential/Kitchen/Kitchenware/Flatware/Fork_Small.usd"
    
    def get_props(size):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS, recursive=True), size=size, mode='point_instance')
        with instances:
            rep.modify.pose(
                # position=rep.distribution.uniform((-0, 76.3651, -58), (96, 76.3651, 96)),
                position=rep.distribution.uniform((0, 76.3651, 0), (90, 76.3651, 42)),
                # rotation=rep.distribution.uniform((-90, 90, 0), (0, -0, 0)),
                # rotation=rep.distribution.uniform((-90, -0, 0), (-90, -0, 0)), # old 
                 rotation=rep.distribution.uniform((-90, -180, 0), (90, 180, 0)),
                # rotation=rep.distribution.uniform((-90, -0, 0), (-90, -0, 0)),
            )
        return instances.node


    def get_props_rpi(size):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS1, recursive=True), size=size, mode='point_instance')
        with instances:
            rep.modify.pose(
                # position=rep.distribution.uniform((-0, 76.3651, -58), (96, 76.3651, 96)),
                position=rep.distribution.uniform((0, 76.3651, 0), (90, 76.3651, 42)),
                # rotation=rep.distribution.uniform((-90, -0, 0), (-90, -0, 0)),
                rotation=rep.distribution.uniform((-90, -180, 0), (90, 180, 0)),
                #    rotation=rep.distribution.uniform((-90, 90, 0), (0, -0, 0)),
            )
        return instances.node

    def table():
        table = rep.create.from_usd(TABLE, semantics=[('class', 'table')])

        with table:
            rep.modify.pose(
                position=(46, -0.0, 20),
                # rotation=(-90,0,0),
            )
        return table

    rep.randomizer.register(get_props)
    rep.randomizer.register(get_props_rpi)
    rep.randomizer.register(table)

    camera = rep.create.camera(
    position=(46, 120 , 25),
    # position=(46, 120 , 12),
    rotation=(-90, 0, 0),
    # focus_distance=rep.distribution.normal(400.0, 100),
    # focus_distance=30,
    # focal_length=9.0,
    focus_distance=39.1,
    focal_length=18.5,
    f_stop=1.8,
    )


    render_product = rep.create.render_product(camera, resolution=(1024, 1024))
    # Setup randomization
    with rep.trigger.on_frame(num_frames=50):
        rep.randomizer.get_props(3)
        rep.randomizer.get_props_rpi(3)
        rep.randomizer.table()

    writer = rep.WriterRegistry.get("BasicWriter")

    writer.initialize(output_dir="C:/Users/User/Documents/omni_asset/test123", rgb=True, bounding_box_2d_tight=False)

    writer.attach([render_product])

    rep.orchestrator.preview()