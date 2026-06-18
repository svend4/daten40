# ifos_cors_config_snippets_v1.py
# FastAPI example
FASTAPI = '''
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["https://app.example.com"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
'''
# Express example
EXPRESS = '''
const cors = require("cors");
app.use(cors({
  origin: ["https://app.example.com"],
  credentials: true,
  methods: ["GET","POST","PUT","PATCH","DELETE","OPTIONS"],
  allowedHeaders: ["Content-Type","Authorization"]
}));
'''
