# swagger_client.DefaultApi

All URIs are relative to *https://7b49p3sxj6.execute-api.ap-northeast-2.amazonaws.com/prod*

Method | HTTP request | Description
------------- | ------------- | -------------
[**analyses_analysis_id_predefined_url_get**](DefaultApi.md#analyses_analysis_id_predefined_url_get) | **GET** /analyses/{analysisId}/predefined_url | 
[**analyses_analysis_id_rounds_round_put**](DefaultApi.md#analyses_analysis_id_rounds_round_put) | **PUT** /analyses/{analysisId}/rounds/{round} | 
[**analyses_post**](DefaultApi.md#analyses_post) | **POST** /analyses | 
[**cdms_get**](DefaultApi.md#cdms_get) | **GET** /cdms | 
[**organizations_get**](DefaultApi.md#organizations_get) | **GET** /organizations | 
[**organizations_org_id_get**](DefaultApi.md#organizations_org_id_get) | **GET** /organizations/{orgId} | 


# **analyses_analysis_id_predefined_url_get**
> analyses_analysis_id_predefined_url_get(round, analysis_id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
round = 'round_example' # str | 
analysis_id = 'analysis_id_example' # str | 

try:
    api_instance.analyses_analysis_id_predefined_url_get(round, analysis_id)
except ApiException as e:
    print("Exception when calling DefaultApi->analyses_analysis_id_predefined_url_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **round** | **str**|  | 
 **analysis_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **analyses_analysis_id_rounds_round_put**
> analyses_analysis_id_rounds_round_put(analysis_id, round)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
analysis_id = 'analysis_id_example' # str | 
round = 'round_example' # str | 

try:
    api_instance.analyses_analysis_id_rounds_round_put(analysis_id, round)
except ApiException as e:
    print("Exception when calling DefaultApi->analyses_analysis_id_rounds_round_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **analysis_id** | **str**|  | 
 **round** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **analyses_post**
> analyses_post()



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try:
    api_instance.analyses_post()
except ApiException as e:
    print("Exception when calling DefaultApi->analyses_post: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cdms_get**
> cdms_get()



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try:
    api_instance.cdms_get()
except ApiException as e:
    print("Exception when calling DefaultApi->cdms_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organizations_get**
> organizations_get()



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try:
    api_instance.organizations_get()
except ApiException as e:
    print("Exception when calling DefaultApi->organizations_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organizations_org_id_get**
> organizations_org_id_get(org_id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
org_id = 'org_id_example' # str | 

try:
    api_instance.organizations_org_id_get(org_id)
except ApiException as e:
    print("Exception when calling DefaultApi->organizations_org_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

