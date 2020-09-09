from typing import get_type_hints

import hypothesis
from hypothesis import strategies as st

import isort


def _as_config(kw) -> isort.Config:
    kw["atomic"] = False
    if "wrap_length" in kw and "line_length" in kw:
        kw["wrap_length"], kw["line_length"] = sorted([kw["wrap_length"], kw["line_length"]])
    try:
        return isort.Config(**kw)
    except ValueError:
        kw["wrap_length"] = 0
        return isort.Config(**kw)


def configs() -> st.SearchStrategy[isort.Config]:
    """Generate arbitrary Config objects."""
    skip = {
        "line_ending",
        "sections",
        "known_standard_library",
        "known_future_library",
        "known_third_party",
        "known_first_party",
        "known_local_folder",
        "extra_standard_library",
        "forced_separate",
        "lines_after_imports",
        "add_imports",
        "lines_between_sections",
        "lines_between_types",
        "sources",
        "virtual_env",
        "conda_env",
        "directory",
        "formatter",
        "formatting_function",
        "comment_prefix",
        "atomic",
        "skip",
        "src_paths",
    }
    inferred_kwargs = {
        k: st.from_type(v)
        for k, v in get_type_hints(isort.settings._Config).items()
        if k not in skip
    }
    specific = {
        "line_length": st.integers(0, 200),
        "wrap_length": st.integers(0, 200),
        "indent": st.integers(0, 20).map(lambda n: n * " "),
        "default_section": st.sampled_from(sorted(isort.settings.KNOWN_SECTION_MAPPING)),
        "force_grid_wrap": st.integers(0, 20),
        "profile": st.sampled_from(sorted(isort.settings.profiles)),
        "py_version": st.sampled_from(("auto",) + isort.settings.VALID_PY_TARGETS),
    }
    kwargs = {**inferred_kwargs, **specific}
    return st.fixed_dictionaries({}, optional=kwargs).map(_as_config)


st.register_type_strategy(isort.Config, configs())

CODE_SNIPPET = """
'''Taken from bottle.py

Copyright (c) 2009-2018, Marcel Hellkamp.
License: MIT (see LICENSE for details)
'''
# Lots of stdlib and builtin differences.
if py3k:
    import http.client as httplib
    import _thread as thread
    from urllib.parse import urljoin, SplitResult as UrlSplitResult
    from urllib.parse import urlencode, quote as urlquote, unquote as urlunquote
    urlunquote = functools.partial(urlunquote, encoding='latin1')
    from http.cookies import SimpleCookie, Morsel, CookieError
    from collections.abc import MutableMapping as DictMixin
    import pickle # comment number 2
    from io import BytesIO
    import configparser

    basestring = str
    unicode = str
    json_loads = lambda s: json_lds(touni(s))
    callable = lambda x: hasattr(x, '__call__')
    imap = map

    def _raise(*a):
        raise a[0](a[1]).with_traceback(a[2])
else:  # 2.x
    import httplib
    import thread
    from urlparse import urljoin, SplitResult as UrlSplitResult
    from urllib import urlencode, quote as urlquote, unquote as urlunquote
    from Cookie import SimpleCookie, Morsel, CookieError
    from itertools import imap
    import cPickle as pickle
    from StringIO import StringIO as BytesIO
    import ConfigParser as configparser  # commentnumberone
    from collections import MutableMapping as DictMixin
    unicode = unicode
    json_loads = json_lds
    exec(compile('def _raise(*a): raise a[0], a[1], a[2]', '<py3fix>', 'exec'))
"""
SHOULD_RETAIN = [
    """'''Taken from bottle.py

Copyright (c) 2009-2018, Marcel Hellkamp.
License: MIT (see LICENSE for details)
'''""",
    "# Lots of stdlib and builtin differences.",
    "if py3k:",
    "http.client",
    "_thread",
    "urllib.parse",
    "urlencode",
    "urlunquote = functools.partial(urlunquote, encoding='latin1')",
    "http.cookies",
    "SimpleCookie",
    "collections.abc",
    "pickle",
    "comment number 2",
    "io",
    "configparser",
    """basestring = str
    unicode = str
    json_loads = lambda s: json_lds(touni(s))
    callable = lambda x: hasattr(x, '__call__')
    imap = map

    def _raise(*a):
        raise a[0](a[1]).with_traceback(a[2])
else:  # 2.x
""",
    "httplib",
    "thread",
    "urlparse",
    "urllib",
    "Cookie",
    "itertools",
    "cPickle",
    "StringIO",
    "ConfigParser",
    "commentnumberone",
    "collections",
    """unicode = unicode
    json_loads = json_lds
    exec(compile('def _raise(*a): raise a[0], a[1], a[2]', '<py3fix>', 'exec'))""",
]


