# ifos_trace_id_middleware_snippets_v1.py
# FastAPI trace-id middleware
FASTAPI = '''
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
class TraceIdMW(BaseHTTPMiddleware):
  async def dispatch(self, request, call_next):
    tid = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-Id"] = tid
    return response
'''
# Express snippet
EXPRESS = '''
app.use((req,res,next)=>{
  const tid = req.get("X-Request-Id") || require("crypto").randomUUID();
  res.set("X-Request-Id", tid);
  req.traceId = tid;
  next();
});
'''
