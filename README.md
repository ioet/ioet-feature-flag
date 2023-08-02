# ioet Feature Flags

Feature Flags library to standardize feature toggles across our Internal Apps.
The current implementation is pretty bare-bones and only checks whether the flag is enabled or not.
However, we aim to follow [this standard](https://martinfowler.com/articles/feature-toggles.html) as our framework.

Moreover, we are planning to support [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) as the main feature flag provider. However, we may support other providers in the future.


## Setting up AWS AppConfig manually

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
```shell
pip install git+ssh://git@github.com/ioet/ioet-feature-flag.git@<branch-or-tag>
```

To install the latest version using `pip`:
```shell
pip install git+ssh://git@github.com/ioet/ioet-feature-flag.git
```

It is also possible to install with HTTPS instead of SSH by simply replacing `ssh://git@github.com` by `https://github.com`, although we recommend using SSH instead.

If you want to, you can also clone this repository locally and install the library by specifying the folder in which the repo was cloned

```shell
poetry add /path/to/ioet-feature-flag # Absolute path
poetry add ../ioet-feature-flag # Relative path
```

## Requirements
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


## Usage
The example below uses a sample feature to include a cancellation link in a email so the user can cancel the sales order.

1. Create the `feature_toggles.json` file with the following content:
```json
{
    "isOrderCancellationEnabled": true,
    "isAutoRefundEnable": false
}
```
2. Register a router class as a `FeatureRouter`. With this, `_get_toggles` method will be present to query any flag. Override the `__call__` method with your desired routing logic, like this:
```python
from ioet_feature_flag import FeatureRouter


class IncludeOrderCancelationLink(FeatureRouter):
    def __call__(self) -> bool:
        order_cancellation_enabled, auto_refund_enabled = self._get_toggles(
            ["isOrderCancellationEnabled", "isAutoRefundEnable"]
        )
        return order_cancellation_enabled and auto_refund_enabled
```

3. Mark a function as a toggle point. This function must have three arguments `toggle_point`, `when_on` and `when_off`. Use the `toggle_point` argument to toggle your paths of execution:
```python
from ioet_feature_flag import TogglePoint

@TogglePoint(toggle_router=IncludeOrderCancelationLink)
def _usage_of_order_cancellation_email(toggle_point, when_on, when_off):
    return toggle_point.toggle(
        when_on=when_on,
        when_off=when_off
    )

class InvoiceEmailer:
    def generate_invoice_email(self) -> str:
        base_mail = "Your order has been approved. "
        cancelation_link = _usage_of_order_cancellation_email(
            when_on="Link for cancelation is <here>",
            when_off=""
        )
        return base_mail + cancelation_link
    
```
4. Call your feature and check the response based on `feature_toggles.json` flags (try changing its values to make the function show the cancelation link):
```python
def main():
    email = InvoiceEmailer().generate_invoice_email()
    print(email) #Will show: Your order has been approved.


main()
```

## Considerations
- Please note that the current implementation is subject to change.
