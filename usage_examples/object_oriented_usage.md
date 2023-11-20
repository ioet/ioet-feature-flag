# Library usage example with object-oriented programming

Suppose we have an email body builder in our application. A new feature to include the cancellation link on the email's body is being developed. The project structure looks like this:

```
.
├── cases
│   ├── __init__.py
│   └── create_email_body_case.py
├── dependency_factories
│   ├── __init__.py
│   └── cases_factory.py
├── feature_toggles
│   └── feature-toggles.yaml
├── test
└── main.py

```
> **Info:**
> By default, the library will search for a YAML file on `./feature_toggles/feature-toggles.yaml`.
> To override this behavior, create a `Toggles` instance specifying the `provider` parameter.
> This way, you can not only change the toggles path but also use any other provider described on
> README file.

## Adding feature flags
Since it's needed to test the new feature locally, a new pair of toggles are added to the development environment in the `feature-toggles.yaml` file:

```yaml
dev:
  isOrderCancellationEnabled:
    type: static
    enabled: true
  isAutoRefundEnabled:
    type: static
    enabled: true
```

> **Note:** Both flags need to be declared as false in any other environment that isn't meant to have the feature yet. If an environment does not have a flag declared, the library will raise an exception.

## Using the library in a class
Let's add the library to `create_email_body_case.py` and use it to insert a toggle point:
```python
from ioet_feature_flag import Toggles, ToggleContext

import typing

class CreateEmailBodyCase2:
    # Here, we inserted the Toggles class as a dependency for this use case
    def __init__(self, feature_toggles: Toggles):
        self._toggles = feature_toggles

    # The decision function is declared to check for flags
    # and determine the adequate code path (when_on or when_off)
    @staticmethod
    def _usage_of_order_cancellation_email(get_toggles: typing.Callable, when_on, when_off, context: ToggleContext=None):
        order_cancellation_enabled, auto_refund_enabled = get_toggles(
            ["isOrderCancellationEnabled", "isAutoRefundEnabled"],
            context
        )
        if order_cancellation_enabled and auto_refund_enabled:
            return when_on
        return when_off

    def run(self, client_name: str, sales_order_number: str) -> str:
        header = f"""
            Dear {client_name},

            Your order number {sales_order_number} has been approved.
            """

        footer = """
            Cheers,

            Your company team
            """

        # The decision function is wrapped using the toggle dependency
        use_cancellation_text = self._toggles.toggle_decision(self._usage_of_order_cancellation_email)

        # The toggle decision can be used only specifying the return values
        cancellation_text = use_cancellation_text(
            when_on=f"    To cancel your order follow this link: http://cancel/{sales_order_number}",
            when_off="",
        )

        return f"""
        {header}
        {cancellation_text}
        {footer}
        """

```
> **IMPORTANT NOTE:** The function `get_toggles` used on the decision function expects a list and **will return a tuple** if you pass mulltiple flags to it and **you will need to unpack it**. However, if you pass only one flag (as in, a list with just one element), **it will return a boolean** with the value of the flag that you specified. We made this decision to avoid confusion when using the result in an if statement.

```python
my_toggle_a, my_toggle_b = get_toggles(["myToggleA", "myToggleB"])  # returns a tuple
my_toggle = get_toggles(["myToggleA"])  # returns a boolean
my_toggle = get_toggles("myToggleA")  # also returns a boolean
```

Now, the dependency factory for the use case needs to be updated to include the toggles class.

> **Important:** 
> Please note that the Toggles class needs a `project_root: Path` parameter. This is done to make the default path
> of the toggles file consistent. If another path or provider needs to be used, you can do it, the project root parameter
> will not be considered.

For this example, project root path was declared on `dependency_factories/__init__.py`:
```python
from pathlib import Path


PROJECT_ROOT: Path = Path(__file__).parent.parent

```
In the use case's dependency factory, we just add the toggles dependency liek this: 

```python
from ioet_feature_flag import Toggles

import cases

from . import PROJECT_ROOT


def get_create_email_body_case() -> cases.CreateEmailBodyCase2:
    return cases.CreateEmailBodyCase2(feature_toggles=Toggles(project_root=PROJECT_ROOT))

```

### Using context for toggle decision
If a flag needs context to determine if it's on or off, you can provide it using the `ToggleContext` class:
```python
from ioet_feature_flag import Toggles, ToggleContext

import typing

class CreateEmailBodyCase2:
    # Here, we inserted the Toggles class as a dependency for this use case
    def __init__(self, feature_toggles: Toggles):
        self._toggles = feature_toggles

    # The decision function is declared to check for flags
    # and determine the adequate code path (when_on or when_off)
    @staticmethod
    def _usage_of_order_cancellation_email(get_toggles: typing.Callable, when_on, when_off, context: ToggleContext=None):
        order_cancellation_enabled, auto_refund_enabled = get_toggles(
            ["isOrderCancellationEnabled", "isAutoRefundEnabled"],
            context
        )
        if order_cancellation_enabled and auto_refund_enabled:
            return when_on
        return when_off

    def run(self, client_name: str, sales_order_number: str) -> str:
        header = f"""
            Dear {client_name},

            Your order number {sales_order_number} has been approved.
            """

        footer = """
            Cheers,

            Your company team
            """

        # The decision function is wrapped using the toggle dependency
        use_cancellation_text = self._toggles.toggle_decision(self._usage_of_order_cancellation_email)

        # A context is declared to send the user's information for
        # the toggle decision
        toggle_context = ToggleContext(
            username=client_name,
            role="client"
        )

        # The toggled is passed as a parameter to the toggle decision function
        cancellation_text = use_cancellation_text(
            when_on=f"    To cancel your order follow this link: http://cancel/{sales_order_number}",
            when_off="",
            context=toggle_context
        )

        return f"""
        {header}
        {cancellation_text}
        {footer}
        """

```
> **Note:** Even though sending a toggle context is optional, the parameter declaration on the decision function is *required* and needs to be defaulted to `None`.

## Toggling behavior
Now the use case is ready to be used locally with the new feature. Providing that the environment variable is set to `dev`, the email body will look like this:
```
    Dear Alec,

    Your order number 3456 has been approved.
    
    To cancel your order follow this link: http://cancel/3456

    Cheers,

    Your company team
```

Otherwise, it will look like this:

```
    Dear Alec,

    Your order number 3456 has been approved.
    


    Cheers,

    Your company team

```



