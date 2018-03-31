History of changes
==================


Unreleased
~~~~~~~~~~

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
