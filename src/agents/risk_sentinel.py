"""
Regulatory Validation Agent
Uses IBM Granite Guardian 3.0 model for risk assessment and security validation
Performs cryptographic sealing, anomaly detection, and regulatory validation
Supports multi-framework trade compliance validation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import json
from loguru import logger

from ..models.base_agent import (
    BaseAgent,
    AgentType,
    AgentContext,
    AgentResult
)


class RiskLevel:
    """Risk level constants"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RegulatoryValidationAgent(BaseAgent):
    """
    🛡️ Regulatory Validation Agent
    
    Responsibilities:
    - Assess trade transaction risks
    - Detect anomalies in transactions
    - Validate data integrity
    - Generate cryptographic seals
    - Monitor security threats
    - Validate regulatory compliance
    """
    
    def __init__(
        self,
        agent_id: str = "regulatory-validation-001",
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize Regulatory Validation Agent"""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.REGULATORY_VALIDATION,
            model_name="ibm/granite-guardian-3.0-8b",
            config=config
        )
        
        # Risk assessment thresholds
        self.risk_thresholds = {
            "transaction_amount": {
                "low": 10000,
                "medium": 50000,
                "high": 100000,
                "critical": 500000
            },
            "anomaly_score": {
                "low": 0.3,
                "medium": 0.5,
                "high": 0.7,
                "critical": 0.9
            }
        }
        
        # Known risk patterns
        self.risk_patterns = [
            "unusual_transaction_volume",
            "suspicious_origin",
            "blacklisted_entity",
            "tariff_evasion_indicator",
            "documentation_inconsistency"
        ]
        
        logger.info("Regulatory Validation Agent initialized with security protocols")
    
    async def validate_input(self, context: AgentContext) -> bool:
        """
        Validate input context for risk assessment
        
        Args:
            context: Input context to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            data = context.data
            
            # Check for required fields
            if "assessment_type" not in data:
                logger.warning("Missing assessment_type in context")
                return False
            
            # Validate assessment type
            valid_types = [
                "transaction_risk",
                "anomaly_detection",
                "integrity_check",
                "security_audit",
                "cryptographic_seal"
            ]
            
            if data["assessment_type"] not in valid_types:
                logger.warning(f"Invalid assessment type: {data['assessment_type']}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Input validation error: {str(e)}")
            return False
    
    async def process(self, context: AgentContext) -> AgentResult:
        """
        Process risk assessment request
        
        Args:
            context: Input context with data to assess
            
        Returns:
            AgentResult with risk assessment
        """
        assessment_type = context.data.get("assessment_type")
        
        logger.info(f"Processing {assessment_type} risk assessment")
        
        try:
            if assessment_type == "transaction_risk":
                result_data = await self._assess_transaction_risk(context.data)
            elif assessment_type == "anomaly_detection":
                result_data = await self._detect_anomalies(context.data)
            elif assessment_type == "integrity_check":
                result_data = await self._check_integrity(context.data)
            elif assessment_type == "security_audit":
                result_data = await self._security_audit(context.data)
            elif assessment_type == "cryptographic_seal":
                result_data = await self._generate_cryptographic_seal(context.data)
            else:
                raise ValueError(f"Unsupported assessment type: {assessment_type}")
            
            # Add warnings if high risk detected
            warnings = []
            risk_level = result_data.get("risk_level")
            if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                warnings.append(f"High risk detected: {risk_level}")
            
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                data=result_data,
                warnings=warnings
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
    
    async def _assess_transaction_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess risk level of a transaction
        
        Args:
            data: Transaction data
            
        Returns:
            Risk assessment results
        """
        logger.info("Assessing transaction risk")
        
        transaction = data.get("transaction", {})
        amount = transaction.get("amount", 0)
        origin = transaction.get("origin_country")
        destination = transaction.get("destination_country")
        commodity = transaction.get("commodity")
        
        # Calculate risk factors
        amount_risk = self._calculate_amount_risk(amount)
        origin_risk = self._calculate_origin_risk(origin)
        commodity_risk = self._calculate_commodity_risk(commodity)
        
        # Aggregate risk score
        risk_score = (amount_risk + origin_risk + commodity_risk) / 3
        risk_level = self._determine_risk_level(risk_score)
        
        risk_factors = []
        if amount_risk > 0.5:
            risk_factors.append(f"High transaction amount: ${amount:,.2f}")
        if origin_risk > 0.5:
            risk_factors.append(f"Origin country risk: {origin}")
        if commodity_risk > 0.5:
            risk_factors.append(f"Commodity risk: {commodity}")
        
        return {
            "assessment_type": "transaction_risk",
            "risk_level": risk_level,
            "risk_score": round(risk_score, 3),
            "risk_factors": risk_factors,
            "details": {
                "amount_risk": round(amount_risk, 3),
                "origin_risk": round(origin_risk, 3),
                "commodity_risk": round(commodity_risk, 3)
            },
            "recommendations": self._generate_risk_recommendations(risk_level, risk_factors),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _detect_anomalies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect anomalies in trade data
        
        Args:
            data: Trade data to analyze
            
        Returns:
            Anomaly detection results
        """
        logger.info("Detecting anomalies")
        
        transactions = data.get("transactions", [])
        detected_anomalies = []
        
        for idx, transaction in enumerate(transactions):
            anomaly_score = self._calculate_anomaly_score(transaction)
            
            if anomaly_score > self.risk_thresholds["anomaly_score"]["medium"]:
                detected_anomalies.append({
                    "transaction_id": transaction.get("id", f"tx_{idx}"),
                    "anomaly_score": round(anomaly_score, 3),
                    "anomaly_type": self._identify_anomaly_type(transaction),
                    "details": transaction
                })
        
        risk_level = RiskLevel.LOW
        if detected_anomalies:
            max_score = max(a["anomaly_score"] for a in detected_anomalies)
            risk_level = self._determine_risk_level(max_score)
        
        return {
            "assessment_type": "anomaly_detection",
            "risk_level": risk_level,
            "total_transactions": len(transactions),
            "anomalies_detected": len(detected_anomalies),
            "anomalies": detected_anomalies,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _check_integrity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check data integrity
        
        Args:
            data: Data to verify
            
        Returns:
            Integrity check results
        """
        logger.info("Checking data integrity")
        
        payload = data.get("payload", {})
        expected_hash = data.get("expected_hash")
        
        # Calculate actual hash
        actual_hash = self._calculate_hash(payload)
        
        integrity_valid = (expected_hash == actual_hash) if expected_hash else True
        
        return {
            "assessment_type": "integrity_check",
            "integrity_valid": integrity_valid,
            "actual_hash": actual_hash,
            "expected_hash": expected_hash,
            "risk_level": RiskLevel.LOW if integrity_valid else RiskLevel.CRITICAL,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _security_audit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive security audit
        
        Args:
            data: Data to audit
            
        Returns:
            Security audit results
        """
        logger.info("Performing security audit")
        
        # Run multiple security checks
        transaction_risk = await self._assess_transaction_risk(data)
        anomaly_check = await self._detect_anomalies(data)
        integrity_check = await self._check_integrity(data)
        
        # Aggregate security score
        all_checks = [transaction_risk, anomaly_check, integrity_check]
        security_score = self._calculate_security_score(all_checks)
        
        overall_risk = self._determine_overall_risk([
            transaction_risk.get("risk_level"),
            anomaly_check.get("risk_level"),
            integrity_check.get("risk_level")
        ])
        
        return {
            "assessment_type": "security_audit",
            "risk_level": overall_risk,
            "security_score": security_score,
            "checks": {
                "transaction_risk": transaction_risk,
                "anomaly_detection": anomaly_check,
                "integrity_check": integrity_check
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _generate_cryptographic_seal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cryptographic seal for data
        
        Args:
            data: Data to seal
            
        Returns:
            Cryptographic seal information
        """
        logger.info("Generating cryptographic seal")
        
        payload = data.get("payload", {})
        
        # Generate multiple hashes for verification
        sha256_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()
        
        sha512_hash = hashlib.sha512(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()
        
        # Create seal metadata
        seal = {
            "seal_id": f"seal_{datetime.utcnow().timestamp()}",
            "algorithm": "SHA-256/SHA-512",
            "sha256": sha256_hash,
            "sha512": sha512_hash,
            "sealed_at": datetime.utcnow().isoformat(),
            "sealed_by": self.agent_id,
            "payload_size": len(json.dumps(payload))
        }
        
        return {
            "assessment_type": "cryptographic_seal",
            "seal": seal,
            "risk_level": RiskLevel.LOW,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _calculate_amount_risk(self, amount: float) -> float:
        """Calculate risk based on transaction amount"""
        thresholds = self.risk_thresholds["transaction_amount"]
        
        if amount < thresholds["low"]:
            return 0.1
        elif amount < thresholds["medium"]:
            return 0.3
        elif amount < thresholds["high"]:
            return 0.6
        elif amount < thresholds["critical"]:
            return 0.8
        else:
            return 1.0
    
    def _calculate_origin_risk(self, origin: Optional[str]) -> float:
        """Calculate risk based on origin country"""
        # Simplified risk calculation
        # In production, use actual risk database
        high_risk_countries = ["XX", "YY", "ZZ"]  # Placeholder
        
        if origin in high_risk_countries:
            return 0.8
        return 0.2
    
    def _calculate_commodity_risk(self, commodity: Optional[str]) -> float:
        """Calculate risk based on commodity type"""
        # Simplified risk calculation
        high_risk_commodities = ["weapons", "drugs", "precious_metals"]
        
        if commodity in high_risk_commodities:
            return 0.9
        return 0.1
    
    def _calculate_anomaly_score(self, transaction: Dict[str, Any]) -> float:
        """Calculate anomaly score for a transaction"""
        # Simplified anomaly detection
        # In production, use ML model
        score = 0.0
        
        # Check for unusual patterns
        if transaction.get("amount", 0) > 100000:
            score += 0.3
        
        if not transaction.get("documentation"):
            score += 0.4
        
        return min(score, 1.0)
    
    def _identify_anomaly_type(self, transaction: Dict[str, Any]) -> str:
        """Identify type of anomaly"""
        if transaction.get("amount", 0) > 100000:
            return "unusual_transaction_volume"
        if not transaction.get("documentation"):
            return "documentation_inconsistency"
        return "unknown"
    
    def _calculate_hash(self, data: Any) -> str:
        """Calculate SHA-256 hash of data"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level from score"""
        thresholds = self.risk_thresholds["anomaly_score"]
        
        if score < thresholds["low"]:
            return RiskLevel.LOW
        elif score < thresholds["medium"]:
            return RiskLevel.MEDIUM
        elif score < thresholds["high"]:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _determine_overall_risk(self, risk_levels: List[str]) -> str:
        """Determine overall risk from multiple assessments"""
        if RiskLevel.CRITICAL in risk_levels:
            return RiskLevel.CRITICAL
        elif RiskLevel.HIGH in risk_levels:
            return RiskLevel.HIGH
        elif RiskLevel.MEDIUM in risk_levels:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _calculate_security_score(self, checks: List[Dict[str, Any]]) -> float:
        """Calculate overall security score"""
        # Simplified scoring
        risk_weights = {
            RiskLevel.LOW: 1.0,
            RiskLevel.MEDIUM: 0.7,
            RiskLevel.HIGH: 0.4,
            RiskLevel.CRITICAL: 0.0
        }
        
        scores = [
            risk_weights.get(check.get("risk_level", RiskLevel.LOW), 0.5)
            for check in checks
        ]
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _generate_risk_recommendations(
        self,
        risk_level: str,
        risk_factors: List[str]
    ) -> List[str]:
        """Generate recommendations based on risk assessment"""
        if risk_level == RiskLevel.LOW:
            return ["Transaction appears normal. Proceed with standard processing."]
        
        recommendations = [
            f"Risk level: {risk_level.upper()}",
            "Recommended actions:"
        ]
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.extend([
                "- Conduct enhanced due diligence",
                "- Verify all documentation",
                "- Contact compliance officer",
                "- Consider transaction hold pending review"
            ])
        else:
            recommendations.extend([
                "- Review transaction details",
                "- Verify documentation completeness"
            ])
        
        if risk_factors:
            recommendations.append("Risk factors identified:")
            recommendations.extend([f"  - {factor}" for factor in risk_factors])
        return recommendations


# Legacy alias for backward compatibility
RiskSentinelAgent = RegulatoryValidationAgent

# Made with Bob
