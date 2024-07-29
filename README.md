# ioet Feature Flags

Feature Flags library to standardize feature toggles across our Internal Apps.
We are aim to follow [this standard](https://martinfowler.com/articles/feature-toggles.html) as our framework.

The default provider that we support is a Yaml or Json file hosted in the project's repo.
However, we also support other providers such as [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html). We may support other providers in the future.

The supported providers are listed in the [Providers](#providers) section.


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

**IMPORTANT NOTE**: There's a fair chance that you have CI/CD pipelines in your project. Please make sure that they have the `git` command available before including this library in your project. Otherwise your pipelines **will fail**.

## Requirements

Create a yaml file. It can be located anywhere you want, for example, at `./feature_toggles/feature-toggles.yaml`. Make sure that it has the following format:
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

It is also possible to specify a different file location, or use other formats or providers, such as JSON or AWS AppConfig. This is documented in the [Providers](#providers) section.


## Backend Usage

The library may be used in an object-oriented fashion or a functional one, please check out the examples:
- [OOP usage](./usage_examples/object_oriented_usage.md)
- [Functional usage](./usage_examples/functional_usage.md)

## Frontend usage
We also support a couple of React hooks to make use of the feature flags in the frontend.
You will need to create an endpoint that retrieves all the flags, and install the [ioet-ui-library](https://github.com/ioet/ioet-ui-library) library.
This is documented on the [Frontend Usage Guide](./usage_examples/frontend_usage.md) page.

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
  "development": {
    "your_feature": {
      "enabled": true
    },
    "another_feature": {
      "enabled": false,
      "type": "standard"
    }
  }
}
```

`"development"` comes from the `ENVIRONMENT` env variable. If you desire to use another env variable to specify which environment to use, you can specify the `environment` parameter, like so:
```
provider = ioet_feature_flag.JsonToggleProvider(
  toggles_file_path="./your/toggles.json",
  environment=os.getenv("OTHER_ENV_VARIABLE")
)
```

### Remote Git providers

We have two remote git providers: `JsonGitRemoteProvider` and `YamlGitRemoteProvider`. The only difference between them is just the file format and extension that they expect to read.

Unless you are using a public git repository, you must generate a Github token and export it in an env variable.
You can follow the instructions [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) to generate one.
**Make sure to give it all the `repo` permissions and the `read:org` permission**.

Once you have your token ready, you can initialize it like so:
```python
provider = ioet_feature_flag.YamlGitRemoteProvider(
  environment="prod",
  project_id="your-app-name",
  token=os.getenv("GITHUB_TOKEN"),
)
toggles = ioet_feature_flag.Toggles(provider=provider)
```
The default `base_url` parameter is `https://raw.githubusercontent.com/ioet/feature-flag-repository/main/`, but you can specify another one if you wish.

Another optional parameter is `cache_ttl_seconds`, which defines how often the provider is allowed to perform an HTTP request to fetch the feature flags file.
By default it has a value of `300` seconds (5 minutes).

The effective URL is going to resolve to `https://raw.githubusercontent.com/ioet/feature-flag-repository/main/{project_id}/{environment}.yaml`.

We are going to have more details about the format and structure of the files in the `ioet/feature-flag-repository` repo.

### AWS AppConfig

**Setting up AWS AppConfig manually:**
1. Log in to your ioet AWS account: https://ioet.awsapps.com/start/
2. Select your app and click on "Management Console"
3. Search for "AWS AppConfig" and select the first option under the "Services" section
4. Click on "Create Application" and name it as you wish
5. Click on the "Create" button to create a profile. Here, you will need to select either "Feature Flag" or "Freeform Configuration". The difference between the two is the UI within the AWS console. "Feature Flag" is a bit friendlier to use and, it's more oriented to managing feature flags. In "Freeform Configuration" you have to modify a JSON file.
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
> Please note that all flags must be under a defined environment. The examples on this section show only the structure needed to declare a flag.
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

### Role-based flag
It enables turning a code path on for a list of roles when the flag is `enabled`. The allowed roles must be inserted on a list. The following examples shows the flag structure:
```yaml
role-based-flag:
  enabled: true
  type: role_based
  roles:
    - developer
    - qa
```

### User percentage flag
It enables turning a code path on for a percentage (`p`) of users from the whole population, whislt the rest of the population
 (`1-p`) won't be able to see the feaure. Salt can be any string value. The following example shows the flag structure:
 ```yaml
 percentage-based-flag:
  type: percentage
  percentage: 14.03
  salt: ticket_id
 ```

## Exceptions

This library can raise different exceptions given certain conditions:

- `ToggleNotFoundError`: When the library is trying to find a feature flag that doesn't exist in the `feature_toggles.yaml` file.
- `InvalidDecisionFunction`: When your `when_on` or `when_off` parameters are either booleans, not the same type, or a function that only returns a boolean.
- `ToggleEnvironmentError`: When the `ENVIRONMENT` env variable is either not specified or is not found in your feature flags file.
- `InvalidToggleType`: When a toggle type is not valid.
- `MissingToggleAttributes`: When a specific attribute needed for a particular feature type is not specified.
- `InvalidToggleAttribute`: When a specified attribute is not valid.
- `MissingToggleContext`: When the toggle context is not specified for a particular feature type that requires it (such as `pilot_users` and `role_based`).

## Considerations
- Please note that the current implementation is subject to change.
- If something goes wrong when setting up the Feature Flag library, feel free to get in touch with the Feature Flag team to help you with your issue.
- After performing load tests with the file-based providers, it was found that the YAML provider is slower than the JSON provider. This provider might become a performance bottleneck when used on projects with more than 300 feature toggles (provided that the project had 5 environments defined). JSON provider does not have the same issues, so take this into consideration when choosing a file format for feature flags. 
