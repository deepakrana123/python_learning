from fastapi import APIRouter
from app.schemas.parser_schema import ParseRequest, ParseResponse

# from app.services.parser.parser import parse_workflow
from app.services.parser.metrics import metrics

router = APIRouter(prefix="/parse", tags=["Parser"])


@router.post("/", response_model=ParseResponse)
def parse_route(payload: ParseRequest):
    return parse_workflow(payload.raw_input)


@router.get("/metrics")
def get_metrics():
    return metrics
