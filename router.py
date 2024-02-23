from fastapi import APIRouter

from app.controller import auth_controller, comment_controller, post_controller, user_controller

router = APIRouter(
    prefix="/api",
)

# AUTH
router.include_router(
    auth_controller.router,
)

# COMMENTS
router.include_router(
    comment_controller.router,
)

# POSTS
router.include_router(
    post_controller.router,
)

# USERS
router.include_router(
    user_controller.router,
)
