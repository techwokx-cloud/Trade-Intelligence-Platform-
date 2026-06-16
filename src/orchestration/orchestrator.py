"""
IBM watsonx Orchestrate Integration
Manages agent lifecycle, routing, and execution coordination
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum
import asyncio
from loguru import logger

from ..models.base_agent import (
    BaseAgent,
    AgentContext,
    AgentResult,
    AgentType,
    agent_registry
)
from ..agents.ingestion_scout import IngestionScoutAgent
from ..agents.compliance_officer import ComplianceOfficerAgent
from ..agents.risk_sentinel import RiskSentinelAgent


class ExecutionMode(Enum):
    """Execution modes for agent orchestration"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"


class OrchestrationStatus(Enum):
    """Status of orchestration execution"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL_SUCCESS = "partial_success"


class AgentOrchestrator:
    """
    Main orchestrator for BantuMarket multi-agent system
    Coordinates execution flow between agents via IBM watsonx Orchestrate
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize orchestrator
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.execution_history: List[Dict[str, Any]] = []
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        
        # Initialize agents
        self.ingestion_scout = IngestionScoutAgent()
        self.compliance_officer = ComplianceOfficerAgent()
        self.risk_sentinel = RiskSentinelAgent()
        
        # Register agents
        agent_registry.register(self.ingestion_scout)
        agent_registry.register(self.compliance_officer)
        agent_registry.register(self.risk_sentinel)
        
        logger.info("Agent Orchestrator initialized with 3 agents")
    
    async def execute_workflow(
        self,
        workflow_id: str,
        initial_data: Dict[str, Any],
        mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    ) -> Dict[str, Any]:
        """
        Execute a complete workflow through all agents
        
        Args:
            workflow_id: Unique identifier for the workflow
            initial_data: Initial data to process
            mode: Execution mode (sequential/parallel/conditional)
            
        Returns:
            Workflow execution results
        """
        logger.info(f"Starting workflow {workflow_id} in {mode.value} mode")
        
        start_time = datetime.utcnow()
        self.active_workflows[workflow_id] = {
            "status": OrchestrationStatus.RUNNING.value,
            "start_time": start_time.isoformat()
        }
        
        try:
            if mode == ExecutionMode.SEQUENTIAL:
                result = await self._execute_sequential(workflow_id, initial_data)
            elif mode == ExecutionMode.PARALLEL:
                result = await self._execute_parallel(workflow_id, initial_data)
            elif mode == ExecutionMode.CONDITIONAL:
                result = await self._execute_conditional(workflow_id, initial_data)
            else:
                raise ValueError(f"Unsupported execution mode: {mode}")
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            workflow_result = {
                "workflow_id": workflow_id,
                "status": OrchestrationStatus.COMPLETED.value,
                "execution_time_seconds": execution_time,
                "mode": mode.value,
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.execution_history.append(workflow_result)
            self.active_workflows[workflow_id]["status"] = OrchestrationStatus.COMPLETED.value
            
            logger.info(f"Workflow {workflow_id} completed in {execution_time:.2f}s")
            
            return workflow_result
            
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            
            self.active_workflows[workflow_id]["status"] = OrchestrationStatus.FAILED.value
            
            return {
                "workflow_id": workflow_id,
                "status": OrchestrationStatus.FAILED.value,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _execute_sequential(
        self,
        workflow_id: str,
        initial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute agents sequentially: Ingestion → Compliance → Risk
        
        Args:
            workflow_id: Workflow identifier
            initial_data: Initial data
            
        Returns:
            Sequential execution results
        """
        logger.info("Executing sequential workflow")
        
        results = {}
        
        # Step 1: Ingestion Scout
        logger.info("Step 1: Ingestion Scout")
        ingestion_context = AgentContext(
            agent_id=self.ingestion_scout.agent_id,
            agent_type=AgentType.INGESTION_SCOUT,
            data=initial_data
        )
        ingestion_result = await self.ingestion_scout.execute(ingestion_context)
        results["ingestion"] = ingestion_result.to_dict()
        
        if not ingestion_result.success:
            logger.warning("Ingestion failed, stopping workflow")
            return results
        
        # Step 2: Compliance Officer (uses ingestion data)
        logger.info("Step 2: Compliance Officer")
        compliance_context = AgentContext(
            agent_id=self.compliance_officer.agent_id,
            agent_type=AgentType.COMPLIANCE_OFFICER,
            data={
                "check_type": "full_compliance_audit",
                **ingestion_result.data
            },
            parent_context_id=ingestion_context.get_hash()
        )
        compliance_result = await self.compliance_officer.execute(compliance_context)
        results["compliance"] = compliance_result.to_dict()
        
        # Step 3: Risk Sentinel (uses both previous results)
        logger.info("Step 3: Risk Sentinel")
        risk_context = AgentContext(
            agent_id=self.risk_sentinel.agent_id,
            agent_type=AgentType.RISK_SENTINEL,
            data={
                "assessment_type": "security_audit",
                "payload": {
                    "ingestion": ingestion_result.data,
                    "compliance": compliance_result.data
                }
            },
            parent_context_id=compliance_context.get_hash()
        )
        risk_result = await self.risk_sentinel.execute(risk_context)
        results["risk"] = risk_result.to_dict()
        
        # Generate cryptographic seal
        logger.info("Generating cryptographic seal")
        seal_context = AgentContext(
            agent_id=self.risk_sentinel.agent_id,
            agent_type=AgentType.RISK_SENTINEL,
            data={
                "assessment_type": "cryptographic_seal",
                "payload": results
            }
        )
        seal_result = await self.risk_sentinel.execute(seal_context)
        results["seal"] = seal_result.to_dict()
        
        return results
    
    async def _execute_parallel(
        self,
        workflow_id: str,
        initial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute agents in parallel where possible
        
        Args:
            workflow_id: Workflow identifier
            initial_data: Initial data
            
        Returns:
            Parallel execution results
        """
        logger.info("Executing parallel workflow")
        
        # First, run ingestion (required for others)
        ingestion_context = AgentContext(
            agent_id=self.ingestion_scout.agent_id,
            agent_type=AgentType.INGESTION_SCOUT,
            data=initial_data
        )
        ingestion_result = await self.ingestion_scout.execute(ingestion_context)
        
        if not ingestion_result.success:
            return {"ingestion": ingestion_result.to_dict()}
        
        # Run compliance and risk in parallel
        compliance_context = AgentContext(
            agent_id=self.compliance_officer.agent_id,
            agent_type=AgentType.COMPLIANCE_OFFICER,
            data={
                "check_type": "full_compliance_audit",
                **ingestion_result.data
            }
        )
        
        risk_context = AgentContext(
            agent_id=self.risk_sentinel.agent_id,
            agent_type=AgentType.RISK_SENTINEL,
            data={
                "assessment_type": "transaction_risk",
                "transaction": ingestion_result.data
            }
        )
        
        # Execute in parallel
        compliance_task = self.compliance_officer.execute(compliance_context)
        risk_task = self.risk_sentinel.execute(risk_context)
        
        compliance_result, risk_result = await asyncio.gather(
            compliance_task,
            risk_task
        )
        
        return {
            "ingestion": ingestion_result.to_dict(),
            "compliance": compliance_result.to_dict(),
            "risk": risk_result.to_dict()
        }
    
    async def _execute_conditional(
        self,
        workflow_id: str,
        initial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute agents conditionally based on results
        
        Args:
            workflow_id: Workflow identifier
            initial_data: Initial data
            
        Returns:
            Conditional execution results
        """
        logger.info("Executing conditional workflow")
        
        results = {}
        
        # Always start with ingestion
        ingestion_context = AgentContext(
            agent_id=self.ingestion_scout.agent_id,
            agent_type=AgentType.INGESTION_SCOUT,
            data=initial_data
        )
        ingestion_result = await self.ingestion_scout.execute(ingestion_context)
        results["ingestion"] = ingestion_result.to_dict()
        
        if not ingestion_result.success:
            return results
        
        # Run compliance check
        compliance_context = AgentContext(
            agent_id=self.compliance_officer.agent_id,
            agent_type=AgentType.COMPLIANCE_OFFICER,
            data={
                "check_type": "full_compliance_audit",
                **ingestion_result.data
            }
        )
        compliance_result = await self.compliance_officer.execute(compliance_context)
        results["compliance"] = compliance_result.to_dict()
        
        # Only run risk assessment if compliance issues detected
        if compliance_result.warnings or not compliance_result.success:
            logger.info("Compliance issues detected, running risk assessment")
            
            risk_context = AgentContext(
                agent_id=self.risk_sentinel.agent_id,
                agent_type=AgentType.RISK_SENTINEL,
                data={
                    "assessment_type": "security_audit",
                    "payload": {
                        "ingestion": ingestion_result.data,
                        "compliance": compliance_result.data
                    }
                }
            )
            risk_result = await self.risk_sentinel.execute(risk_context)
            results["risk"] = risk_result.to_dict()
        else:
            logger.info("No compliance issues, skipping detailed risk assessment")
            results["risk"] = {"skipped": True, "reason": "No compliance issues detected"}
        
        return results
    
    async def execute_single_agent(
        self,
        agent_type: AgentType,
        data: Dict[str, Any]
    ) -> AgentResult:
        """
        Execute a single agent
        
        Args:
            agent_type: Type of agent to execute
            data: Data to process
            
        Returns:
            Agent execution result
        """
        agent = self._get_agent_by_type(agent_type)
        
        context = AgentContext(
            agent_id=agent.agent_id,
            agent_type=agent_type,
            data=data
        )
        
        return await agent.execute(context)
    
    def _get_agent_by_type(self, agent_type: AgentType) -> BaseAgent:
        """Get agent instance by type"""
        if agent_type == AgentType.INGESTION_SCOUT:
            return self.ingestion_scout
        elif agent_type == AgentType.COMPLIANCE_OFFICER:
            return self.compliance_officer
        elif agent_type == AgentType.RISK_SENTINEL:
            return self.risk_sentinel
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a workflow"""
        return self.active_workflows.get(workflow_id)
    
    def get_execution_history(
        self,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get execution history"""
        if limit:
            return self.execution_history[-limit:]
        return self.execution_history
    
    def get_agent_status_all(self) -> List[Dict[str, Any]]:
        """Get status of all agents"""
        return agent_registry.get_status_all()
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all agents"""
        health_results = {}
        
        for agent in [self.ingestion_scout, self.compliance_officer, self.risk_sentinel]:
            health_results[agent.agent_id] = await agent.health_check()
        
        all_healthy = all(health_results.values())
        
        return {
            "orchestrator_healthy": True,
            "agents": health_results,
            "all_agents_healthy": all_healthy,
            "timestamp": datetime.utcnow().isoformat()
        }


# Global orchestrator instance
orchestrator = AgentOrchestrator()

# Made with Bob
