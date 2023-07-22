import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_PATH =os.path.join(ROOT_DIR, 'resources')
CONFIG_PATH = os.path.join(RESOURCES_PATH, 'config.json')  # requires `import os`
ENV_VAR_PATH = os.path.join(RESOURCES_PATH,'env.json')
EXAMPLE_INPUTS_PATH = os.path.join(RESOURCES_PATH,"example_inputs")

