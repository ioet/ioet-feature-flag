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

It is also possible to install with SSH instead of HTTPS by simply replacing `https://github.com` by `ssh://git@github.com`, although we recommend using SSH instead.
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

Example made by @eguezgustavo 

```python
import ioet_feature_flag

toggles = ioet_feature_flag.Toggles()


@toggles.toggle_decision
def usage_of_order_cancellation_email(get_toggles, when_on, when_off, context = None):
    order_cancellation_enabled, auto_refund_enabled = get_toggles(
        ["isOrderCancellationEnabled", "isAutoRefundEnable"],
        context
    )
    if order_cancellation_enabled and auto_refund_enabled:
        return when_on
    return when_off


def create_email_body(client_name: str, sales_order_number: str) -> str:
    header = f"""
    Dear {client_name},

    Your order number {sales_order_number} has bee approved.
    """

    footer = """
    Cheers,

    Your company team
    """
    
    toggle_context = ioet_feature_flag.ToggleContext(
      username=client_name,
      role="client"
    )
    cancellation_text = usage_of_order_cancellation_email(
        when_on=f"To cancel your order follow this link: http://cancel/{sales_order_number}",
        when_off="",
        context=toggle_context
    )

    return f"""
    {header}
    {cancellation_text}
    {footer}
    """

body = create_email_body("Gustavo", "2342937")
print(body)
```

You can also toggle between function calls without sending context, like this:
```python
def gen_one_pokedex():
  # Let's imagine that this is actually an API call and
  # we want to either prevent or allow its usage
  return ["Bulbasaur", "Squirtle", "Charmander"]

def gen_two_pokedex():
  # Same here
  return ["Chikorita", "Totodile", "Cyndaquil"]


# Here the decision function is declared with a context param
# but when called, you may not need to send it
@toggles.toggle_decision
def decide_pokedex_usage(get_toggles, when_on, when_off, context = None):
    use_gen_two_pokedex = get_toggles(["useGenTwoPokedex"], context)
    if use_gen_two_pokedex:
        return when_on
    return when_off


def client()
  get_pokedex_list = decide_pokedex_usage(
    when_on=gen_two_pokedex,
    when_off=gen_one_pokedex,
  )

  pokemons = get_pokedex_list()
```

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


## Considerations
- Please note that the current implementation is subject to change.
