# Library usage example with functional programming

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