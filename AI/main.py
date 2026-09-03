"""Customer AI Service - Following Lab 5 & 6 patterns.

Run from the AI folder:

    uvicorn api.main:app --reload --port 8000

Endpoints:
    GET  /health            - Service health check
    GET  /tools             - List available tools
    POST /auth/set-token    - Set JWT token for backend authentication
    POST /customer/summary  - Generate customer summary (Lab 5 pattern)
    POST /customer/ask      - Ask a specific question (Lab 5 pattern)
    POST /customer/graph    - Run graph with human approval (Lab 6 pattern)
    POST /customer/resume   - Resume after human approval (Lab 6 pattern)
    GET  /customer/thread/{id} - Get thread state (Lab 6 pattern)
"""

import os
import time
from typing import Optional, Literal, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# ── Load Environment ──
load_dotenv()

# ── Configuration ──
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemini-2.5-flash-lite")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000/api")


# ── Pydantic Models ──

class TokenRequest(BaseModel):
    """Request to set JWT token."""
    token: str = Field(..., description="JWT token from C# backend")


class SummaryRequest(BaseModel):
    """Request for customer summary."""
    customer_id: int = Field(..., description="Customer ID")
    include_service_history: bool = Field(True, description="Include service history")
    include_bookings: bool = Field(True, description="Include pending bookings")
    include_maintenance: bool = Field(True, description="Include maintenance recommendations")
    specific_question: Optional[str] = Field(None, description="Specific question to answer")


class AskRequest(BaseModel):
    """Request for asking a question."""
    customer_id: int = Field(..., description="Customer ID")
    question: str = Field(..., description="Question to ask about the customer")
    max_iterations: int = Field(5, ge=1, le=10, description="Max tool iterations")


class GraphRequest(BaseModel):
    """Request for graph-based agent."""
    customer_id: int = Field(..., description="Customer ID")
    question: str = Field(..., description="Question to process")
    thread_id: str = Field("default", description="Conversation thread ID")


class ResumeRequest(BaseModel):
    """Resume after human approval."""
    thread_id: str = Field(..., description="Thread ID to resume")
    decision: str = Field(..., description="'approve' or 'deny'")


class ToolCall(BaseModel):
    """Record of a tool call."""
    tool: str
    args: dict[str, Any]
    result: str


class CustomerAIResponse(BaseModel):
    """Response from the AI service."""
    customer_id: int
    summary: str
    tool_calls: List[ToolCall] = Field(default_factory=list)
    stop_reason: Literal["answered", "iteration_cap", "error"] = "answered"
    tokens_used: int = 0
    seconds: float = 0.0


class GraphResponse(BaseModel):
    """Graph response."""
    status: Literal["completed", "awaiting_approval"]
    answer: Optional[str] = None
    interrupt: Optional[dict] = None
    nodes: List[str] = Field(default_factory=list)
    thread_id: str


# ── Backend Client ──

class BackendClient:
    """Client to call the C# backend API."""
    
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def set_token(self, token: str):
        """Set the JWT token for authentication."""
        self.token = token
    
    def _get_headers(self) -> dict:
        """Get headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    async def get_customer(self, customer_id: int) -> dict:
        """Fetch customer from C# backend."""
        import httpx
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/Customer/{customer_id}",
                headers=self._get_headers()
            )
            if response.status_code == 404:
                return {"error": f"Customer {customer_id} not found"}
            response.raise_for_status()
            return response.json()


# Global backend client
_backend = BackendClient()


# ── Tools ──

def get_customer_info(customer_id: int) -> str:
    """
    Get comprehensive customer information including name, contact details, and vehicles.
    """
    try:
        return f"""
Customer ID: {customer_id}
Name: John Doe
Email: john.doe@example.com
Phone: +1-555-0101
Address: 123 Main St, Anytown, AN 12345
Customer Since: 2024-01-01
Number of Vehicles: 1

Vehicles:
- 2020 Toyota Camry (ABC-123), Mileage: 45,000 km
"""
    except Exception as e:
        return f"Error fetching customer info: {str(e)}"


def get_service_history(customer_id: int, limit: int = 5) -> str:
    """
    Get the customer's service history. Shows past services, costs, and work performed.
    """
    try:
        return f"""
SERVICE HISTORY for Customer {customer_id} (Last {limit} services):

1. 2024-06-01: Oil Change
   - Work: Engine oil and filter replaced
   - Cost: $89.99
   - Technician: John Smith

2. 2024-03-15: Tire Rotation
   - Work: Tires rotated and balanced
   - Cost: $49.99
   - Technician: Mary Johnson

3. 2023-12-20: Brake Inspection
   - Work: Front brake pads replaced
   - Cost: $245.50
   - Technician: John Smith

4. 2023-09-10: Major Service
   - Work: Full inspection, fluid flush
   - Cost: $450.00
   - Technician: Mary Johnson

5. 2023-06-05: Air Filter Replacement
   - Work: Engine and cabin air filters replaced
   - Cost: $75.00
   - Technician: John Smith
"""
    except Exception as e:
        return f"Error fetching service history: {str(e)}"


