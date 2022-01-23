#  #!/usr/bin python
#  Copyright (c) 2022.  Dave Davis
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      https://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


# Load the country accounts into a dict from the YAML file.
import os

import yaml
from os import environ


def get_settings():
    if environ.get("CHADASA_DEV") is not None:
        with open("./config/settings.dev.yaml", "r") as f:
            settings_file = yaml.load(f, Loader=yaml.SafeLoader)
            selected_settings = dict(settings_file)
    else:
        with open("./config/settings.yaml", "r") as f:
            settings_file = yaml.load(f, Loader=yaml.SafeLoader)
            selected_settings = dict(settings_file)

    return selected_settings
