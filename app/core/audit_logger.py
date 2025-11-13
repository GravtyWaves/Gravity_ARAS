"""
ARAS Audit Logging Middleware
Track all API requests and responses for security analysis

Built by Elite Team - DevOps Engineer (Kubernetes Expert)
"""

import json
import logging
import time
from datetime import datetime
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger("aras.audit")


class AuditLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware for comprehensive API audit logging.
    
    Logs all HTTP requests and responses with:
    - Request: method, path, query params, headers, IP, user agent
    - Response: status code, duration, size
    - Errors: exception details, stack trace
    
    Logs are structured JSON for easy parsing and analysis.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        # Configure structured JSON logging
        self._configure_logger()
    
    def _configure_logger(self):
        """Configure audit logger with JSON formatter."""
        # Create console handler with JSON formatting
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        
        # Custom JSON formatter
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                }
                
                # Add extra fields if present
                if hasattr(record, 'audit_data'):
                    log_data.update(record.audit_data)
                
                return json.dumps(log_data)
        
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log audit trail."""
        
        # Generate request ID
        request_id = self._generate_request_id(request)
        
        # Start timer
        start_time = time.time()
        
        # Extract request metadata
        request_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", ""),
            "referer": request.headers.get("referer", ""),
        }
        
        # Log request
        logger.info(
            f"{request.method} {request.url.path}",
            extra={"audit_data": {
                **request_data,
                "event": "request_received",
            }}
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Extract response metadata
            response_data = {
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "response_size": int(response.headers.get("content-length", 0)),
            }
            
            # Log response
            logger.info(
                f"{request.method} {request.url.path} - {response.status_code}",
                extra={"audit_data": {
                    **request_data,
                    **response_data,
                    "event": "request_completed",
                }}
            )
            
            # Add audit headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
            
            return response
            
        except Exception as e:
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            logger.error(
                f"{request.method} {request.url.path} - ERROR: {str(e)}",
                extra={"audit_data": {
                    **request_data,
                    "event": "request_error",
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "duration_ms": round(duration_ms, 2),
                }},
                exc_info=True
            )
            
            raise
    
    def _generate_request_id(self, request: Request) -> str:
        """Generate unique request ID."""
        import uuid
        return str(uuid.uuid4())
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address."""
        # Check for forwarded IP (behind proxy/load balancer)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check for real IP header
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to direct client
        if request.client:
            return request.client.host
        
        return "unknown"


# Utility function for manual audit logging
def log_audit_event(
    event: str,
    user_id: str = None,
    action: str = None,
    resource: str = None,
    details: dict = None
):
    """
    Log custom audit event.
    
    Args:
        event: Event type (e.g., "user_login", "data_access")
        user_id: User identifier
        action: Action performed (e.g., "create", "update", "delete")
        resource: Resource affected (e.g., "article", "user")
        details: Additional event details
    """
    audit_data = {
        "event": event,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    
    if user_id:
        audit_data["user_id"] = user_id
    if action:
        audit_data["action"] = action
    if resource:
        audit_data["resource"] = resource
    if details:
        audit_data["details"] = details
    
    logger.info(
        f"Audit: {event}",
        extra={"audit_data": audit_data}
    )
