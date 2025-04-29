# meson.build for qvqsim project

project('qvqsim',
  version : '0.1.0',
  license : 'MIT', # Specify your actual license
  default_options : ['warning_level=1'],
  meson_version : '>=0.60.0' # Keep minimum version
)

# --- Python Setup ---
# Find the Python 3 interpreter installation
py_mod = import('python')
# find_installation() usually finds the system python3 by default
py_inst = py_mod.find_installation()

# Check Python version if necessary
# py_inst.check_version('>=3.8', 'Python 3.8 or higher is required.')

# Get Python dependency object
py_dep = py_inst.dependency()

# --- Source Files ---
# List the core Python source files
qvqsim_sources = files(
  'qvqsim.py',
  'qv_simulate.py',
  'input_json.py',
  'input_yaml.py',
  'input_qvqsim.py',
  'output_qvqsim.py'
)

# List the test files
qvqsim_tests = files(
  'test_qvqsim.py'
)

# run_target('qvqsim',
# command : [py_inst, 'qvqsim.py'],
# args : [] # Allows passing arguments like the input file on the command line
# )

run_target('qvqsim',
  command : [py_inst, 'qvqsim.py', '--'] # The '--' helps separate script name from arguments
)
# --- Testing Target ---
# Defines 'meson test'
# Uses Python's unittest module discovery feature
test('unit_tests', py_inst,
  args : ['-m', 'unittest', 'discover', '-s', meson.current_source_dir(), '-p', 'test_*.py'],
  # Set PYTHONPATH using list-of-strings format for env
  env : {} # Or env : [], or just remove the line
)

# --- Documentation Target (Placeholder) ---
# Defines 'meson compile docs'
# Replace echo command with actual Sphinx build command later
docs_target = custom_target('docs',
  command : ['echo', 'Generating documentation (placeholder)'],
  output : 'docs_placeholder.txt', # Dummy output file
  build_by_default : false, # Don't build docs by default
  console : true # Show command output
)

# --- Summary Messages ---
# Display helpful messages after configuration (meson setup builddir)
message('------------------------------------')
message('qvqsim configuration complete.')
message(' ')
message('To run the simulator:')
message('  meson run -C builddir qvqsim <path_to_input_file>')
message('  (Example: meson run -C builddir qvqsim simple_circuit.json)')
message(' ')
message('To run tests:')
message('  meson test -C builddir')
message(' ')
message('To build documentation (placeholder):')
message('  meson compile -C builddir docs')
message('------------------------------------')
