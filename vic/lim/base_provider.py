"""
===========================================================
AutoShortsAI
Video Intelligence Core (VIC)

Base LLM Provider
===========================================================

Abstract interface for Large Language Model providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    async def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Generate a response from an LLM.

        Parameters
        ----------
        system_prompt
            Instruction for the model.

        user_prompt
            User input.

        Returns
        -------
        str
            Raw response from the model.
        """
        raise NotImplementedError