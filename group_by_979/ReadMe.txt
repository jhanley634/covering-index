
Oracle insists on aggregate functions for each column queried in a GROUP BY.
Mysql is more permissive.
Sometimes we'd like to use the same query with multiple backend DB vendors.

Does mysql performance suffer if we tack on MIN to referenced columns?
