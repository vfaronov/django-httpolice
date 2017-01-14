Changelog
=========

All notable changes to Django-HTTPolice will be documented in this file.

This project adheres to `Semantic Versioning <http://semver.org/>`_
(which means it is unstable until 1.0).


Unreleased
~~~~~~~~~~

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
