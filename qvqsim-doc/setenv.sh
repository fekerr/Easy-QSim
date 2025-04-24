# setenv.sh - Set environment variables and aliases for qvqsim.
#
# Run this script with 'source setenv.sh' to configure:
#   QVQSIM_SRC : folder for the source, set to your current working directory.
#   QVQSIM_BLD : folder for the build directory (typically ./builddir).
#   ninjaqv   : an alias to run ninja's 'doit' target.

# Set QVQSIM_SRC to the current working directory.
export QVQSIM_SRC=$(pwd)

# Set QVQSIM_BLD to the build directory relative to QVQSIM_SRC.
export QVQSIM_BLD="${QVQSIM_SRC}/builddir"

# Create an alias to run the ninja 'doit' target.
alias ninjaqv="ninja -C \"${QVQSIM_BLD}\" doit"

# lines limit for doit.sh output to console (25 lines = default)
export QVQSIM_LOGOUT=25

# Optional: provide a friendly message confirming that the environment has been set.
echo "qvqsim environment variables set:"
echo "  QVQSIM_SRC = ${QVQSIM_SRC}"
echo "  QVQSIM_BLD = ${QVQSIM_BLD}"
echo "  QVQSIM_LOGOUT = ${QVQSIM_LOGOUT}"
echo "Alias 'ninjaqv' is available to run 'ninja -C ${QVQSIM_BLD} doit'"
