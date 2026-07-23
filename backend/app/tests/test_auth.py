"""Tests for auth endpoints — login, me, permissions."""

from __future__ import annotations

import pytest


@pytest.mark.anyio
class TestAuth:
    async def test_login_success(self, client, test_user):
        resp = await client.post(
            "/v1/auth/login",
            data={"username": test_user["email"], "password": test_user["password"]},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0

    async def test_login_wrong_password(self, client, test_user):
        resp = await client.post(
            "/v1/auth/login",
            data={"username": test_user["email"], "password": "wrongpass"},
        )
        assert resp.status_code == 401

    async def test_login_nonexistent_user(self, client):
        resp = await client.post(
            "/v1/auth/login",
            data={"username": "noone@test.com", "password": "testpass123"},
        )
        assert resp.status_code == 401

    async def test_me_endpoint(self, client, auth_headers):
        resp = await client.get("/v1/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "id" in data
        assert data["role"] == "admin"

    async def test_me_without_token(self, client):
        resp = await client.get("/v1/auth/me")
        assert resp.status_code == 401

    async def test_permissions_endpoint(self, client, auth_headers):
        resp = await client.get("/v1/auth/me/permissions", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "permissions" in data
        assert "user:read" in data["permissions"]
