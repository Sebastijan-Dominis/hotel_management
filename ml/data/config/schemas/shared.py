"""Shared schema blocks reused by interim and processed data configs."""

import logging
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from ml.exceptions import ConfigError

logger = logging.getLogger(__name__)

class Output(BaseModel):
    """Output artifact settings for persisted datasets."""

    path_suffix: str = Field(..., description="Suffix for the output data file path, which will be combined with the data name and version to create the full path.")
    format: Literal["parquet"] = Field("parquet", description="Format to save the interim data (default: 'parquet').")
    compression: Literal['snappy', 'gzip', 'brotli', 'lz4', 'zstd'] | None = Field("snappy", description="Compression method to use when saving the data (default: 'snappy').")

class DataInfo(BaseModel):
    """Dataset identity and output target metadata."""

    name: str = Field(..., description="Name of the data being processed.")
    version: str = Field(..., description="Version of the interim data being created.")
    output: Output

    @field_validator("version", mode="before")
    @classmethod
    def validate_version_format(cls, v):
        """Ensure dataset version follows ``v{number}`` convention.

        Args:
            v: Dataset version value.

        Returns:
            str: Validated dataset version string.
        """

        if not isinstance(v, str) or not v.startswith("v") or not v[1:].isdigit():
            msg = f"Version must be in format 'v{{number}}', e.g. 'v1', 'v2', etc. Got '{v}'."
            logger.error(msg)
            raise ConfigError(msg)
        return v