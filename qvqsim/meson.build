project('qvqsim', [],
  version : '0.1',
  meson_version : '>=0.55',
  default_options : ['warning_level=2']
)

# Ensure that a Python3 interpreter is available.
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

# Custom target to run the 'doit.sh' script.
# The doit.sh script is expected to:
#   - Execute the simulator and write a log file with an auto-incremented name.
#   - Output the log content (truncated to 25 lines by default or as controlled by the
#     QVSIM_LOGOUT environment variable).
#   - Touch a stamp file (doit.stamp) so Meson can track target completion.
doit_run = custom_target('doit_run',
  command : ['./doit.sh'],
  output  : 'doit.stamp',        # Dummy output file produced by doit.sh (via "touch doit.stamp").
  build_by_default : true,
  build_always_stale: true,      # Use this in place of the deprecated 'build_always'.
  capture : false               # Pass the output directly to the console.
)

# Create an alias target so that running "ninja doit" executes our custom target.
alias_target('doit', doit_run)
