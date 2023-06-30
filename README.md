# ioet Feature Flags

Feature Flags library to standardize feature toggles across our Internal Apps.
The current implementation is pretty bare-bones and only checks whether the flag is enabled or not.
However, we aim to follow [this standard](https://martinfowler.com/articles/feature-toggles.html) as our framework.

Moreover, we are planning to support [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) as the main feature flag provider. However, we may support other providers in the future.


## Installation
We are currently supporting Python version 3.9 as the minimum version required to install this library, as it is the oldest python version that our Internal Apps use.

We recommend installing this library with [Poetry](https://python-poetry.org/) (you can find more about installing dependencies with poetry [here](https://python-poetry.org/docs/cli/#add)).

To install an specific version (recommended):
```
poetry add poetry add git+ssh://git@github.com/ioet/ioet-feature-flag.git#<branch-or-tag>
```

To install the latest version:
```shell
poetry add poetry add git+ssh://git@github.com/ioet/ioet-feature-flag.git
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


## Usage

```python
import ioet_featureflag

feature_flags = ioet_featureflag.FeatureFlags(
    provider=ioet_featureflag.providers.AWSAppConfigProvider(
        appconfig_app="your_app",
        appconfig_env="your_env",
        appconfig_profile="your_profile",
    )
)

@feature_flags.off("enable_new_feature")
def old_feature():
    pass

@feature_flags.on("enable_new_feature")
def new_feature():
    pass

def client():
    old_feature()
    new_feature()
```

In this example, if the flag `enable_new_feature` is turned on, the `old_feature` function will _not_ get executed, and the `new_feature` function will be executed.

If the flag is off, `old_feature` will be executed and `new_feature` will not.


## Considerations
- Please note that the current implementation is subject to change.
- In order for AWS AppConfig to work, you must set env variables accordingly.
