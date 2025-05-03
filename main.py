from setup import ControllerFactory

controller_factory = ControllerFactory()
controller = controller_factory.create_controller()
controller.run()
