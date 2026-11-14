# Retrospective Invoice FAQ Assistant
## Author: Maxine Coimin

This assistant, Ayo, is designed to let customers know the status of their retro invoice. It uses only the mock invoice data provided to it and does not pull information for any outside sources.
Any requests outside of its scope are redirected to a live billing speciialist to assist with. This includes things directly tied to the invoice like requesting to make a payment or updating biling addresses.

This is unsecured and could be damaging to the company if customer specific data were to be leaked.


Week 12 Update
The model does well with providing the invoice status. It also does well with requesting specific formating to search, one example being that I asked for the status of invoice 1001 and it responded that the invoice formatting has to be input as INV-1000. The door refused to update the address without the full address being provided. I added instructions that required the correct invoice number formatting and full address before making a change. 