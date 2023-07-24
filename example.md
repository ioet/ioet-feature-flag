# Library usage example
> This example uses the invoiceEmalier case described on [Feature Flags Framework](https://martinfowler.com/articles/feature-toggles.html)

First, it's required to create a RouterStrategy for the client:
```python
from ioet_feature_flag import RouterStrategy


class ClientStrategy(RouterStrategy):
    def compute_state(self, config_name: str) -> bool:
        if config_name == "include_order_cancelation_in_email":
            # base logic but the idea is to decide here how to deal
            # with multiple feature toggles
            return self.toggle_config.get_toggle("cancelarion_function")

```

Then, register the router strategy to the ToggleRouter
```python
from ioet_feature_flag import ToggleRouter
from client import ClientStrategy


router = ToggleRouter()
router.register(ClientStrategy)
```

Use the router to decorate toggle points on your classes:
```python
from client._config import router


class InvoiceEmailer:
    @router.toggle_point("include_order_cancelation_in_email")
    def generate_invoice_email(self, toggle_point=None):
        base_mail = build_email_for_invoice(self.invoice)
        modified_mail = toggle_point.toggle(
            path_when_enabled=lambda: self.add_order_cancelation_content(base_mail),
            path_when_disabled=lambda: base_email
        )
        return modified_mail

    def add_order_cancelation_content(self, email):
        # some custom logic
        return email
```

Now you can use your code with different outputs that depend on the toggle (example of `main.py`):
```python
from client import InvoiceEmailer
from ioet_feaure_flag import ToggleConfiguration


def main():
    emailer = InvoiceEmailer()
    mail_with_cancel_link = emailer.generate_invoice_email()
    toggle_config = ToggleConfiguration()
    toggle_config.set_toggle("cancelarion_function", False)
    mail_without_cancel_link = emailer.generate_invoice_email()

```