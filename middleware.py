import json
import logging
import time
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

# 配置日志
logger = logging.getLogger('api_logger')
logger.setLevel(logging.INFO)

# 创建文件处理器
fh = logging.FileHandler('api.log')
fh.setLevel(logging.INFO)

# 创建控制台处理器
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 添加处理器到logger
if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(ch)

# 敏感字段列表
SENSITIVE_FIELDS = ['password', 'token', 'key', 'secret', 'api_key', 'auth']


def sanitize_data(data):
    """脱敏敏感数据"""
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            if key.lower() in SENSITIVE_FIELDS:
                sanitized[key] = '***'
            else:
                sanitized[key] = sanitize_data(value)
        return sanitized
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    else:
        return data


class APILoggingMiddleware(MiddlewareMixin):
    """API请求响应日志中间件"""
    
    def process_request(self, request: HttpRequest):
        """处理请求前"""
        # 只记录/api/开头的接口
        if not request.path.startswith('/api/'):
            return None
        
        # 记录请求开始时间
        request.start_time = time.time()
        
        # 记录请求信息
        try:
            # 尝试获取请求体
            if request.body:
                body = json.loads(request.body.decode('utf-8'))
                sanitized_body = sanitize_data(body)
            else:
                body = None
                sanitized_body = None
        except Exception as e:
            body = None
            sanitized_body = None
        
        # 记录请求信息
        logger.info(
            f"Request: {request.method} {request.path} "
            f"IP: {request.META.get('REMOTE_ADDR', '')} "
            f"Body: {json.dumps(sanitized_body) if sanitized_body else None}"
        )
        
        return None
    
    def process_response(self, request: HttpRequest, response: HttpResponse):
        """处理响应后"""
        # 只记录/api/开头的接口
        if not request.path.startswith('/api/'):
            return response
        
        # 计算耗时
        if hasattr(request, 'start_time'):
            elapsed_time = time.time() - request.start_time
        else:
            elapsed_time = 0
        
        # 记录响应信息
        try:
            # 尝试获取响应体
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                try:
                    # 尝试解析为JSON
                    response_data = json.loads(content)
                    sanitized_response = sanitize_data(response_data)
                except Exception:
                    # 如果不是JSON，直接使用
                    sanitized_response = content
            else:
                sanitized_response = None
        except Exception as e:
            sanitized_response = None
        
        # 记录响应信息
        logger.info(
            f"Response: {request.method} {request.path} "
            f"Status: {response.status_code} "
            f"Time: {elapsed_time:.3f}s "
            f"Body: {json.dumps(sanitized_response) if sanitized_response else None}"
        )
        
        return response
    
    def process_exception(self, request: HttpRequest, exception: Exception):
        """处理异常"""
        # 只记录/api/开头的接口
        if not request.path.startswith('/api/'):
            return None
        
        # 计算耗时
        if hasattr(request, 'start_time'):
            elapsed_time = time.time() - request.start_time
        else:
            elapsed_time = 0
        
        # 记录异常信息
        logger.error(
            f"Exception: {request.method} {request.path} "
            f"IP: {request.META.get('REMOTE_ADDR', '')} "
            f"Time: {elapsed_time:.3f}s "
            f"Error: {str(exception)}",
            exc_info=True
        )
        
        return None
