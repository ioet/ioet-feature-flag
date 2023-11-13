# Library usage example with functional programming

Example made by @eguezgustavo 

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

## Using the library
The feature flag library includes a decorator to mark functions as toggle routers and use them in other functions:

```python
import ioet_feature_flag

import typing


toggles = ioet_feature_flag.Toggles()


@toggles.toggle_decision
def usage_of_order_cancellation_email(get_toggles: typing.Callable, when_on, when_off, context: ioet_feature_flag.ToggleContext = None):
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

    Your order number {sales_order_number} has been approved.
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

> **IMPORTANT NOTE:** The function `get_toggles` used on the decision function expects a list and **will return a tuple** if you pass mulltiple flags to it and **you will need to unpack it**. However, if you pass only one flag (as in, a list with just one element), **it will return a boolean** with the value of the flag that you specified. We made this decision to avoid confusion when using the result in an if statement.

```python
my_toggle_a, my_toggle_b = get_toggles(["myToggleA", "myToggleB"])  # returns a tuple
my_toggle = get_toggles(["myToggleA"])  # returns a boolean
my_toggle = get_toggles("myToggleA")  # also returns a boolean
```

## Toggling decision without context

You can also toggle between function calls without sending context, like this:
```python
import ioet_feature_flag

import typing


toggles = ioet_feature_flag.Toggles()


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
def decide_pokedex_usage(get_toggles: typing.Callable, when_on, when_off, context: ioet_feature_flag.ToggleContext = None):
    use_gen_two_pokedex = get_toggles(["useGenTwoPokedex"], context)
    if use_gen_two_pokedex:
        return when_on
    return when_off


def client():
  get_pokedex_list = decide_pokedex_usage(
    when_on=gen_two_pokedex,
    when_off=gen_one_pokedex,
  )

  pokemons = get_pokedex_list()
```
> **Note:** Even though sending a toggle context is optional, the parameter declaration on the decision function is *required* and needs to be defaulted to `None`.

## Toggling behavior
Providing that the environment variable is set to `dev`, the email body created with first example will look like this:
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
