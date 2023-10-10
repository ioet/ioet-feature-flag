# ioet Feature Flags

Feature Flags library to standardize feature toggles across our Internal Apps.
The current implementation is pretty bare-bones and only checks whether the flag is enabled or not.
However, we aim to follow [this standard](https://martinfowler.com/articles/feature-toggles.html) as our framework.

Moreover, we are planning to support [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) as the main feature flag provider. However, we may support other providers in the future.


## Installation
We are currently supporting Python version 3.9 as the minimum version required to install this library, as it is the oldest python version that our Internal Apps use.

To install with Poetry:
```shell
poetry add git+https://github.com/ioet/ioet-feature-flag.git@<branch-or-tag>
```

To install with `pip`:
```shell
pip install git+https://github.com/ioet/ioet-feature-flag.git@<branch-or-tag>
```

It is also possible to install with SSH instead of HTTPS by simply replacing `https://github.com` by `ssh://git@github.com`.
Example:
```shell
poetry add git+ssh://git@github.com/ioet/ioet-feature-flag.git#<branch-or-tag>
```

If you want to, you can also clone this repository locally and install the library by specifying the folder in which the repo was cloned

```shell
poetry add /path/to/ioet-feature-flag # Absolute path
poetry add ../ioet-feature-flag # Relative path
```

## Requirements

By default, the library attempts to read a file located at `./feature_toggles/feature-toggles.yaml`, so make sure to create a file in that location with the following format:
```
production:
  some_toggle:
    enabled: true
    type: static
staging:
  another_toggle:
    enabled: false
```
The flags are going to be taken from either the `production` or `staging` section depending on the `ENVIRONMENT` env variable.

It is also possible to use other formats or providers, such as JSON or AWS AppConfig, which are documented under the "Providers" section.


## Usage

The library may be used in a object-oriented fashion or a functional one, please check out the examples:
- [OOP usage](./usage_examples/object_oriented_usage.md)
- [Functional usage](./usage_examples/functional_usage.md)

## How to release version to Production
The release process is done locally. Before you start, please make sure you have permission to
do it. Then, follow the steps:
- Place yourself on the version you would like to release (let v0.0.1 be the version example):

```
git checkout v0.0.1-stg
```

- Then, tag it with a production version tag:

```
git tag v0.0.1
```

- Then, push the new release tag:

```
git push origin v0.0.1
```

- Production CI/CD will be triggered.


## Providers

### JSON
It works pretty much the same as the default Yaml provider, with the difference that you have to specify the file location yourself.
```python
provider = ioet_feature_flag.JsonToggleProvider("./your/toggles.json")
toggles = ioet_feature_flag.Toggles(provider=provider)
```

The file format is as it follows:
```
{
  "your_feature": {
    "enabled": true
  },
  "another_feature": {
    "enabled": false,
    "type": "standard"
  }
}
```

### AWS AppConfig

**Setting up AWS AppConfig manually:**
1. Log in to your ioet AWS account: https://ioet.awsapps.com/start/
2. Select your app and click on "Management Console"
3. Search for "AWS AppConfig" and select the first option under the "Services" section
4. Click on "Create Application" and name it as you wish
5. Click on the "Create" button to create a profile. Here, you will need to select either "Feature Flag" or "Freeform Configuration". The difference between the two is the UI within the AWS console. "Feature Flag" is a bit friendlier to use and it's more oriented to managing feature flags. In "Freeform Configuration" you have to modify a JSON file.
6. Once the profile is created, you will be prompted to start creating flags. "Name" is just the name of the feature flag, and "key" is how you will be able to find it in your application. In the case of "Freeform Configuration", the JSON must have this format:
```
{
  "your_feature": {
    "enabled": true
  },
  "another_feature": {
    "enabled": false,
    "type": "standard"
  }
}
```
Currently, we only support one type of feature flag (either enabled or not), so the "type" field won't have any effect. We are going to document the different types of feature flags as we implement them.

7. Once you created your first feature flag, you will need to save the version.
8. After saving the version, you will need to start a deployment in order for the new flags to be available.
9. Keep in mind that the library is environment aware, so in this step, before starting the deployment, make sure to select the right environment.
10. Select the deployment strategy that you want, and just wait for the deployment to be done. You will have to perform a deployment every time you update your flags.

Once the library is installed, in order to be able to use the AWS AppConfig provider, the following environment variables must be set:
```
AWS_APPCONFIG_APP=your-appconfig-app-name
AWS_APPCONFIG_ENV=your-appconfig-environment
AWS_APPCONFIG_PROFILE=your-appconfig-profile
AWS_DEFAULT_REGION=us-east-2
AWS_ACCESS_KEY_ID="your-access-key-id"
AWS_SECRET_ACCESS_KEY="your-access-key"
AWS_SESSION_TOKEN="your-session-token"
```

And lastly, specify the AWS AppConfig provider like so:
```
provider = ioet_feature_flag.AWSAppConfigToggleProvider()
toggles = ioet_feature_flag.Toggles(provider=provider)
```
## Currently supported feature flag types
> Please note that all flags must be under a defined enviroment. The examples on this section show only the structure needed to declare a flag.
### Static flag
This is the most basic type: It toggles a code path on when the flag is `enabled`. The structure for this flag on the YAML file is the following:
```yaml
static-flag-name:
  enabled: true # It can also be false
  type: static
```

### Cutover flag
It toggles a code path on when the flag is `enabled` and it is at or after the **initial datetime** specified for the flag.
```yaml
cutover-flag:
  enabled: true
  type: cutover
  date: 2023-08-20 10:00
```
> **Please note**
> - The datetime format for this flag is `%Y-%m-%d %H:%M`
> - The time specified will be checked against UTC time. 


### Pilot users flag
It enables turning a code path on for a list of **specific users** when the flag is `enabled`. The allowed users must be inserted on a list. The following example shows the flag structure using a user's email:
```yaml
pilot-users-flag:
  enabled: true
  type: pilot_users
  allowed_users:
    - john.doe@email.com
    - jane.doe@email.com
  ```

## Considerations
- Please note that the current implementation is subject to change.