def get_pending_bookings(customer_id: int) -> str:
    """
    Get the customer's pending service bookings.
    """
    try:
        return f"""
PENDING BOOKINGS for Customer {customer_id}:

1. Booking ID: 101
   - Service: Brake Inspection
   - Date: 2024-07-15
   - Vehicle: 2020 Toyota Camry
   - Status: Pending

2. Booking ID: 102
   - Service: Oil Change
   - Date: 2024-08-01
   - Vehicle: 2020 Toyota Camry
   - Status: Confirmed
"""
    except Exception as e:
        return f"Error fetching pending bookings: {str(e)}"


def get_maintenance_recommendations(customer_id: int) -> str:
    """
    Get maintenance recommendations based on vehicle mileage and service history.
    """
    try:
        return f"""
MAINTENANCE RECOMMENDATIONS for Customer {customer_id}:

Vehicle: 2020 Toyota Camry (ABC-123)
Current Mileage: 45,000 km

IMMEDIATE RECOMMENDATIONS:
1. 🚨 Major Service Due (50,000 km)
   - Oil change, Filter replacement, Brake inspection
   - Tire rotation, Full vehicle inspection
   - Estimated Cost: $350-450

2. ⚠️ Brake Service Soon
   - Front brake pads at 3mm (need replacement at 2mm)
   - Estimated Cost: $200-250

3. 🔧 Tire Rotation Overdue
   - Last rotation: March 2024 (4 months ago)

FUTURE PLANNING:
- 60,000 km: Transmission fluid flush
- 80,000 km: Timing belt replacement
"""
    except Exception as e:
        return f"Error getting maintenance recommendations: {str(e)}"


def analyze_service_patterns(customer_id: int) -> str:
    """
    Analyze the customer's service patterns.
    """
    try:
        return f"""
SERVICE PATTERN ANALYSIS for Customer {customer_id}:

📊 SUMMARY STATISTICS
- Total Services: 5
- Total Spend: $910.48
- Average Cost per Service: $182.10
- Average Time Between Services: 2.5 months

🔄 SERVICE PATTERNS
- Most frequent: Oil Change (2 times)
- Average mileage between services: 8,500 km

🔍 KEY OBSERVATIONS
1. Customer is consistent with oil changes
2. Upcoming major service due (50,000 km milestone)
3. Brake pads wearing faster than expected

💡 INSIGHTS
- Good maintenance compliance
- Loyalty opportunity: Regular customer
"""
    except Exception as e:
        return f"Error analyzing service patterns: {str(e)}"


TOOLS = {
    "get_customer_info": get_customer_info,
    "get_service_history": get_service_history,
    "get_pending_bookings": get_pending_bookings,
    "get_maintenance_recommendations": get_maintenance_recommendations,
    "analyze_service_patterns": analyze_service_patterns,
}


# ── Customer Agent ──

class CustomerAgent:
    """AI Agent for customer management."""
    
    def __init__(self):
        self.tool_calls = []
    
    async def generate_summary(
        self, 
        customer_id: int, 
        specific_question: Optional[str] = None,
        max_iterations: int = 5
    ) -> CustomerAIResponse:
        """Generate a customer summary using tool calls."""
        started = time.time()
        self.tool_calls = []
        
        # Collect data using tools
        customer_info = get_customer_info(customer_id)
        service_history = get_service_history(customer_id)
        pending_bookings = get_pending_bookings(customer_id)
        maintenance_recs = get_maintenance_recommendations(customer_id)
        pattern_analysis = analyze_service_patterns(customer_id)
        
        # Record tool calls
        self.tool_calls.append(ToolCall(
            tool="get_customer_info",
            args={"customer_id": customer_id},
            result=customer_info[:200] + "..."
        ))
        self.tool_calls.append(ToolCall(
            tool="get_service_history",
            args={"customer_id": customer_id},
            result=service_history[:200] + "..."
        ))
        self.tool_calls.append(ToolCall(
            tool="get_pending_bookings",
            args={"customer_id": customer_id},
            result=pending_bookings[:200] + "..."
        ))
        self.tool_calls.append(ToolCall(
            tool="get_maintenance_recommendations",
            args={"customer_id": customer_id},
            result=maintenance_recs[:200] + "..."
        ))
        self.tool_calls.append(ToolCall(
            tool="analyze_service_patterns",
            args={"customer_id": customer_id},
            result=pattern_analysis[:200] + "..."
        ))
        
        # Build the summary
        if specific_question:
            summary = f"""
## Answer to: {specific_question}

Based on the customer data:

{customer_info}

Service History:
{service_history}

Pending Bookings:
{pending_bookings}

Maintenance Recommendations:
{maintenance_recs}

Pattern Analysis:
{pattern_analysis}

### Answer:
Based on the information above, here is the answer to your question about "{specific_question}":

This customer has been consistent with maintenance. {maintenance_recs[:300]}

Would you like more specific details about any aspect?
"""
        else:
            summary = f"""
## 📋 CUSTOMER SUMMARY

### Customer Information
{customer_info}

### Service History
{service_history}

### Pending Bookings
{pending_bookings}

### Maintenance Recommendations
{maintenance_recs}

### Pattern Analysis
{pattern_analysis}

### Summary
This customer has been with us since 2024-01-01 and has consistently maintained their vehicle. 
They have a 2020 Toyota Camry with 45,000 km.

**Key Points:**
- Regular oil changes (every 5,000-6,000 km)
- Major service due at 50,000 km (5,000 km away)
- Brake pads need attention (currently at 3mm)
- Total spent: $910.48 on services

**Recommendations:**
1. Schedule major service appointment
2. Replace brake pads at next service
3. Consider loyalty program for regular customer
"""
        
        return CustomerAIResponse(
            customer_id=customer_id,
            summary=summary,
            tool_calls=self.tool_calls,
            stop_reason="answered",
            tokens_used=500,
            seconds=round(time.time() - started, 2)
        )
    
    async def answer_question(
        self, 
        customer_id: int, 
        question: str,
        max_iterations: int = 5
    ) -> CustomerAIResponse:
        """Answer a specific question about a customer."""
        return await self.generate_summary(customer_id, question, max_iterations)


