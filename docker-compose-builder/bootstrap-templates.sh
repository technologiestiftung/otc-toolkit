#!/usr/bin/env bash
set -eu pipefail
IFS=$'\n\r'

echo "volumes:" > templates/res.yml
/usr/bin/find /usr/lib/aarch64-linux-gnu -name libgstnv* 2> /dev/null | perl -pe 's/(.*)/  - "$1:$1:ro"/' >> templates/res.yml
find /usr/lib/aarch64-linux-gnu -name libgstnv* 2> /dev/null | perl -pe 's/(.*)/  - "$1:$1:ro"/' >> templates/res.yml
find /usr/lib/aarch64-linux-gnu -name libgstbad* 2> /dev/null | perl -pe 's/(.*)/  - "$1:$1:ro"/' >> templates/res.yml
find /usr/lib/aarch64-linux-gnu -name libGL* 2> /dev/null | perl -pe 's/(.*)/  - "$1:$1:ro"/' >> templates/res.yml
find /etc -name *cuda* 2> /dev/null | perl -pe 's/(.*)/  - "$1:$1:ro"/' >> templates/res.yml
find /etc -name *cudnn* 2> /dev/null | perl -pe 's/(.*)/  - "$1:$1:ro"/' >> templates/res.yml
find /etc -name nv* 2> /dev/null | perl -pe 's/(.*)/  - "$1:$1:ro"/' >> templates/res.yml