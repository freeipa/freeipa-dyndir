# ipaqe-dyndir

ipaqe-dyndir is a simple script that reads the config file
used by freeipa integration test framework and prepares
a dynamic inventory for ansible.

The script implements command `--list` returning an
json formatted information about the whole inventory.
The information includes inventory metadata, thus making
ansible call the script only once.


## Usage

The script is ment to be run by ansible. That means the only argument
available is `--list`. All other options must be passed to the script
either as environment variables or in a configuration file on a known
location.

When run manually, the script offers several other options.
For help message, use the --help option.

### Environment variables
IPATEST_YAML_CONF -- the environment variable used by the freeipa integration
tests is used by the dynamic inventory as well. The script simply reads the
data and converts them to the required format.


### /etc/ipaqe-dyndir.conf
This is the main configuration file. The file contains options
mostly used in generated metadata.
