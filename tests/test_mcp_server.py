"""Smoke test the web3sentinel-corpus MCP server via real stdio handshake."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_search_and_read():
    repo_root = Path(__file__).resolve().parent.parent
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
        cwd=str(repo_root),
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            names = {t.name for t in tools.tools}
            assert {"search_corpus", "read_corpus_entry", "list_synthesis_notes", "corpus_stats"} <= names

            stats_result = await session.call_tool("corpus_stats", {})
            text = stats_result.content[0].text
            assert '"total"' in text
            assert "swc" in text

            hits = await session.call_tool("search_corpus", {"query": "reentrancy", "top_k": 3})
            hits_text = hits.content[0].text
            assert "swc-107" in hits_text

            entry = await session.call_tool("read_corpus_entry", {"entry_id": "swc-107"})
            assert "Reentrancy" in entry.content[0].text
