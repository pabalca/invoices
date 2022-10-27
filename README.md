# ruler
Trading rules aggregator.
- Expose API to receive trading rules from autotraders.
- Whitelist and filter autotraders.
- Market link execution.

## Run it. Create and populate db.
```
FLASK_DEBUG=1 FLASK_APP=/Users/pabs/git/invoices/invoices/ flask initdb
FLASK_DEBUG=1 FLASK_APP=/Users/pabs/git/invoices/invoices/ flask scrape
FLASK_DEBUG=1 FLASK_APP=/Users/pabs/git/invoices/invoices/ flask run
```

