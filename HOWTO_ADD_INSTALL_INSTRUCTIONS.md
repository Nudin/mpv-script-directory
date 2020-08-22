# Howto add Install Instructions

To install a plugin automatically with Mplug, there have to be install
instructions in the mpv script directory. To do this, add the following
information to the entry in the file `mpv_script_directory.json`.

Most likely you will find all information on the scripts site.

## Installation method `install`
This is the method, how the plugin should be downloaded and installed.
Currently the only method supported in mplug is `git`.

- `git`: Clone a git repository containing the scripts and create symlinks for
  the relevant files.
- `tar`: Download and unpack a tarball.
- `url`: Download a single file.

# Install source
Specifies the source to obtain the plugin from.

- If `install` is `git` a property called `git` should be set to the cloneable url.
- If `install` is `tar` a property called `script_url` should be set to url of the tarball
- If `install` is `url` a property called `script_url` should be set to url of the script.

# Installation directory or filename
Specifies the name of the folder that contains the downloaded content or the
downloaded file. This is needed so that if multiple plugins share a git repo or
tarball this must not be downloaded multiple times.

- If `install` is `git` the property `gitdir` should specify the name for local
  directory to clone the git repo in. For repositories on github/gitlab/similar
  this should follow the form `github\username\reponame`.

# Files to install
This Specifies which files from the downloaded should be installed where.

- `scriptfiles`: List of files that should be installed in the script folder.
- `scriptoptfiles`: List of files that should be installed in the script-opts folder.
- `shaderfiles`: List of files that should be installed in the shaders folder
- `fontfiles`: List of files that should be installed in the fonts folder
- `executeablefiles`: List of executeable files that should be installed (user
  queried, defaults to `~/bin`).

# Installation notes
If there is anything the user should do or know you can use the field
`install-notes` its text will be displayed after the installation. This is
mainly for cases where some installation steps cannot be done automatically by
mplug.