@hypothesis.example(
    config=isort.Config(py_version='all', force_to_top=frozenset(), skip=frozenset({'.svn', '.venv', 'build', 'dist', '.bzr', '.tox', '.hg', '.mypy_cache', '.nox', '_build', 'buck-out', 'node_modules', '.git', '.eggs', '.pants.d', 'venv', '.direnv'}), skip_glob=frozenset(), skip_gitignore=True, line_length=79, wrap_length=0, line_ending='', sections=('FUTURE', 'STDLIB', 'THIRDPARTY', 'FIRSTPARTY', 'LOCALFOLDER'), no_sections=False, known_future_library=frozenset({'__future__'}), known_third_party=frozenset(), known_first_party=frozenset(), known_local_folder=frozenset(), known_standard_library=frozenset({'pwd', 'types', 'nntplib', 'jpeg', 'pyclbr', 'encodings', 'ctypes', 'macerrors', 'filecmp', 'dbm', 'mimetypes', 'statvfs', 'msvcrt', 'spwd', 'codecs', 'SimpleHTTPServer', 'compiler', 'pickletools', 'tkinter', 'pickle', 'fm', 'bsddb', 'contextvars', 'dummy_thread', 'pipes', 'heapq', 'dircache', 'commands', 'unicodedata', 'ntpath', 'marshal', 'fpformat', 'linecache', 'calendar', 'pty', 'MimeWriter', 'inspect', 'mmap', 'ic', 'tty', 'nis', 'new', 'wave', 'HTMLParser', 'anydbm', 'tracemalloc', 'pdb', 'sunau', 'GL', 'parser', 'winsound', 'dbhash', 'zlib', 'MacOS', 'pprint', 'crypt', 'aetools', 'DEVICE', 'fl', 'gettext', 'asyncore', 'copyreg', 'queue', 'resource', 'turtledemo', 'fnmatch', 'hotshot', 'trace', 'string', 'plistlib', 'gzip', 'functools', 'aepack', 'hashlib', 'imp', 'MiniAEFrame', 'getpass', 'shutil', 'ttk', 'multifile', 'operator', 'reprlib', 'subprocess', 'cgi', 'select', 'SimpleXMLRPCServer', 'audioop', 'macresource', 'stringprep', 'wsgiref', 'SUNAUDIODEV', 'atexit', 'lzma', 'asyncio', 'datetime', 'binhex', 'autoGIL', 'doctest', 'thread', 'enum', 'tempfile', 'posixfile', 'mhlib', 'html', 'itertools', 'exceptions', 'sgmllib', 'array', 'test', 'imputil', 'shlex', 'flp', 'uu', 'gdbm', 'urlparse', 'msilib', 'termios', 'modulefinder', 'ossaudiodev', 'timeit', 'binascii', 'popen2', 'ConfigParser', 'poplib', 'zipfile', 'cfmfile', 'pstats', 'AL', 'contextlib', 'code', 'zipimport', 'base64', 'platform', 'ast', 'fileinput', 'locale', 'buildtools', 'stat', 'quopri', 'readline', 'collections', 'aetypes', 'concurrent', 'runpy', 'copy_reg', 'rexec', 'cmath', 'optparse', 'dummy_threading', 'ColorPicker', 'sched', 'netrc', 'sunaudiodev', 'socketserver', 'logging', 'PixMapWrapper', 'sysconfig', 'Nav', 'copy', 'cmd', 'csv', 'chunk', 'multiprocessing', 'warnings', 'weakref', 'py_compile', 'sre', 'sre_parse', 'curses', 'threading', 're', 'FrameWork', '_thread', 'imgfile', 'cd', 'sre_constants', 'xdrlib', 'dataclasses', 'urllib2', 'StringIO', 'configparser', 'importlib', 'UserList', 'posixpath', 'mailbox', 'rfc822', 'grp', 'pydoc', 'sets', 'textwrap', 'numbers', 'W', 'gl', 'htmllib', 'macostools', 'tarfile', 'ipaddress', 'xmlrpc', 'icopen', 'traceback', '_winreg', 'random', 'CGIHTTPServer', 'dis', 'sha', 'selectors', 'statistics', 'DocXMLRPCServer', 'imghdr', 'venv', 'keyword', 'xmlrpclib', 'ftplib', 'getopt', 'posix', 'smtpd', 'profile', 'sndhdr', 'signal', 'EasyDialogs', 'dumbdbm', 'fcntl', 'SocketServer', 'distutils', 'symbol', 'pathlib', 'cStringIO', 'imaplib', 'unittest', 'al', 'cProfile', 'robotparser', 'BaseHTTPServer', 'os', 'pkgutil', 'socket', 'fractions', 'shelve', 'aifc', 'cgitb', 'xml', 'decimal', 'sre_compile', 'ssl', 'user', 'Bastion', 'formatter', 'time', 'abc', 'winreg', 'difflib', 'FL', 'bz2', 'asynchat', 'gc', 'gensuitemodule', 'symtable', 'secrets', 'Carbon', 'mailcap', 'sys', 'bdb', 'fpectl', 'httplib', 'webbrowser', 'smtplib', 'Cookie', 'whichdb', 'turtle', 'tokenize', 'UserString', 'tabnanny', 'site', 'struct', 'codeop', 'email', 'typing', 'cookielib', 'Queue', 'rlcompleter', 'errno', 'macpath', 'videoreader', 'md5', 'cPickle', 'Tix', 'io', 'faulthandler', 'Tkinter', 'glob', 'syslog', 'telnetlib', '_dummy_thread', 'hmac', 'uuid', 'imageop', 'future_builtins', 'json', 'htmlentitydefs', 'lib2to3', 'UserDict', 'mutex', 'sqlite3', 'findertools', 'bisect', 'builtins', 'urllib', 'http', 'compileall', 'argparse', 'ScrolledText', 'token', 'dl', 'applesingle', 'math', 'ensurepip', 'mimify', 'mimetools', 'colorsys', 'zipapp', '__builtin__'}), extra_standard_library=frozenset(), known_other={'other': frozenset({'', '\x10\x1bm'})}, multi_line_output=0, forced_separate=(), indent='             ', comment_prefix='  #', length_sort=True, length_sort_straight=False, length_sort_sections=frozenset(), add_imports=frozenset(), remove_imports=frozenset({'', '\U00076fe7þs\x0c\U000c8b75v\U00106541', '𥒒>\U0001960euj𒎕\x9e', '\x15\x9b', '\x02l', '\U000b71ef.\x1c', '\x7f?\U000ec91c', '\x7f,ÞoÀP8\x1b\x1e»3\x86\x94¤ÁÓ~\U00066b1a,O\U0010ab28\x90«', 'Y\x06ºZ\x04Ýì\U00078ce1.\U0010c1f9[EK\x83EÖø', ';À¨|\x1bÂ 𑐒🍸V'}), append_only=False, reverse_relative=True, force_single_line=False, single_line_exclusions=('Y\U000347d9g\x957K', '', 'Ê\U000e8ad2\U0008fa72ùÏ\x19ç\U000eaecc𤎪.', '·o\U000d00e5\U000b36de+\x8f\U000b5953´\x08oÜ', '', ':sI¶', ''), default_section='THIRDPARTY', import_headings={}, balanced_wrapping=False, use_parentheses=True, order_by_type=True, atomic=False, lines_after_imports=-1, lines_between_sections=1, lines_between_types=0, combine_as_imports=True, combine_star=False, include_trailing_comma=False, from_first=False, verbose=False, quiet=False, force_adds=False, force_alphabetical_sort_within_sections=False, force_alphabetical_sort=False, force_grid_wrap=0, force_sort_within_sections=False, lexicographical=False, ignore_whitespace=False, no_lines_before=frozenset({'uøø', '¢', '&\x8c5Ï\U000e5f01Ø', '\U0005d415\U000a3df2h\U000f24e5\U00104d7b34¹ÒÀ', '\U000e374c8', 'w'}), no_inline_sort=False, ignore_comments=False, case_sensitive=False, sources=({'py_version': 'py3', 'force_to_top': frozenset(), 'skip': frozenset({'.svn', '.venv', 'build', 'dist', '.bzr', '.tox', '.hg', '.mypy_cache', '.nox', '_build', 'buck-out', 'node_modules', '.git', '.eggs', '.pants.d', 'venv', '.direnv'}), 'skip_glob': frozenset(), 'skip_gitignore': False, 'line_length': 79, 'wrap_length': 0, 'line_ending': '', 'sections': ('FUTURE', 'STDLIB', 'THIRDPARTY', 'FIRSTPARTY', 'LOCALFOLDER'), 'no_sections': False, 'known_future_library': frozenset({'__future__'}), 'known_third_party': frozenset(), 'known_first_party': frozenset(), 'known_local_folder': frozenset(), 'known_standard_library': frozenset({'pwd', 'copy', 'cmd', 'csv', 'chunk', 'multiprocessing', 'warnings', 'types', 'weakref', 'nntplib', 'pyclbr', 'encodings', 'py_compile', 'sre', 'ctypes', 'sre_parse', 'filecmp', 'curses', 'threading', 'dbm', 're', '_thread', 'sre_constants', 'xdrlib', 'dataclasses', 'mimetypes', 'configparser', 'importlib', 'msvcrt', 'spwd', 'posixpath', 'mailbox', 'codecs', 'grp', 'pickletools', 'tkinter', 'pickle', 'contextvars', 'pydoc', 'textwrap', 'numbers', 'pipes', 'heapq', 'tarfile', 'unicodedata', 'ntpath', 'ipaddress', 'marshal', 'xmlrpc', 'traceback', 'linecache', 'calendar', 'pty', 'random', 'dis', 'selectors', 'statistics', 'imghdr', 'venv', 'inspect', 'mmap', 'keyword', 'ftplib', 'tty', 'nis', 'getopt', 'posix', 'smtpd', 'wave', 'profile', 'sndhdr', 'signal', 'tracemalloc', 'pdb', 'sunau', 'winsound', 'parser', 'zlib', 'fcntl', 'pprint', 'distutils', 'crypt', 'symbol', 'gettext', 'pathlib', 'asyncore', 'copyreg', 'imaplib', 'unittest', 'queue', 'resource', 'turtledemo', 'fnmatch', 'cProfile', 'os', 'pkgutil', 'socket', 'trace', 'fractions', 'string', 'shelve', 'plistlib', 'aifc', 'gzip', 'functools', 'cgitb', 'xml', 'hashlib', 'decimal', 'imp', 'sre_compile', 'ssl', 'formatter', 'winreg', 'time', 'getpass', 'shutil', 'abc', 'difflib', 'bz2', 'operator', 'reprlib', 'subprocess', 'cgi', 'select', 'asynchat', 'audioop', 'gc', 'secrets', 'symtable', 'mailcap', 'sys', 'bdb', 'fpectl', 'stringprep', 'webbrowser', 'smtplib', 'wsgiref', 'atexit', 'lzma', 'asyncio', 'datetime', 'binhex', 'doctest', 'turtle', 'enum', 'tempfile', 'tokenize', 'tabnanny', 'site', 'html', 'struct', 'itertools', 'codeop', 'email', 'array', 'test', 'typing', 'shlex', 'uu', 'msilib', 'termios', 'rlcompleter', 'modulefinder', 'ossaudiodev', 'timeit', 'binascii', 'poplib', 'errno', 'macpath', 'zipfile', 'io', 'faulthandler', 'pstats', 'contextlib', 'code', 'glob', 'zipimport', 'base64', 'syslog', 'platform', 'ast', 'fileinput', 'telnetlib', 'locale', '_dummy_thread', 'hmac', 'stat', 'uuid', 'quopri', 'readline', 'collections', 'json', 'concurrent', 'lib2to3', 'sqlite3', 'runpy', 'cmath', 'optparse', 'bisect', 'builtins', 'urllib', 'dummy_threading', 'http', 'compileall', 'argparse', 'token', 'sched', 'netrc', 'math', 'ensurepip', 'socketserver', 'colorsys', 'zipapp', 'logging', 'sysconfig'}), 'extra_standard_library': frozenset(), 'known_other': {}, 'multi_line_output': 0, 'forced_separate': (), 'indent': '    ', 'comment_prefix': '  #', 'length_sort': False, 'length_sort_straight': False, 'length_sort_sections': frozenset(), 'add_imports': frozenset(), 'remove_imports': frozenset(), 'append_only': False, 'reverse_relative': False, 'force_single_line': False, 'single_line_exclusions': (), 'default_section': 'THIRDPARTY', 'import_headings': {}, 'balanced_wrapping': False, 'use_parentheses': False, 'order_by_type': True, 'atomic': False, 'lines_after_imports': -1, 'lines_between_sections': 1, 'lines_between_types': 0, 'combine_as_imports': False, 'combine_star': False, 'include_trailing_comma': False, 'from_first': False, 'verbose': False, 'quiet': False, 'force_adds': False, 'force_alphabetical_sort_within_sections': False, 'force_alphabetical_sort': False, 'force_grid_wrap': 0, 'force_sort_within_sections': False, 'lexicographical': False, 'ignore_whitespace': False, 'no_lines_before': frozenset(), 'no_inline_sort': False, 'ignore_comments': False, 'case_sensitive': False, 'sources': (), 'virtual_env': '', 'conda_env': '', 'ensure_newline_before_comments': False, 'directory': '', 'profile': '', 'honor_noqa': False, 'src_paths': frozenset(), 'old_finders': False, 'remove_redundant_aliases': False, 'float_to_top': False, 'filter_files': False, 'formatter': '', 'formatting_function': None, 'color_output': False, 'treat_comments_as_code': frozenset(), 'treat_all_comments_as_code': False, 'supported_extensions': frozenset({'py', 'pyx', 'pyi'}), 'blocked_extensions': frozenset({'pex'}), 'constants': frozenset(), 'classes': frozenset(), 'variables': frozenset(), 'dedup_headings': False, 'source': 'defaults'}, {'classes': frozenset({'\U000eb6c6\x9eÑ\U0008297dâhï\x8eÆ', 'C', '\x8e\U000422ac±\U000b5a1f\U000c4166', 'ùÚ'}), 'single_line_exclusions': ('Y\U000347d9g\x957K', '', 'Ê\U000e8ad2\U0008fa72ùÏ\x19ç\U000eaecc𤎪.', '·o\U000d00e5\U000b36de+\x8f\U000b5953´\x08oÜ', '', ':sI¶', ''), 'indent': '             ', 'no_lines_before': frozenset({'uøø', '¢', '&\x8c5Ï\U000e5f01Ø', '\U0005d415\U000a3df2h\U000f24e5\U00104d7b34¹ÒÀ', '\U000e374c8', 'w'}), 'quiet': False, 'honor_noqa': False, 'dedup_headings': True, 'known_other': {'\x10\x1bm': frozenset({'\U000682a49\U000e1a63²KÇ¶4', '', '\x1a', '©'}), '': frozenset({'íå\x94Ì', '\U000cf258'})}, 'treat_comments_as_code': frozenset({''}), 'length_sort': True, 'reverse_relative': True, 'combine_as_imports': True, 'py_version': 'all', 'use_parentheses': True, 'skip_gitignore': True, 'remove_imports': frozenset({'', '\U00076fe7þs\x0c\U000c8b75v\U00106541', '𥒒>\U0001960euj𒎕\x9e', '\x15\x9b', '\x02l', '\U000b71ef.\x1c', '\x7f?\U000ec91c', '\x7f,ÞoÀP8\x1b\x1e»3\x86\x94¤ÁÓ~\U00066b1a,O\U0010ab28\x90«', 'Y\x06ºZ\x04Ýì\U00078ce1.\U0010c1f9[EK\x83EÖø', ';À¨|\x1bÂ 𑐒🍸V'}), 'atomic': False, 'source': 'runtime'}), virtual_env='', conda_env='', ensure_newline_before_comments=False, directory='/home/abuild/rpmbuild/BUILD/isort-5.5.1', profile='', honor_noqa=False, old_finders=False, remove_redundant_aliases=False, float_to_top=False, filter_files=False, formatting_function=None, color_output=False, treat_comments_as_code=frozenset({''}), treat_all_comments_as_code=False, supported_extensions=frozenset({'py', 'pyx', 'pyi'}), blocked_extensions=frozenset({'pex'}), constants=frozenset(), classes=frozenset({'\U000eb6c6\x9eÑ\U0008297dâhï\x8eÆ', 'C', '\x8e\U000422ac±\U000b5a1f\U000c4166', 'ùÚ'}), variables=frozenset(), dedup_headings=True),
    disregard_skip=True
)
@hypothesis.given(
    config=st.from_type(isort.Config),
    disregard_skip=st.booleans(),
)
@hypothesis.settings(deadline=None)
def test_isort_is_idempotent(config: isort.Config, disregard_skip: bool) -> None:
    try:
        result = isort.code(CODE_SNIPPET, config=config, disregard_skip=disregard_skip)
        result = isort.code(result, config=config, disregard_skip=disregard_skip)
        assert result == isort.code(result, config=config, disregard_skip=disregard_skip)
    except ValueError:
        pass


