import logging

from api.auth.users import current_active_user
from fastapi import Depends, HTTPException

logger = logging.getLogger()


class RoleChecker:
    """Lightweight Class to check a user permission set against
    the set of allowed roles on an endpoint or router."""

    def __init__(self, allowed_roles: set):
        self.allowed_roles = allowed_roles

    def __call__(self, user=Depends(current_active_user)):
        if not set(user.roles).isdisjoint(self.allowed_roles):
            logger.debug(
                f"User {user.email} with roles {user.roles} not in {self.allowed_roles}"
            )
            raise HTTPException(status_code=403, detail="Operation not permitted")
