Python Demandware SDK
========

Description
-----------
Python Demandware SDK provides access to the OCAPI services.
https://documentation.demandware.com/display/DOC131/Open+Commerce+API

Installation
-------------
::

    $ pip install dw --upgrade


Basic usage
-----------
::

    from dw.client import Demandware

    DW_API = {
        'client_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'hostname': 'changeme.demandware.net',
        'site': 'SiteGenesis',
        'version': 'v13_1',
    }

    conn = Demandware(DW_API)

    product = conn.get_product('008884303989')
    print product.name


Contributors
-------------

* Moises Brenes <https://github.com/gin>
* Conflict <https://github.com/weareconflict>
