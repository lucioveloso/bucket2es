#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
from mock import patch
import json
import os
import index



class TestLambda(unittest2.TestCase):

    def setUp(self):
        os.environ['lambda_action_on_process'] = "rename"
        os.environ['my_endpoint_url'] = "localhost"
        self.valid_event = '{ "Records":' \
                      '   [{ "s3":' \
                      '       { "bucket": ' \
                      '           { "name": "fake-bucket-name" ' \
                      '       },' \
                      '       "object": ' \
                      '           { "key": "fake-key" } ' \
                      '       }' \
                      '     }] ' \
                      '}'

    @patch('auth.init_elasticsearch')
    @patch('index.init_index')
    def test_invoke_with_none_event(self, mock_es, mock_es_index):

        with self.assertRaises(ValueError) as cm:
            index.lambda_handler(None, None)
        self.assertEqual(
            'Invalid event',
            str(cm.exception)
        )

    @patch('auth.init_elasticsearch')
    @patch('index.init_index')
    def test_invoke_with_invalid_event(self, mock_es, mock_es_index):
        invalid_event = '{ "Records": [{ "test": "a" }] } '
        invalid_event_obj = json.loads(invalid_event)
        with self.assertRaises(ValueError) as cm:
            index.lambda_handler(invalid_event_obj, None)
        self.assertEqual(
            'Invalid event record',
            str(cm.exception)
        )

    @patch('auth.init_elasticsearch')
    @patch('index.init_index')
    def test_invoke_with_invalid_event_just_bucket(self, mock_es, mock_es_index):
        invalid_event = '{ "Records":' \
                        '    [{ "s3":' \
                        '       { "bucket": ' \
                        '           { "name": "fake-bucket-name" } ' \
                        '       } ' \
                        '     }] ' \
                        '}'
        invalid_event_obj = json.loads(invalid_event)
        with self.assertRaises(ValueError) as cm:
            index.lambda_handler(invalid_event_obj, None)
        self.assertEqual(
            'Invalid event record',
            str(cm.exception)
        )

    @patch('auth.init_elasticsearch')
    @patch('index.init_index')
    @patch('index.read_bucket_file', return_value='{ "name": "MyName", "age": 20 }')
    @patch('index.change_processed_file')
    def test_invoke_mocking_bucket_valid_json(self, mock_es, mock_es_index, mock_bucket, mock_change_file):
        self.assertEqual(index.lambda_handler(json.loads(self.valid_event), None), "end")

    @patch('auth.init_elasticsearch')
    @patch('index.init_index')
    @patch('index.read_bucket_file', return_value='{ "name": "MyName", "age": "20" }')
    @patch('index.change_processed_file')
    def test_invoke_mocking_bucket_invalid_json(self, mock_es, mock_es_index, mock_bucket, mock_change_file):
        mock_bucket.return_value = '{ }'
        valid_event_obj = json.loads(self.valid_event)
        with self.assertRaises(ValueError) as cm:
            index.lambda_handler(valid_event_obj, None)
        self.assertEqual(
            'Invalid json file input',
            str(cm.exception)
        )

    def test_invoke_without_variables(self):
        os.environ.pop("lambda_action_on_process")
        os.environ.pop("my_endpoint_url")
        with self.assertRaises(ValueError) as cm:
            index.lambda_handler(None, None)
        self.assertEqual(
            'Missing variables',
            str(cm.exception)
        )
        self.assertRaises(ValueError, index.lambda_handler, None, None)
        self.setUp()


    @patch('auth.init_elasticsearch')
    @patch('index.init_index')
    def test_invoke_with_invalid_bucket(self, mock_es, mock_es_index):
        valid_event_obj = json.loads(self.valid_event)
        with self.assertRaises(ValueError) as cm:
            index.lambda_handler(valid_event_obj, None)
        self.assertEqual(
            'File does not exist',
            str(cm.exception)
        )


    @patch('index.s3', return_value=None)
    def test_change_processed_file(self, mock_s3):
        class Object(object):
            pass
        obj = Object()
        obj.bucket_name = "testing"
        obj.key = "key"
        setattr(obj, "bucket_name", "test")
        self.assertEqual(index.change_processed_file(obj, "True"), "Renamed")
        os.environ['lambda_action_on_process'] = "none"
        self.assertEqual(index.change_processed_file(obj, "True"), "None")
        os.environ['lambda_action_on_process'] = "delete"
        self.assertEqual(index.change_processed_file(obj, "True"), "Deleted")


if __name__ == '__main__':
    unittest2.main()
