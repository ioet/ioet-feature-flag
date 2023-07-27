# Library usage example
> This example uses the invoiceEmalier case described on [Feature Flags Framework](https://martinfowler.com/articles/feature-toggles.html)

First, it's required to *register* the toggle routers that the app will use. With this, you can access the toggle configuration object and define your behaviour based on any number of toggles:
```python
# routers.py
from ioet_feature_flag import ToggleRouter


class IncludeOrderCancelationInEmail(ToggleRouter):
    def __call__(self) -> bool:
        return self._toggle_configuration.get("cancelarion_function")
```

To use the new router, a toggle point needs to be defined. Inject a toggle point to any feature:
```python
from ioet_feature_flag import TogglePoint

from routers import IncludeOrderCancelationInEmail


class InvoiceEmailer:
    def __init__(self, *other_args, toggle_point: TogglePoint):
        # other attributes
        self.toggle_point = toggle_point

    def generate_invoice_email(self):
        base_mail = build_email_for_invoice(self.invoice)
        modified_mail = self.toggle_point.toggle(
            toggle_router=IncludeOrderCancelationInEmail()
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
from ioet_feaure_flag import get_toggle_configuration


def main():
    emailer = InvoiceEmailer()
    mail_with_cancel_link = emailer.generate_invoice_email()
    toggle_config = get_toggle_configuration()
    toggle_config.set_toggle("cancelarion_function", False)
    mail_without_cancel_link = emailer.generate_invoice_email()

```