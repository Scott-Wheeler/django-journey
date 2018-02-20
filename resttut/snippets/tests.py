from django.test import TestCase

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.utils.six import BytesIO

# Create your tests here.


class SnippetTests(TestCase):

    def test_create_snippet(self):
        snippet = Snippet(code='print("hello world")\n')
        snippet.save()
        
        self.assertEqual(snippet.id, 1)
        self.assertEqual(snippet.title, '')
        self.assertEqual(snippet.linenos, False)
        self.assertEqual(snippet.code, 'print("hello world")\n')
        self.assertEqual(snippet.language, 'python')
        self.assertEqual(snippet.style, 'friendly')
        
        
class SnippetSerializerTests(TestCase):

    def test_create_snippet_serializer(self):
        snippet = Snippet(code='print("hello world")\n')
        snippet.save()
        serializer = SnippetSerializer(snippet)
        
        self.assertEqual(serializer.data['id'], 1)
        self.assertEqual(serializer.data['title'], '')
        self.assertEqual(serializer.data['code'], 'print("hello world")\n')
        self.assertEqual(serializer.data['language'], 'python')
        self.assertEqual(serializer.data['style'], 'friendly')

    def test_many_snippets_serializer(self):
        snippet1 = Snippet(code='print("hello world")\n', title="first")
        snippet1.save()
        snippet2 = Snippet(code='print("hi")\n', title="second")
        snippet2.save()
        serializer = SnippetSerializer(Snippet.objects.all(), many=True)
        
        self.assertEqual(serializer.data[0]['id'], 1)
        self.assertEqual(serializer.data[0]['title'], 'first')
        self.assertEqual(serializer.data[0]['code'], 'print("hello world")\n')
        self.assertEqual(serializer.data[0]['language'], 'python')
        self.assertEqual(serializer.data[0]['style'], 'friendly')
        self.assertEqual(serializer.data[1]['id'], 2)
        self.assertEqual(serializer.data[1]['title'], 'second')
        self.assertEqual(serializer.data[1]['code'], 'print("hi")\n')
        self.assertEqual(serializer.data[1]['language'], 'python')
        self.assertEqual(serializer.data[1]['style'], 'friendly')

    def test_create_snippet_instance(self):
        serializer = SnippetSerializer(data={'code': 'print("created")', 'title': 'Created With Serializer'})
        self.assertEqual(serializer.initial_data, {'code': 'print("created")', 'title': 'Created With Serializer'})
        
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        
        self.assertEqual(serializer.data['code'], 'print("created")')
        self.assertEqual(serializer.data['title'], 'Created With Serializer')
        self.assertEqual(serializer.data['language'], 'python')
        self.assertEqual(serializer.data['style'], 'friendly')

        snippet = serializer.create(serializer.validated_data)
        self.assertEqual(snippet.id, 1)
        self.assertEqual(snippet.title, 'Created With Serializer')
        self.assertEqual(snippet.linenos, False)
        self.assertEqual(snippet.code, 'print("created")')
        self.assertEqual(snippet.language, 'python')
        self.assertEqual(snippet.style, 'friendly')
        
    def test_update_snippet_instance(self):
        """
        serializer.data doesn't get updated, that's no good... TODO: what's going on?
        probably a cached instance
        """
        snippet = Snippet(code='print("hello world")\n')
        snippet.save()
        serializer = SnippetSerializer(snippet)
        serializer.update(serializer.instance, {
            'code':   'print("new code")\n',
            'title':  'updated',
            'linenos': True
        })
        self.assertEqual(snippet.code, 'print("new code")\n')
        self.assertEqual(snippet.title, 'updated')
        self.assertEqual(snippet.linenos, True)

    def test_serialize_to_json(self):
        snippet = Snippet(code='print("hello world")\n')
        snippet.save()
        serializer = SnippetSerializer(snippet)
        content = JSONRenderer().render(serializer.data)
        self.assertEqual(content,
            b'{"id":1,"title":"","code":"print(\\"hello world\\")\\n","linenos":false,"language":"python","style":"friendly"}'
        )

    def test_deserialize_from_json(self):
        snippet = Snippet(code='print("hello world")\n', title='snippet')
        snippet.save()
        serializer = SnippetSerializer(snippet)
        content = JSONRenderer().render(serializer.data)
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        
        self.assertEqual(data, {
            'id': 1,
            'title': 'snippet',
            'code': 'print("hello world")\n',
            'linenos': False,
            'language': 'python',
            'style': 'friendly'
        })
        
#     def test_create_snippets(self):
#         snippet1 = Snippet(code='foo = "bar"\n')
#         snippet1.save()
#         snippet2 = Snippet(code='print("hello world")\n')
#         snippet2.save()
#         serializer = SnippetSerializer(snippet2)
#         self.assertEqual(serializer.data['code']
        
