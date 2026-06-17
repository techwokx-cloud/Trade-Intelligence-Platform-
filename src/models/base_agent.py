"""
Base Agent Interface and Abstract Classes
Defines the core structure for all Trade Intelligence Platform agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
import json
from loguru import logger


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class AgentType(Enum):
    """Types of agents in the system"""
    DATA_INGESTION = "data_ingestion"
    COMPLIANCE_INTELLIGENCE = "compliance_intelligence"
    REGULATORY_VALIDATION = "regulatory_validation"
    
    # Legacy aliases for backward compatibility
    INGESTION_SCOUT = "data_ingestion"
    COMPLIANCE_OFFICER = "compliance_intelligence"
    RISK_SENTINEL = "regulatory_validation"


@dataclass
class AgentContext:
    """Context data passed between agents"""
    
    agent_id: str
    agent_type: AgentType
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_context_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "metadata": self.metadata,
            "parent_context_id": self.parent_context_id
        }
    
    def get_hash(self) -> str:
        """Generate cryptographic hash of context"""
        context_str = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(context_str.encode()).hexdigest()


@dataclass
class AgentResult:
    """Result returned by agent execution"""
    
    success: bool
    agent_id: str
    agent_type: AgentType
    data: Dict[str, Any]
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    execution_time_ms: float = 0.0
    context_hash: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "success": self.success,
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "data": self.data,
            "errors": self.errors,
            "warnings": self.warnings,
            "execution_time_ms": self.execution_time_ms,
            "context_hash": self.context_hash,
            "timestamp": self.timestamp.isoformat()
        }


class BaseAgent(ABC):
    """
    Abstract base class for all Trade Intelligence Platform agents
    Implements common functionality and enforces interface contracts
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_type: AgentType,
        model_name: str,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize base agent
        
        Args:
            agent_id: Unique identifier for the agent
            agent_type: Type of agent (from AgentType enum)
            model_name: IBM Granite model to use
            config: Optional configuration dictionary
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.model_name = model_name
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self._execution_count = 0
        
        logger.info(f"Initialized {self.agent_type.value} agent: {self.agent_id}")
    
    @abstractmethod
    async def process(self, context: AgentContext) -> AgentResult:
        """
        Main processing method - must be implemented by subclasses
        
        Args:
            context: Input context with data to process
            
        Returns:
            AgentResult with processing outcome
        """
        pass
    
    @abstractmethod
    async def validate_input(self, context: AgentContext) -> bool:
        """
        Validate input context before processing
        
        Args:
            context: Input context to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    async def execute(self, context: AgentContext) -> AgentResult:
        """
        Execute agent with full lifecycle management
        
        Args:
            context: Input context
            
        Returns:
            AgentResult with execution outcome
        """
        start_time = datetime.utcnow()
        self.status = AgentStatus.RUNNING
        self._execution_count += 1
        
        try:
            # Validate input
            if not await self.validate_input(context):
                raise ValueError("Input validation failed")
            
            logger.info(f"Agent {self.agent_id} starting execution #{self._execution_count}")
            
            # Process
            result = await self.process(context)
            
            # Calculate execution time
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            result.execution_time_ms = execution_time
            result.context_hash = context.get_hash()
            
            self.status = AgentStatus.COMPLETED
            logger.info(f"Agent {self.agent_id} completed in {execution_time:.2f}ms")
            
            return result
            
        except Exception as e:
            self.status = AgentStatus.FAILED
            logger.error(f"Agent {self.agent_id} failed: {str(e)}")
            
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                data={},
                errors=[str(e)],
                execution_time_ms=execution_time,
                context_hash=context.get_hash()
            )
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "status": self.status.value,
            "model_name": self.model_name,
            "execution_count": self._execution_count
        }
    
    async def health_check(self) -> bool:
        """Perform health check on agent"""
        try:
            # Basic health check - can be extended by subclasses
            return self.status != AgentStatus.FAILED
        except Exception as e:
            logger.error(f"Health check failed for {self.agent_id}: {str(e)}")
            return False


class AgentRegistry:
    """Registry for managing agent instances"""
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
    
    def register(self, agent: BaseAgent) -> None:
        """Register an agent"""
        self._agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.agent_id}")
    
    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self._agents.get(agent_id)
    
    def get_all(self) -> List[BaseAgent]:
        """Get all registered agents"""
        return list(self._agents.values())
    
    def unregister(self, agent_id: str) -> bool:
        """Unregister an agent"""
        if agent_id in self._agents:
            del self._agents[agent_id]
            logger.info(f"Unregistered agent: {agent_id}")
            return True
        return False
    
    def get_status_all(self) -> List[Dict[str, Any]]:
        """Get status of all agents"""
        return [agent.get_status() for agent in self._agents.values()]


# Global registry instance
agent_registry = AgentRegistry()

# Made with Bob
