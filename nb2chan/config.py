"""Config nb2chan."""
# pylint: disable=invalid-name, too-few-public-methods, no-self-argument, no-self-use
from typing import List, Union

from pydantic import BaseSettings, Field, validator

from logzero import logger


class Settings(BaseSettings):
    """Preset default valid tokens."""

    token_list: List[Union[str, int]] = Field(
        default_factory=lambda: ["DEMO_TOKEN", "SECRET_TOKEN"]
    )

    @validator("token_list")
    def validate_namelist(cls, v):
        """Validate."""
        res = []
        for elm in v:
            try:
                # may use numerbers
                elm = str(elm).strip()
            except Exception as exc:
                logger.error(exc)
                raise

            _ = """
            if len(elm) < 1:
                raise ValueError(
                    "Empty token not allowed"
                )
            """

            if len(elm) == 0:
                logger.warning(
                    "This entry [%s] is empty: probably not what you want, but we let it pass.",
                    elm,
                )

            res.append(elm)

        return res

    class Config:  # pylint: disable=too-few-public-methods
        """Config."""

        env_prefix = "nb2chan_"
        # extra = "allow"
        env_file = ".env.nb2chan"
        env_file_encoding = "utf-8"

        logger.info("env_prefix: %s, env_file: %s", env_prefix, env_file)
