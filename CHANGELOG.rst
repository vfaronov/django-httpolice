History of changes
==================


Unreleased
~~~~~~~~~~
- Dropped Python 2 support. If you need it, use the older versions.
- To reduce clutter in failing tests, notice `1070`_ is now silenced
  by default (unless you override ``HTTPOLICE_SILENCE``).

.. _1070: https://httpolice.readthedocs.io/page/notices.html#1070


0.4.0 - 2018-03-31
~~~~~~~~~~~~~~~~~~

- Supports Django 2.0.
- No longer supports Django prior to 1.11.
- No longer supports old-style ``MIDDLEWARE_CLASSES``.


0.3.0 - 2017-03-12
~~~~~~~~~~~~~~~~~~

- For consistency, the backlog view now shows exchanges in direct order
  (that is, the latest exchange is now at the bottom).
- The deprecated form ``HTTPOLICE_RAISE = True`` is no longer supported.
  Use ``HTTPOLICE_RAISE = 'error'`` (or ``'comment'``) instead.


0.2.0 - 2016-08-14
~~~~~~~~~~~~~~~~~~
Added
-----
- The middleware is now compatible with new-style (Django 1.10+) ``MIDDLEWARE``
  as well as old-style ``MIDDLEWARE_CLASSES``.
- You can now ask the middleware to raise ``ProtocolError``
  even on notices of severity "comment"
  by setting ``HTTPOLICE_RAISE = 'comment'``.

Deprecated
----------
- Setting ``HTTPOLICE_RAISE = True`` is deprecated
  in favor of the new form ``HTTPOLICE_RAISE = 'error'``.
  The next release will only support the new form.


0.1.0 - 2016-05-08
~~~~~~~~~~~~~~~~~~

- Initial release.
