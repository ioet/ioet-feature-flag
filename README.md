# ioet Feature Flags

Feature Flags library to standardize feature toggles across our Internal Apps.
The current implementation is pretty bare-bones and only checks whether the flag is enabled or not.
However, we aim to follow [this standard](https://martinfowler.com/articles/feature-toggles.html) as our framework.

Moreover, we are planning to support [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) as the main feature flag provider. However, we may support other providers in the future.


## Installation
We are currently supporting Python version 3.9 as the minimum version required to install this library, as it is the oldest python version that our Internal Apps use.

We recommend installing this library with [Poetry](https://python-poetry.org/) (you can find more about installing dependencies with poetry [here](https://python-poetry.org/docs/cli/#add)).

To install an specific version (recommended):
```shell
poetry add git+ssh://git@github.com/ioet/ioet-feature-flag.git#<branch-or-tag>
```

To install the latest version:
```shell
poetry add git+ssh://git@github.com/ioet/ioet-feature-flag.git
```

To install an specific version using `pip`:
```
pip install git+ssh://git@github.com/ioet/ioet-feature-flag.git@<branch-or-tag>
```

To install the latest version using `pip`:
```
pip install git+ssh://git@github.com/ioet/ioet-feature-flag.git
```

It is also possible to install with HTTPS instead of SSH by simply replacing `ssh://git@github.com` by `https://github.com`, although we recommend using SSH instead.


## Requirements
In order to be able to use the AWS AppConfig provider, the following environment variables must be set:
```
AWS_APPCONFIG_APP=your-appconfig-app-name
AWS_APPCONFIG_ENV=your-appconfig-environment
AWS_APPCONFIG_PROFILE=your-appconfig-profile
AWS_DEFAULT_REGION=us-east-2
AWS_ACCESS_KEY_ID="your-access-key-id"
AWS_SECRET_ACCESS_KEY="your-access-key"
AWS_SESSION_TOKEN="your-session-token"
```


## Usage

```python
from ioet_json_feature_flag import FeatureRouter

router = FeatureRouter()
router.set_feature_toggle("flag_name", is_flag_enabled=True)

def path_when_enabled():
    pass


def path_when_disabled():
    pass

@router.toggle_point("flag_name")
def client(toggle_point):
    returned_value = toggle_point.toggle(
        path_when_enabled,
        path_when_disabled
    )
```

Once the feature router is declared, you can set flags (or get them from the 
configuration file specified at `file.json`) and then decorate the caller 
function of the desired functionality to get a `toggle_point` parameter, in which the behaviours can be passed. This `toggle_point` will execute the right path according to the flag and return its return value, if any.


## Considerations
- Please note that the current implementation is subject to change.
