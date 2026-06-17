"""
Compliance Intelligence Agent
Uses IBM Granite 3.0 8B Instruct model for multi-framework trade compliance checking
Validates trade regulations, tariffs, and cross-border requirements across multiple frameworks
Supports: AfCFTA, WTO, country-specific regulations, and extensible to USMCA, EU, ASEAN, GCC
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from ..models.base_agent import (
    BaseAgent,
    AgentType,
    AgentContext,
    AgentResult
)


class ComplianceIntelligenceAgent(BaseAgent):
    """
    ⚖️ Compliance Intelligence Agent
    
    Responsibilities:
    - Validate multi-framework trade compliance (AfCFTA, WTO, etc.)
    - Check tariff regulations across frameworks
    - Verify documentation requirements
    - Assess regulatory risks
    - Generate compliance reports
    - Support extensible framework architecture
    """
    
    def __init__(
        self,
        agent_id: str = "compliance-intelligence-001",
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize Compliance Intelligence Agent"""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.COMPLIANCE_INTELLIGENCE,
            model_name="ibm/granite-3.0-8b-instruct",
            config=config
        )
        
        # Multi-framework compliance rules database
        self.compliance_rules = {
            "AfCFTA": {
                "tariff_elimination": {
                    "phase1": {"percentage": 90, "deadline": "2024-01-01"},
                    "phase2": {"percentage": 97, "deadline": "2029-01-01"}
                },
                "rules_of_origin": {
                    "minimum_local_content": 0.35,  # 35% minimum
                    "substantial_transformation": True
                },
                "documentation": [
                    "certificate_of_origin",
                    "commercial_invoice",
                    "packing_list",
                    "bill_of_lading"
                ]
            },
            "WTO": {
                "tariff_elimination": {
                    "most_favored_nation": True,
                    "national_treatment": True
                },
                "rules_of_origin": {
                    "minimum_local_content": 0.30,
                    "substantial_transformation": True
                },
                "documentation": [
                    "certificate_of_origin",
                    "commercial_invoice",
                    "customs_declaration"
                ]
            },
            # Extensible to USMCA, EU, ASEAN, GCC
        }
        
        logger.info("Compliance Intelligence Agent initialized with multi-framework support")
    
    async def validate_input(self, context: AgentContext) -> bool:
        """
        Validate input context for compliance checking
        
        Args:
            context: Input context to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            data = context.data
            
            # Check for required fields
            required_fields = ["check_type"]
            for field in required_fields:
                if field not in data:
                    logger.warning(f"Missing required field: {field}")
                    return False
            
            # Validate check type
            valid_check_types = [
                "tariff_compliance",
                "documentation_check",
                "rules_of_origin",
                "full_compliance_audit"
            ]
            
            if data["check_type"] not in valid_check_types:
                logger.warning(f"Invalid check type: {data['check_type']}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Input validation error: {str(e)}")
            return False
    
    async def process(self, context: AgentContext) -> AgentResult:
        """
        Process compliance check request
        
        Args:
            context: Input context with trade data
            
        Returns:
            AgentResult with compliance assessment
        """
        check_type = context.data.get("check_type")
        
        logger.info(f"Processing {check_type} compliance check")
        
        try:
            if check_type == "tariff_compliance":
                result_data = await self._check_tariff_compliance(context.data)
            elif check_type == "documentation_check":
                result_data = await self._check_documentation(context.data)
            elif check_type == "rules_of_origin":
                result_data = await self._check_rules_of_origin(context.data)
            elif check_type == "full_compliance_audit":
                result_data = await self._full_compliance_audit(context.data)
            else:
                raise ValueError(f"Unsupported check type: {check_type}")
            
            # Determine overall compliance status
            is_compliant = result_data.get("compliance_status") == "compliant"
            warnings = result_data.get("warnings", [])
            
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                data=result_data,
                warnings=warnings if not is_compliant else []
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
    
    async def _check_tariff_compliance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check tariff compliance with specified trade framework
        
        Args:
            data: Trade data including tariff information and framework
            
        Returns:
            Tariff compliance assessment
        """
        logger.info("Checking tariff compliance")
        
        framework = data.get("framework", "AfCFTA")
        commodity = data.get("commodity", {})
        origin_country = data.get("origin_country")
        destination_country = data.get("destination_country")
        tariff_rate = data.get("tariff_rate", 0)
        
        # Check against specified framework tariff schedule
        expected_tariff = self._calculate_expected_tariff(
            framework,
            commodity.get("category"),
            origin_country,
            destination_country
        )
        
        is_compliant = tariff_rate <= expected_tariff
        
        return {
            "check_type": "tariff_compliance",
            "framework": framework,
            "compliance_status": "compliant" if is_compliant else "non_compliant",
            "details": {
                "commodity": commodity.get("name"),
                "origin": origin_country,
                "destination": destination_country,
                "applied_tariff": tariff_rate,
                "expected_tariff": expected_tariff,
                "difference": tariff_rate - expected_tariff
            },
            "recommendations": self._generate_tariff_recommendations(
                is_compliant,
                tariff_rate,
                expected_tariff
            ),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _check_documentation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if all required documentation is present for specified framework
        
        Args:
            data: Trade data including documents and framework
            
        Returns:
            Documentation compliance assessment
        """
        logger.info("Checking documentation compliance")
        
        framework = data.get("framework", "AfCFTA")
        provided_docs = data.get("documents", [])
        required_docs = self.compliance_rules.get(framework, {}).get("documentation", [])
        
        missing_docs = [doc for doc in required_docs if doc not in provided_docs]
        extra_docs = [doc for doc in provided_docs if doc not in required_docs]
        
        is_compliant = len(missing_docs) == 0
        
        return {
            "check_type": "documentation_check",
            "framework": framework,
            "compliance_status": "compliant" if is_compliant else "non_compliant",
            "details": {
                "required_documents": required_docs,
                "provided_documents": provided_docs,
                "missing_documents": missing_docs,
                "extra_documents": extra_docs
            },
            "warnings": [f"Missing required document: {doc}" for doc in missing_docs],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _check_rules_of_origin(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check rules of origin compliance for specified framework
        
        Args:
            data: Trade data including origin information and framework
            
        Returns:
            Rules of origin compliance assessment
        """
        logger.info("Checking rules of origin compliance")
        
        framework = data.get("framework", "AfCFTA")
        local_content = data.get("local_content_percentage", 0)
        substantial_transformation = data.get("substantial_transformation", False)
        
        min_content = self.compliance_rules.get(framework, {}).get("rules_of_origin", {}).get("minimum_local_content", 0.30)
        
        content_compliant = local_content >= min_content
        transformation_compliant = substantial_transformation
        
        is_compliant = content_compliant and transformation_compliant
        
        return {
            "check_type": "rules_of_origin",
            "framework": framework,
            "compliance_status": "compliant" if is_compliant else "non_compliant",
            "details": {
                "local_content_percentage": local_content,
                "minimum_required": min_content,
                "content_compliant": content_compliant,
                "substantial_transformation": substantial_transformation,
                "transformation_compliant": transformation_compliant
            },
            "warnings": self._generate_origin_warnings(
                content_compliant,
                transformation_compliant,
                local_content,
                min_content
            ),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _full_compliance_audit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform full compliance audit for specified framework
        
        Args:
            data: Complete trade data including framework
            
        Returns:
            Comprehensive compliance assessment
        """
        framework = data.get("framework", "AfCFTA")
        logger.info(f"Performing full compliance audit for {framework}")
        
        # Run all checks
        tariff_check = await self._check_tariff_compliance(data)
        doc_check = await self._check_documentation(data)
        origin_check = await self._check_rules_of_origin(data)
        
        # Aggregate results
        all_compliant = all([
            tariff_check["compliance_status"] == "compliant",
            doc_check["compliance_status"] == "compliant",
            origin_check["compliance_status"] == "compliant"
        ])
        
        all_warnings = (
            tariff_check.get("warnings", []) +
            doc_check.get("warnings", []) +
            origin_check.get("warnings", [])
        )
        
        return {
            "check_type": "full_compliance_audit",
            "framework": framework,
            "compliance_status": "compliant" if all_compliant else "non_compliant",
            "checks": {
                "tariff": tariff_check,
                "documentation": doc_check,
                "rules_of_origin": origin_check
            },
            "overall_score": self._calculate_compliance_score([
                tariff_check,
                doc_check,
                origin_check
            ]),
            "warnings": all_warnings,
            "recommendations": self._generate_audit_recommendations(all_warnings),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _calculate_expected_tariff(
        self,
        framework: str,
        category: str,
        origin: str,
        destination: str
    ) -> float:
        """Calculate expected tariff based on framework schedule"""
        # Simplified calculation - in production, use actual tariff database
        if framework == "AfCFTA":
            phase1_percentage = self.compliance_rules["AfCFTA"]["tariff_elimination"]["phase1"]["percentage"]
            return (100 - phase1_percentage) / 100 * 10  # Assume 10% base tariff
        elif framework == "WTO":
            # WTO MFN rates - simplified
            return 0.05  # 5% average MFN rate
        else:
            # Default calculation for unknown frameworks
            return 0.10  # 10% default
    
    def _generate_tariff_recommendations(
        self,
        is_compliant: bool,
        applied: float,
        expected: float
    ) -> List[str]:
        """Generate tariff compliance recommendations"""
        if is_compliant:
            return ["Tariff rate is compliant with AfCFTA regulations"]
        else:
            return [
                f"Reduce tariff rate from {applied}% to {expected}%",
                "Review AfCFTA tariff elimination schedule",
                "Consider applying for tariff exemption if eligible"
            ]
    
    def _generate_origin_warnings(
        self,
        content_compliant: bool,
        transformation_compliant: bool,
        local_content: float,
        min_content: float
    ) -> List[str]:
        """Generate rules of origin warnings"""
        warnings = []
        
        if not content_compliant:
            warnings.append(
                f"Local content ({local_content:.1%}) below minimum ({min_content:.1%})"
            )
        
        if not transformation_compliant:
            warnings.append("Substantial transformation requirement not met")
        
        return warnings
    
    def _calculate_compliance_score(self, checks: List[Dict[str, Any]]) -> float:
        """Calculate overall compliance score"""
        compliant_count = sum(
            1 for check in checks
            if check.get("compliance_status") == "compliant"
        )
        return (compliant_count / len(checks)) * 100 if checks else 0
    
    def _generate_audit_recommendations(self, warnings: List[str]) -> List[str]:
        """Generate recommendations based on audit warnings"""
        if not warnings:
            return ["All compliance checks passed. No action required."]
        
        recommendations = [
            "Address the following compliance issues:",
            *[f"- {warning}" for warning in warnings],
            "Consult with trade compliance specialist if needed"
        ]
        
        return recommendations


# Legacy alias for backward compatibility
ComplianceOfficerAgent = ComplianceIntelligenceAgent

# Made with Bob
