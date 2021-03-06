# -*- coding: utf-8 -*-
from io import BytesIO, BufferedReader
from watson.http.wsgi import get_form_vars, _process_field_storage
from tests.watson.http.support import sample_environ


class TestWsgiModule(object):

    def test_get_form_vars_with_file(self):
        environ = sample_environ(
            REQUEST_METHOD='POST',
            CONTENT_TYPE='multipart/form-data; boundary=---------------------------721837373350705526688164684',
        )
        postdata = """-----------------------------721837373350705526688164684
Content-Disposition: form-data; name="id"

1234
-----------------------------721837373350705526688164684
Content-Disposition: form-data; name="title"


-----------------------------721837373350705526688164684
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

Testing 123.

-----------------------------721837373350705526688164684
Content-Disposition: form-data; name="submit"

 Add\x20
-----------------------------721837373350705526688164684--
"""
        environ['CONTENT_LENGTH'] = len(postdata)
        encoding = 'utf-8'
        fp = BufferedReader(BytesIO(postdata.encode(encoding)))
        environ['wsgi.input'] = fp
        post, files = get_form_vars(environ, dict)
        file = files.get('file')
        assert file.filename == 'test.txt'
        assert post.get('id') == '1234'

    def test_process_field_storage(self):
        post, files = _process_field_storage('test', {}, {})
        assert len(post) == 0