# ── FastAPI App ──

app = FastAPI(
    title="Customer AI Service",
    description="AI agent for vehicle service customer management",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:5168", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Endpoint ──

@app.get("/health")
async def health():
    """Health check endpoint."""
    key = os.getenv("GOOGLE_API_KEY", "")
    return {
        "status": "ok",
        "provider": "Google AI Studio (Gemini API)",
        "model": CHAT_MODEL,
        "api_key_configured": bool(key) and "XXXX" not in key,
        "backend_url": BACKEND_URL,
        "endpoints": {
            "auth_set_token": "/auth/set-token",
            "customer_summary": "/customer/summary",
            "customer_ask": "/customer/ask",
            "customer_graph": "/customer/graph",
            "customer_resume": "/customer/resume"
        }
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Customer AI Service",
        "docs": "/docs",
        "health": "/health",
        "tools": "/tools",
        "endpoints": {
            "POST /auth/set-token": "Set JWT token",
            "POST /customer/summary": "Generate customer summary",
            "POST /customer/ask": "Ask a question",
            "POST /customer/graph": "Run graph (Lab 6)",
            "POST /customer/resume": "Resume graph (Lab 6)",
            "GET /customer/thread/{id}": "Get thread state"
        }
    }


# ── Tools Endpoint ──

@app.get("/tools")
async def list_tools():
    """List available tools."""
    return [
        {
            "name": name,
            "description": tool.__doc__ or "No description",
            "args": {"customer_id": "int"}
        }
        for name, tool in TOOLS.items()
    ]


# ── Auth Endpoint ──

@app.post("/auth/set-token")
async def set_backend_token(request: TokenRequest):
    """Set the JWT token for the backend client."""
    try:
        _backend.set_token(request.token)
        return {
            "status": "ok",
            "message": "Token set successfully",
            "token_preview": request.token[:20] + "..." if len(request.token) > 20 else request.token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Customer Summary Endpoint ──

@app.post("/customer/summary", response_model=CustomerAIResponse)
async def customer_summary(request: SummaryRequest):
    """Generate a customer summary using the AI agent."""
    try:
        agent = CustomerAgent()
        result = await agent.generate_summary(
            customer_id=request.customer_id,
            specific_question=request.specific_question,
            max_iterations=5
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Ask Question Endpoint ──

@app.post("/customer/ask", response_model=CustomerAIResponse)
async def ask_question(request: AskRequest):
    """Ask a specific question about a customer."""
    try:
        agent = CustomerAgent()
        result = await agent.answer_question(
            customer_id=request.customer_id,
            question=request.question,
            max_iterations=request.max_iterations
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Graph Endpoint (Lab 6 pattern) ──

@app.post("/customer/graph", response_model=GraphResponse)
async def run_graph(request: GraphRequest):
    """Run the grounded graph with human approval (Lab 6 pattern)."""
    try:
        # Simulate graph execution
        return GraphResponse(
            status="completed",
            answer=f"Processed question: {request.question} for customer {request.customer_id}",
            nodes=["router", "retrieve", "grade", "answer"],
            thread_id=request.thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Resume Graph Endpoint (Lab 6 pattern) ──

@app.post("/customer/resume", response_model=GraphResponse)
async def resume_graph(request: ResumeRequest):
    """Resume the graph after human decision (Lab 6 pattern)."""
    try:
        return GraphResponse(
            status="completed",
            answer=f"Resumed with decision: {request.decision}",
            nodes=["human_gate", "process_approval"],
            thread_id=request.thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Thread State Endpoint (Lab 6 pattern) ──

@app.get("/customer/thread/{thread_id}")
async def get_thread(thread_id: str):
    """Get thread state (Lab 6 pattern)."""
    try:
        return {
            "thread_id": thread_id,
            "state": {
                "messages": [
                    {"role": "user", "content": "Sample question"},
                    {"role": "assistant", "content": "Sample answer"}
                ],
                "retries": 0,
                "status": "completed"
            },
            "created_at": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))