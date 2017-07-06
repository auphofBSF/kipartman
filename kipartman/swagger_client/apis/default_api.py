# coding: utf-8

"""
    Kipartman

    Kipartman api specifications

    OpenAPI spec version: 1.0.0
    Contact: --
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class DefaultApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def add_parts_category(self, category, **kwargs):
        """
        Creates a new part category
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.add_parts_category(category, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param PartCategoryData category: Category to add (required)
        :return: PartCategory
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.add_parts_category_with_http_info(category, **kwargs)
        else:
            (data) = self.add_parts_category_with_http_info(category, **kwargs)
            return data

    def add_parts_category_with_http_info(self, category, **kwargs):
        """
        Creates a new part category
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.add_parts_category_with_http_info(category, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param PartCategoryData category: Category to add (required)
        :return: PartCategory
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['category']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_parts_category" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'category' is set
        if ('category' not in params) or (params['category'] is None):
            raise ValueError("Missing the required parameter `category` when calling `add_parts_category`")


        collection_formats = {}

        resource_path = '/parts/categories'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'category' in params:
            body_params = params['category']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PartCategory',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def delete_parts_category(self, category_id, **kwargs):
        """
        Delete part category
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_parts_category(category_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int category_id: Category id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.delete_parts_category_with_http_info(category_id, **kwargs)
        else:
            (data) = self.delete_parts_category_with_http_info(category_id, **kwargs)
            return data

    def delete_parts_category_with_http_info(self, category_id, **kwargs):
        """
        Delete part category
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_parts_category_with_http_info(category_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int category_id: Category id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['category_id']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_parts_category" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'category_id' is set
        if ('category_id' not in params) or (params['category_id'] is None):
            raise ValueError("Missing the required parameter `category_id` when calling `delete_parts_category`")


        collection_formats = {}

        resource_path = '/parts/categories/{category_id}'.replace('{format}', 'json')
        path_params = {}
        if 'category_id' in params:
            path_params['category_id'] = params['category_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'DELETE',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type=None,
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def find_parts_categories(self, **kwargs):
        """
        Return all categories for parts
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.find_parts_categories(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: list[PartCategory]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.find_parts_categories_with_http_info(**kwargs)
        else:
            (data) = self.find_parts_categories_with_http_info(**kwargs)
            return data

    def find_parts_categories_with_http_info(self, **kwargs):
        """
        Return all categories for parts
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.find_parts_categories_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: list[PartCategory]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_parts_categories" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        resource_path = '/parts/categories'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='list[PartCategory]',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update_parts_category(self, category_id, category, **kwargs):
        """
        Update part category
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_parts_category(category_id, category, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int category_id: Category id (required)
        :param PartCategoryData category: Category to update (required)
        :return: PartCategory
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_parts_category_with_http_info(category_id, category, **kwargs)
        else:
            (data) = self.update_parts_category_with_http_info(category_id, category, **kwargs)
            return data

    def update_parts_category_with_http_info(self, category_id, category, **kwargs):
        """
        Update part category
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_parts_category_with_http_info(category_id, category, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int category_id: Category id (required)
        :param PartCategoryData category: Category to update (required)
        :return: PartCategory
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['category_id', 'category']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_parts_category" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'category_id' is set
        if ('category_id' not in params) or (params['category_id'] is None):
            raise ValueError("Missing the required parameter `category_id` when calling `update_parts_category`")
        # verify the required parameter 'category' is set
        if ('category' not in params) or (params['category'] is None):
            raise ValueError("Missing the required parameter `category` when calling `update_parts_category`")


        collection_formats = {}

        resource_path = '/parts/categories/{category_id}'.replace('{format}', 'json')
        path_params = {}
        if 'category_id' in params:
            path_params['category_id'] = params['category_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'category' in params:
            body_params = params['category']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'PUT',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PartCategory',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
