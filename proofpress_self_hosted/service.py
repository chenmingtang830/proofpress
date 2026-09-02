#!/usr/bin/env python3
"""HTTP service for the single-owner Proofpress self-hosting reference."""
from __future__ import annotations

import argparse
from html import escape
import json
import os
from pathlib import Path
import secrets
import sqlite3
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import proofpress_knowledge as knowledge
from proofpress_self_hosted import assistant as owner_assistant
from proofpress_self_hosted.control_plane import HostedAuthError, HostedControlPlane


MAX_REQUEST_BYTES = 1024 * 1024
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}
