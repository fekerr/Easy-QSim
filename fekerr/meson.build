project('qvqsim', [],
  version : '0.1',
  meson_version : '>=0.55',
  default_options : ['warning_level=2']
)

# Optionally, ensure that a Python3 interpreter is available.
python_dep = dependency('python3', required: true)

# Install Python scripts and configuration files.
install_data(
  'qvqsim.py',
  'qv_simulate.py',
  'input_qvqsim.py',
  'input_json.py',
  'input_yaml.py',
  'output_qvqsim.py',
  'config.toml'
)