@hypothesis.example(
    config=isort.Config(py_version='all', force_to_top=frozenset(), skip=frozenset({'.svn', '.venv', 'build', 'dist', '.bzr', '.tox', '.hg', '.mypy_cache', '.nox', '_build', 'buck-out', 'node_modules', '.git', '.eggs', '.pants.d', 'venv', '.direnv'}), skip_glob=frozenset(), skip_gitignore=True, line_length=79, wrap_length=0, line_ending='', sections=('FUTURE', 'STDLIB', 'THIRDPARTY', 'FIRSTPARTY', 'LOCALFOLDER'), no_sections=False, known_future_library=frozenset({'__future__'}), known_third_party=frozenset(), known_first_party=frozenset(), known_local_folder=frozenset(), known_standard_library=frozenset({'pwd', 'types', 'nntplib', 'jpeg', 'pyclbr', 'encodings', 'ctypes', 'macerrors', 'filecmp', 'dbm', 'mimetypes', 'statvfs', 'msvcrt', 'spwd', 'codecs', 'SimpleHTTPServer', 'compiler', 'pickletools', 'tkinter', 'pickle', 'fm', 'bsddb', 'contextvars', 'dummy_thread', 'pipes', 'heapq', 'dircache', 'commands', 'unicodedata', 'ntpath', 'marshal', 'fpformat', 'linecache', 'calendar', 'pty', 'MimeWriter', 'inspect', 'mmap', 'ic', 'tty', 'nis', 'new', 'wave', 'HTMLParser', 'anydbm', 'tracemalloc', 'pdb', 'sunau', 'GL', 'parser', 'winsound', 'dbhash', 'zlib', 'MacOS', 'pprint', 'crypt', 'aetools', 'DEVICE', 'fl', 'gettext', 'asyncore', 'copyreg', 'queue', 'resource', 'turtledemo', 'fnmatch', 'hotshot', 'trace', 'string', 'plistlib', 'gzip', 'functools', 'aepack', 'hashlib', 'imp', 'MiniAEFrame', 'getpass', 'shutil', 'ttk', 'multifile', 'operator', 'reprlib', 'subprocess', 'cgi', 'select', 'SimpleXMLRPCServer', 'audioop', 'macresource', 'stringprep', 'wsgiref', 'SUNAUDIODEV', 'atexit', 'lzma', 'asyncio', 'datetime', 'binhex', 'autoGIL', 'doctest', 'thread', 'enum', 'tempfile', 'posixfile', 'mhlib', 'html', 'itertools', 'exceptions', 'sgmllib', 'array', 'test', 'imputil', 'shlex', 'flp', 'uu', 'gdbm', 'urlparse', 'msilib', 'termios', 'modulefinder', 'ossaudiodev', 'timeit', 'binascii', 'popen2', 'ConfigParser', 'poplib', 'zipfile', 'cfmfile', 'pstats', 'AL', 'contextlib', 'code', 'zipimport', 'base64', 'platform', 'ast', 'fileinput', 'locale', 'buildtools', 'stat', 'quopri', 'readline', 'collections', 'aetypes', 'concurrent', 'runpy', 'copy_reg', 'rexec', 'cmath', 'optparse', 'dummy_threading', 'ColorPicker', 'sched', 'netrc', 'sunaudiodev', 'socketserver', 'logging', 'PixMapWrapper', 'sysconfig', 'Nav', 'copy', 'cmd', 'csv', 'chunk', 'multiprocessing', 'warnings', 'weakref', 'py_compile', 'sre', 'sre_parse', 'curses', 'threading', 're', 'FrameWork', '_thread', 'imgfile', 'cd', 'sre_constants', 'xdrlib', 'dataclasses', 'urllib2', 'StringIO', 'configparser', 'importlib', 'UserList', 'posixpath', 'mailbox', 'rfc822', 'grp', 'pydoc', 'sets', 'textwrap', 'numbers', 'W', 'gl', 'htmllib', 'macostools', 'tarfile', 'ipaddress', 'xmlrpc', 'icopen', 'traceback', '_winreg', 'random', 'CGIHTTPServer', 'dis', 'sha', 'selectors', 'statistics', 'DocXMLRPCServer', 'imghdr', 'venv', 'keyword', 'xmlrpclib', 'ftplib', 'getopt', 'posix', 'smtpd', 'profile', 'sndhdr', 'signal', 'EasyDialogs', 'dumbdbm', 'fcntl', 'SocketServer', 'distutils', 'symbol', 'pathlib', 'cStringIO', 'imaplib', 'unittest', 'al', 'cProfile', 'robotparser', 'BaseHTTPServer', 'os', 'pkgutil', 'socket', 'fractions', 'shelve', 'aifc', 'cgitb', 'xml', 'decimal', 'sre_compile', 'ssl', 'user', 'Bastion', 'formatter', 'time', 'abc', 'winreg', 'difflib', 'FL', 'bz2', 'asynchat', 'gc', 'gensuitemodule', 'symtable', 'secrets', 'Carbon', 'mailcap', 'sys', 'bdb', 'fpectl', 'httplib', 'webbrowser', 'smtplib', 'Cookie', 'whichdb', 'turtle', 'tokenize', 'UserString', 'tabnanny', 'site', 'struct', 'codeop', 'email', 'typing', 'cookielib', 'Queue', 'rlcompleter', 'errno', 'macpath', 'videoreader', 'md5', 'cPickle', 'Tix', 'io', 'faulthandler', 'Tkinter', 'glob', 'syslog', 'telnetlib', '_dummy_thread', 'hmac', 'uuid', 'imageop', 'future_builtins', 'json', 'htmlentitydefs', 'lib2to3', 'UserDict', 'mutex', 'sqlite3', 'findertools', 'bisect', 'builtins', 'urllib', 'http', 'compileall', 'argparse', 'ScrolledText', 'token', 'dl', 'applesingle', 'math', 'ensurepip', 'mimify', 'mimetools', 'colorsys', 'zipapp', '__builtin__'}), extra_standard_library=frozenset(), known_other={'other': frozenset({'', '\x10\x1bm'})}, multi_line_output=0, forced_separate=(), indent='             ', comment_prefix='  #', length_sort=True, length_sort_straight=False, length_sort_sections=frozenset(), add_imports=frozenset(), remove_imports=frozenset({'', '\U00076fe7þs\x0c\U000c8b75v\U00106541', '𥒒>\U0001960euj𒎕\x9e', '\x15\x9b', '\x02l', '\U000b71ef.\x1c', '\x7f?\U000ec91c', '\x7f,ÞoÀP8\x1b\x1e»3\x86\x94¤ÁÓ~\U00066b1a,O\U0010ab28\x90«', 'Y\x06ºZ\x04Ýì\U00078ce1.\U0010c1f9[EK\x83EÖø', ';À¨|\x1bÂ 𑐒🍸V'}), append_only=False, reverse_relative=True, force_single_line=False, single_line_exclusions=('Y\U000347d9g\x957K', '', 'Ê\U000e8ad2\U0008fa72ùÏ\x19ç\U000eaecc𤎪.', '·o\U000d00e5\U000b36de+\x8f\U000b5953´\x08oÜ', '', ':sI¶', ''), default_section='THIRDPARTY', import_headings={}, balanced_wrapping=False, use_parentheses=True, order_by_type=True, atomic=False, lines_after_imports=-1, lines_between_sections=1, lines_between_types=0, combine_as_imports=True, combine_star=False, include_trailing_comma=False, from_first=False, verbose=False, quiet=False, force_adds=False, force_alphabetical_sort_within_sections=False, force_alphabetical_sort=False, force_grid_wrap=0, force_sort_within_sections=False, lexicographical=False, ignore_whitespace=False, no_lines_before=frozenset({'uøø', '¢', '&\x8c5Ï\U000e5f01Ø', '\U0005d415\U000a3df2h\U000f24e5\U00104d7b34¹ÒÀ', '\U000e374c8', 'w'}), no_inline_sort=False, ignore_comments=False, case_sensitive=False, sources=({'py_version': 'py3', 'force_to_top': frozenset(), 'skip': frozenset({'.svn', '.venv', 'build', 'dist', '.bzr', '.tox', '.hg', '.mypy_cache', '.nox', '_build', 'buck-out', 'node_modules', '.git', '.eggs', '.pants.d', 'venv', '.direnv'}), 'skip_glob': frozenset(), 'skip_gitignore': False, 'line_length': 79, 'wrap_length': 0, 'line_ending': '', 'sections': ('FUTURE', 'STDLIB', 'THIRDPARTY', 'FIRSTPARTY', 'LOCALFOLDER'), 'no_sections': False, 'known_future_library': frozenset({'__future__'}), 'known_third_party': frozenset(), 'known_first_party': frozenset(), 'known_local_folder': frozenset(), 'known_standard_library': frozenset({'pwd', 'copy', 'cmd', 'csv', 'chunk', 'multiprocessing', 'warnings', 'types', 'weakref', 'nntplib', 'pyclbr', 'encodings', 'py_compile', 'sre', 'ctypes', 'sre_parse', 'filecmp', 'curses', 'threading', 'dbm', 're', '_thread', 'sre_constants', 'xdrlib', 'dataclasses', 'mimetypes', 'configparser', 'importlib', 'msvcrt', 'spwd', 'posixpath', 'mailbox', 'codecs', 'grp', 'pickletools', 'tkinter', 'pickle', 'contextvars', 'pydoc', 'textwrap', 'numbers', 'pipes', 'heapq', 'tarfile', 'unicodedata', 'ntpath', 'ipaddress', 'marshal', 'xmlrpc', 'traceback', 'linecache', 'calendar', 'pty', 'random', 'dis', 'selectors', 'statistics', 'imghdr', 'venv', 'inspect', 'mmap', 'keyword', 'ftplib', 'tty', 'nis', 'getopt', 'posix', 'smtpd', 'wave', 'profile', 'sndhdr', 'signal', 'tracemalloc', 'pdb', 'sunau', 'winsound', 'parser', 'zlib', 'fcntl', 'pprint', 'distutils', 'crypt', 'symbol', 'gettext', 'pathlib', 'asyncore', 'copyreg', 'imaplib', 'unittest', 'queue', 'resource', 'turtledemo', 'fnmatch', 'cProfile', 'os', 'pkgutil', 'socket', 'trace', 'fractions', 'string', 'shelve', 'plistlib', 'aifc', 'gzip', 'functools', 'cgitb', 'xml', 'hashlib', 'decimal', 'imp', 'sre_compile', 'ssl', 'formatter', 'winreg', 'time', 'getpass', 'shutil', 'abc', 'difflib', 'bz2', 'operator', 'reprlib', 'subprocess', 'cgi', 'select', 'asynchat', 'audioop', 'gc', 'secrets', 'symtable', 'mailcap', 'sys', 'bdb', 'fpectl', 'stringprep', 'webbrowser', 'smtplib', 'wsgiref', 'atexit', 'lzma', 'asyncio', 'datetime', 'binhex', 'doctest', 'turtle', 'enum', 'tempfile', 'tokenize', 'tabnanny', 'site', 'html', 'struct', 'itertools', 'codeop', 'email', 'array', 'test', 'typing', 'shlex', 'uu', 'msilib', 'termios', 'rlcompleter', 'modulefinder', 'ossaudiodev', 'timeit', 'binascii', 'poplib', 'errno', 'macpath', 'zipfile', 'io', 'faulthandler', 'pstats', 'contextlib', 'code', 'glob', 'zipimport', 'base64', 'syslog', 'platform', 'ast', 'fileinput', 'telnetlib', 'locale', '_dummy_thread', 'hmac', 'stat', 'uuid', 'quopri', 'readline', 'collections', 'json', 'concurrent', 'lib2to3', 'sqlite3', 'runpy', 'cmath', 'optparse', 'bisect', 'builtins', 'urllib', 'dummy_threading', 'http', 'compileall', 'argparse', 'token', 'sched', 'netrc', 'math', 'ensurepip', 'socketserver', 'colorsys', 'zipapp', 'logging', 'sysconfig'}), 'extra_standard_library': frozenset(), 'known_other': {}, 'multi_line_output': 0, 'forced_separate': (), 'indent': '    ', 'comment_prefix': '  #', 'length_sort': False, 'length_sort_straight': False, 'length_sort_sections': frozenset(), 'add_imports': frozenset(), 'remove_imports': frozenset(), 'append_only': False, 'reverse_relative': False, 'force_single_line': False, 'single_line_exclusions': (), 'default_section': 'THIRDPARTY', 'import_headings': {}, 'balanced_wrapping': False, 'use_parentheses': False, 'order_by_type': True, 'atomic': False, 'lines_after_imports': -1, 'lines_between_sections': 1, 'lines_between_types': 0, 'combine_as_imports': False, 'combine_star': False, 'include_trailing_comma': False, 'from_first': False, 'verbose': False, 'quiet': False, 'force_adds': False, 'force_alphabetical_sort_within_sections': False, 'force_alphabetical_sort': False, 'force_grid_wrap': 0, 'force_sort_within_sections': False, 'lexicographical': False, 'ignore_whitespace': False, 'no_lines_before': frozenset(), 'no_inline_sort': False, 'ignore_comments': False, 'case_sensitive': False, 'sources': (), 'virtual_env': '', 'conda_env': '', 'ensure_newline_before_comments': False, 'directory': '', 'profile': '', 'honor_noqa': False, 'src_paths': frozenset(), 'old_finders': False, 'remove_redundant_aliases': False, 'float_to_top': False, 'filter_files': False, 'formatter': '', 'formatting_function': None, 'color_output': False, 'treat_comments_as_code': frozenset(), 'treat_all_comments_as_code': False, 'supported_extensions': frozenset({'py', 'pyx', 'pyi'}), 'blocked_extensions': frozenset({'pex'}), 'constants': frozenset(), 'classes': frozenset(), 'variables': frozenset(), 'dedup_headings': False, 'source': 'defaults'}, {'classes': frozenset({'\U000eb6c6\x9eÑ\U0008297dâhï\x8eÆ', 'C', '\x8e\U000422ac±\U000b5a1f\U000c4166', 'ùÚ'}), 'single_line_exclusions': ('Y\U000347d9g\x957K', '', 'Ê\U000e8ad2\U0008fa72ùÏ\x19ç\U000eaecc𤎪.', '·o\U000d00e5\U000b36de+\x8f\U000b5953´\x08oÜ', '', ':sI¶', ''), 'indent': '             ', 'no_lines_before': frozenset({'uøø', '¢', '&\x8c5Ï\U000e5f01Ø', '\U0005d415\U000a3df2h\U000f24e5\U00104d7b34¹ÒÀ', '\U000e374c8', 'w'}), 'quiet': False, 'honor_noqa': False, 'dedup_headings': True, 'known_other': {'\x10\x1bm': frozenset({'\U000682a49\U000e1a63²KÇ¶4', '', '\x1a', '©'}), '': frozenset({'íå\x94Ì', '\U000cf258'})}, 'treat_comments_as_code': frozenset({''}), 'length_sort': True, 'reverse_relative': True, 'combine_as_imports': True, 'py_version': 'all', 'use_parentheses': True, 'skip_gitignore': True, 'remove_imports': frozenset({'', '\U00076fe7þs\x0c\U000c8b75v\U00106541', '𥒒>\U0001960euj𒎕\x9e', '\x15\x9b', '\x02l', '\U000b71ef.\x1c', '\x7f?\U000ec91c', '\x7f,ÞoÀP8\x1b\x1e»3\x86\x94¤ÁÓ~\U00066b1a,O\U0010ab28\x90«', 'Y\x06ºZ\x04Ýì\U00078ce1.\U0010c1f9[EK\x83EÖø', ';À¨|\x1bÂ 𑐒🍸V'}), 'atomic': False, 'source': 'runtime'}), virtual_env='', conda_env='', ensure_newline_before_comments=False, directory='/home/abuild/rpmbuild/BUILD/isort-5.5.1', profile='', honor_noqa=False, old_finders=False, remove_redundant_aliases=False, float_to_top=False, filter_files=False, formatting_function=None, color_output=False, treat_comments_as_code=frozenset({''}), treat_all_comments_as_code=False, supported_extensions=frozenset({'py', 'pyx', 'pyi'}), blocked_extensions=frozenset({'pex'}), constants=frozenset(), classes=frozenset({'\U000eb6c6\x9eÑ\U0008297dâhï\x8eÆ', 'C', '\x8e\U000422ac±\U000b5a1f\U000c4166', 'ùÚ'}), variables=frozenset(), dedup_headings=True),
    disregard_skip=True
)
@hypothesis.given(
    config=st.from_type(isort.Config),
    disregard_skip=st.booleans(),
)
@hypothesis.settings(deadline=None)
def test_isort_doesnt_lose_imports_or_comments(config: isort.Config, disregard_skip: bool) -> None:
    result = isort.code(CODE_SNIPPET, config=config, disregard_skip=disregard_skip)
    for should_be_retained in SHOULD_RETAIN:
        if should_be_retained not in result:
            if config.ignore_comments and should_be_retained.startswith("comment"):
                continue

            assert should_be_retained in result
