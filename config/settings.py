"""
BantuMarket Configuration Settings
Centralized configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
from typing import Optional
import os


class WatsonXSettings(BaseSettings):
    """IBM watsonx Orchestrate Configuration"""
    
    api_key: str = Field(..., description="IBM watsonx API Key")
    project_id: str = Field(..., description="IBM watsonx Project ID")
    url: str = Field(default="https://us-south.ml.cloud.ibm.com", description="watsonx API URL")
    orchestrate_endpoint: str = Field(default="/v1/orchestrate/agents", description="Orchestrate endpoint path")
    
    model_config = SettingsConfigDict(env_prefix="WATSONX_")


class GraniteModels(BaseSettings):
    """IBM Granite Model Configuration"""
    
    multilingual_model: str = Field(default="ibm/granite-20b-multilingual", description="Multilingual model for ingestion")
    instruct_model: str = Field(default="ibm/granite-3.0-8b-instruct", description="Instruct model for compliance")
    guardian_model: str = Field(default="ibm/granite-guardian-3.0-8b", description="Guardian model for risk assessment")
    
    model_config = SettingsConfigDict(env_prefix="GRANITE_")


class BrightDataSettings(BaseSettings):
    """Bright Data MCP Gateway Configuration"""
    
    api_key: str = Field(..., description="Bright Data API Key")
    zone: str = Field(..., description="Bright Data Zone Name")
    host: str = Field(default="brd.superproxy.io", description="Bright Data Host")
    port: int = Field(default=22225, description="Bright Data Port")
    
    model_config = SettingsConfigDict(env_prefix="BRIGHT_DATA_")
    
    @property
    def proxy_url(self) -> str:
        """Generate proxy URL"""
        return f"http://{self.zone}:{self.api_key}@{self.host}:{self.port}"


class AppSettings(BaseSettings):
    """General Application Configuration"""
    
    name: str = Field(default="BantuMarket", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    environment: str = Field(default="development", description="Environment (development/staging/production)")
    log_level: str = Field(default="INFO", description="Logging level")
    
    model_config = SettingsConfigDict(env_prefix="APP_")


class SecuritySettings(BaseSettings):
    """Security Configuration"""
    
    secret_key: str = Field(..., description="Secret key for encryption")
    encryption_key: str = Field(..., description="Encryption key for sensitive data")
    
    model_config = SettingsConfigDict(env_prefix="")


class StreamlitSettings(BaseSettings):
    """Streamlit Dashboard Configuration"""
    
    server_port: int = Field(default=8501, description="Streamlit server port")
    server_address: str = Field(default="localhost", description="Streamlit server address")
    theme: str = Field(default="light", description="Dashboard theme")
    
    model_config = SettingsConfigDict(env_prefix="STREAMLIT_")


class RateLimitSettings(BaseSettings):
    """API Rate Limiting Configuration"""
    
    max_requests_per_minute: int = Field(default=60, description="Maximum requests per minute")
    max_concurrent_requests: int = Field(default=10, description="Maximum concurrent requests")
    
    model_config = SettingsConfigDict(env_prefix="")


class MonitoringSettings(BaseSettings):
    """Monitoring & Telemetry Configuration"""
    
    enable_prometheus: bool = Field(default=True, description="Enable Prometheus metrics")
    prometheus_port: int = Field(default=9090, description="Prometheus port")
    enable_logging: bool = Field(default=True, description="Enable detailed logging")
    
    model_config = SettingsConfigDict(env_prefix="")


class DataSourceSettings(BaseSettings):
    """AfCFTA Data Sources Configuration"""
    
    afcfta_api_endpoint: str = Field(..., description="AfCFTA API endpoint")
    border_ports_api: str = Field(..., description="Border ports API endpoint")
    commodity_prices_api: str = Field(..., description="Commodity prices API endpoint")
    
    model_config = SettingsConfigDict(env_prefix="")


class Settings(BaseSettings):
    """Master Settings Container"""
    
    watsonx: WatsonXSettings
    granite: GraniteModels
    bright_data: BrightDataSettings
    app: AppSettings
    security: SecuritySettings
    streamlit: StreamlitSettings
    rate_limit: RateLimitSettings
    monitoring: MonitoringSettings
    data_sources: DataSourceSettings
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def __init__(self, **kwargs):
        """Initialize all nested settings"""
        super().__init__(
            watsonx=WatsonXSettings(),
            granite=GraniteModels(),
            bright_data=BrightDataSettings(),
            app=AppSettings(),
            security=SecuritySettings(),
            streamlit=StreamlitSettings(),
            rate_limit=RateLimitSettings(),
            monitoring=MonitoringSettings(),
            data_sources=DataSourceSettings(),
            **kwargs
        )


# Global settings instance
def get_settings() -> Settings:
    """Get or create settings instance"""
    return Settings()


# Export for easy import
settings = get_settings()

# Made with Bob
