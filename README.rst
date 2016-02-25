PassiveTotal Maltego Transforms
===============================

Introduction
------------

*Maltego Transform Distribution Server Transforms for PassiveTotal*

PassiveTotal provides extensive Maltego transforms through our hosting partner, Malformity. This is the preferred method of deployment and use for our transforms as we support the set hosted on Malformity. However, we recognize that some of our clients have their own Transform Distribution Servers and wanted to provide them a way to access the transforms if they wanted to host the set themselves.

Installation
------------

In order to run these transforms, you will need a working TDS server from Paterva_.

.. _Paterva: http://www.paterva.com/web6/documentation/developer-tds.php

Setup your transform server and install the Python libraries by following these instructions_.

.. _instructions: http://www.paterva.com/web6/documentation/TRX_documentation20130403.pdf

Install the requirements for the transforms::

    $ pip install -r requirements.txt

Add the following line to your Apache WSGI file::

    from ptxforms import ez_import

Login to your iTDS interface and enter all of the routes listed in maltego_transform_sheet.txt

Support
-------

These transforms come with no suppport and are only provided as a convenience. Our preferred method for accessing these transforms is using the Maltego transform hub which interfaces with Malformity Labs. Any questions, issues or problems should be directed to Github issues for the fastest triage.


Troubleshooting
---------------

If you experience issues post-installing the transforms, we have debugging logs that can be used.

You can add the following to ptxforms/__init__.py::

    import logging
    logging.basicConfig(level=logging.DEBUG)


Bug Reporting
-------------

Please use the issues feature of Github to report any problems with the transforms and we will work to triage any of the issues.