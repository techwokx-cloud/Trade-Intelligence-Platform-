"""
Data Ingestion Agent
Uses IBM Granite 20B Multilingual model for data ingestion and processing
Handles multilingual data, document parsing, entity extraction, and trade document verification
Supports multiple international trade frameworks and languages
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from loguru import logger

from ..models.base_agent import (
    BaseAgent,
    AgentType,
    AgentContext,
    AgentResult
)


class DataIngestionAgent(BaseAgent):
    """
    🕵️‍♂️ Data Ingestion Agent
    
    Responsibilities:
    - Ingest data from multiple sources
    - Process multilingual content (10+ international languages)
    - Parse and structure trade documents
    - Extract entities and key information
    - Normalize data formats
    - Support multiple trade frameworks
    """
    
    def __init__(
        self,
        agent_id: str = "data-ingestion-001",
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize Data Ingestion Agent"""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.DATA_INGESTION,
            model_name="ibm/granite-20b-multilingual",
            config=config
        )
        
        self.supported_languages = [
            "en", "fr", "pt", "ar", "sw",  # Major African languages
            "am", "ha", "yo", "ig", "zu"
        ]
        
        logger.info(f"Data Ingestion Agent initialized with multilingual support: {self.supported_languages}")
    
    async def validate_input(self, context: AgentContext) -> bool:
        """
        Validate input context for ingestion
        
        Args:
            context: Input context to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if context has required fields
            if not context.data:
                logger.warning("Empty data in context")
                return False
            
            # Validate data source type
            source_type = context.data.get("source_type")
            if source_type not in ["border_ports", "commodity_prices", "web_scrape", "document"]:
                logger.warning(f"Invalid source type: {source_type}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Input validation error: {str(e)}")
            return False
    
    async def process(self, context: AgentContext) -> AgentResult:
        """
        Process ingestion request
        
        Args:
            context: Input context with data source information
            
        Returns:
            AgentResult with ingested and normalized data
        """
        source_type = context.data.get("source_type")
        
        logger.info(f"Processing {source_type} data ingestion")
        
        try:
            if source_type == "border_ports":
                result_data = await self._ingest_border_ports(context.data)
            elif source_type == "commodity_prices":
                result_data = await self._ingest_commodity_prices(context.data)
            elif source_type == "web_scrape":
                result_data = await self._ingest_web_data(context.data)
            elif source_type == "document":
                result_data = await self._ingest_document(context.data)
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
            
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                data=result_data
            )
            
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                data={},
                errors=[str(e)]
            )
    
    async def _ingest_border_ports(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingest live border port traffic data
        
        Args:
            data: Raw border port data
            
        Returns:
            Normalized port traffic data
        """
        logger.info("Ingesting border port traffic data")
        
        # Simulate data processing with Granite 20B Multilingual
        # In production, this would call the actual watsonx API
        
        ports_data = data.get("ports", [])
        processed_ports = []
        
        for port in ports_data:
            processed_port = {
                "port_id": port.get("id"),
                "port_name": port.get("name"),
                "country": port.get("country"),
                "congestion_level": self._calculate_congestion(port),
                "wait_time_hours": port.get("wait_time", 0),
                "active_manifests": port.get("manifests", 0),
                "timestamp": datetime.utcnow().isoformat(),
                "status": "operational" if port.get("operational", True) else "disrupted"
            }
            processed_ports.append(processed_port)
        
        return {
            "source": "border_ports",
            "total_ports": len(processed_ports),
            "ports": processed_ports,
            "ingestion_timestamp": datetime.utcnow().isoformat()
        }
    
    async def _ingest_commodity_prices(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingest regional commodity spot prices
        
        Args:
            data: Raw commodity price data
            
        Returns:
            Normalized commodity price data
        """
        logger.info("Ingesting commodity price data")
        
        commodities = data.get("commodities", [])
        processed_commodities = []
        
        for commodity in commodities:
            processed_commodity = {
                "commodity_id": commodity.get("id"),
                "commodity_name": commodity.get("name"),
                "category": commodity.get("category"),
                "price_usd": commodity.get("price"),
                "currency": commodity.get("currency", "USD"),
                "region": commodity.get("region"),
                "market": commodity.get("market"),
                "price_change_24h": commodity.get("change_24h", 0),
                "volume": commodity.get("volume", 0),
                "timestamp": datetime.utcnow().isoformat()
            }
            processed_commodities.append(processed_commodity)
        
        return {
            "source": "commodity_prices",
            "total_commodities": len(processed_commodities),
            "commodities": processed_commodities,
            "ingestion_timestamp": datetime.utcnow().isoformat()
        }
    
    async def _ingest_web_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingest data from web scraping (via Bright Data MCP)
        
        Args:
            data: Raw web scraping data
            
        Returns:
            Normalized web data
        """
        logger.info("Ingesting web scraping data")
        
        url = data.get("url")
        content = data.get("content", "")
        
        # Process multilingual content
        detected_language = self._detect_language(content)
        
        return {
            "source": "web_scrape",
            "url": url,
            "detected_language": detected_language,
            "content_length": len(content),
            "extracted_data": self._extract_structured_data(content),
            "ingestion_timestamp": datetime.utcnow().isoformat()
        }
    
    async def _ingest_document(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingest and process trade documents
        
        Args:
            data: Document data
            
        Returns:
            Processed document data
        """
        logger.info("Ingesting trade document")
        
        doc_type = data.get("document_type")
        content = data.get("content", "")
        
        return {
            "source": "document",
            "document_type": doc_type,
            "language": self._detect_language(content),
            "extracted_entities": self._extract_entities(content),
            "ingestion_timestamp": datetime.utcnow().isoformat()
        }
    
    def _calculate_congestion(self, port: Dict[str, Any]) -> str:
        """Calculate port congestion level"""
        wait_time = port.get("wait_time", 0)
        
        if wait_time < 2:
            return "low"
        elif wait_time < 6:
            return "medium"
        elif wait_time < 12:
            return "high"
        else:
            return "critical"
    
    def _detect_language(self, content: str) -> str:
        """
        Detect language of content
        In production, this would use Granite 20B Multilingual
        """
        # Simplified language detection
        # In production, use actual model inference
        return "en"  # Default to English
    
    def _extract_structured_data(self, content: str) -> Dict[str, Any]:
        """Extract structured data from unstructured content"""
        # Placeholder for actual extraction logic
        return {
            "entities": [],
            "key_values": {},
            "summary": content[:200] if len(content) > 200 else content
        }
    
    def _extract_entities(self, content: str) -> List[Dict[str, Any]]:
        """Extract named entities from content"""
        # Placeholder for actual entity extraction
        return []
    
    async def fetch_live_data(
        self,
        source: str,
        params: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Convenience method to fetch live data from a source
        
        Args:
            source: Data source type
            params: Optional parameters for the fetch
            
        Returns:
            AgentResult with fetched data
        """
        context = AgentContext(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            data={
                "source_type": source,
                **(params or {})
            }
        )
        
        return await self.execute(context)

# Legacy alias for backward compatibility
IngestionScoutAgent = DataIngestionAgent

# Made with Bob


# Legacy alias for backward compatibility
IngestionScoutAgent = DataIngestionAgent
