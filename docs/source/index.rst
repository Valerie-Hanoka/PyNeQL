PyNEQL: A module for searching Named Entity on SPARQL endpoints
===============================================================

.. toctree::
   :maxdepth: 3
   :glob:
   :hidden:

   Thing
   Person
   license
   modules



Linked Data is the global database of the World Wide Web. One can query those linked databases by sending SPARQL queries to different endpoints.
SPARQL vocabularies are huge and it is sometimes tedious to find how to ask for simple things as Named Entities.

This module aims to provide a very simple way to query named entities by their name, and retrieve a maximum of information from different SPARQL endpoints.

At the moment, only the type of named entities for which query is available are documented.


.. image:: ../../illustration_delimitante.png
  :width: 900
  :alt: ⚓


Named Entities Taxonomy
-----------------------

====================  ============  =======
       Type of Named Entity         Status
----------------------------------  -------
Name                  Inherits
====================  ============  =======
:doc:`Thing`                        Done
:doc:`Person`         Thing         Done
Book                  Thing         WIP
Location              Thing         TODO
TemporalInformation   Thing         TODO
====================  ============  =======

.. image:: ../../illustration_delimitante.png
  :width: 900
  :alt: ⚓



Queries Options
---------------

Languages
^^^^^^^^^^

It is possible to query in multiple languages. See section :doc:`Languages`.


Endpoints
^^^^^^^^^^

At the moment, only a small number of endpoints are supported. See section :doc:`Endpoints`.


Restraining the queries
^^^^^^^^^^^^^^^^^^^^^^^^

TODO


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
