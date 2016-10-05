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
IPATEST_YAML_CONFIG -- the environment variable used by the freeipa integration
tests is used by the dynamic inventory as well. The script simply reads the
data and converts them to the required format.

IPAQE_DYNDIR_CONFIG -- the environment variable specifying the configuration
file when the default configuration in /etc should not be used.
The environment variable allows to pass different configuration
to ansible.

### /etc/ipaqe-dyndir.conf
This is the main configuration file. The file contains options
mostly used in generated metadata.

## Builtin plugin configuration

The dynamic inventory is shipped with two built-in plug-ins that
controll the usage of updates-testing repository and list required
copr repositories.

Each plugin is enabled by a presence of configuration. The name
of the plugin serves as the key in the configuration yaml file.

### updates-testing plugin

The plugin takes single value in the configuration file:


    updates-testing: True

### copr plugin

The plugin takes a list of copr repositories in the configuration file.

    copr:
        - '@freeipa/freeipa-master'
        - pspacek/bind-dyndb-ldap
