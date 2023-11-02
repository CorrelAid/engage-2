import uuid
from datetime import datetime
from typing import Annotated

from api.auth.users import current_active_user
from database.session import transactional_session
from fastapi import APIRouter, Depends, HTTPException, status
from models.comment import Comment
from models.user import User
from pydantic import BaseModel, ConfigDict, TypeAdapter
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class ReadComment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    text: str
    created_at: datetime | None
    created_by: uuid.UUID
    updated_at: datetime | None
    updated_by: uuid.UUID


class CreateComment(BaseModel):
    text: str


class UpdateComment(BaseModel):
    text: str


class CommentStore:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(transactional_session)],
        # user: Annotated[User, Depends(current_active_user)],
    ):
        self.session = session

    async def _get_orm_comment(self, comment_id: uuid.UUID) -> Comment:
        try:
            comment_entry = (
                await self.session.execute(select(Comment).filter_by(id=comment_id))
            ).scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return comment_entry

    async def get(self, comment_id: uuid.UUID) -> ReadComment:
        comment_entry = await self._get_orm_comment(comment_id)
        return TypeAdapter(ReadComment).validate_python(comment_entry)

    async def get_all(self) -> list[ReadComment]:
        stmt = select(Comment)
        comments = (await self.session.scalars(stmt)).all()
        return TypeAdapter(list[ReadComment]).validate_python(comments)

    async def create(
        self, comment: CreateComment, creator_id: uuid.UUID
    ) -> ReadComment:
        processing_time = datetime.utcnow()
        new_comment = Comment(
            id=uuid.uuid4(),
            **comment.model_dump(),
            created_by=creator_id,
            created_at=processing_time,
            updated_at=processing_time,
            updated_by=creator_id,
        )
        self.session.add(new_comment)
        return TypeAdapter(ReadComment).validate_python(new_comment)

    async def delete(self, comment_id: uuid.UUID) -> None:
        comment_entry = await self._get_orm_comment(comment_id)
        await self.session.delete(comment_entry)
        return None

    async def update(
        self, comment_id: uuid.UUID, comment: UpdateComment, updater_id: uuid.UUID
    ) -> ReadComment:
        comment_entry = await self._get_orm_comment(comment_id)
        for key, value in comment.model_dump(exclude_defaults=True).items():
            if getattr(comment_entry, key) != value:
                setattr(comment_entry, key, value)
        comment_entry.updated_by = updater_id
        comment_entry.updated_at = datetime.utcnow()
        return TypeAdapter(ReadComment).validate_python(comment_entry)


@router.get(
    "/",
    response_description="List all comments",
    dependencies=[Depends(current_active_user)],
)
async def list_comment(
    comment_store: Annotated[CommentStore, Depends()],
) -> list[ReadComment]:
    comments = await comment_store.get_all()
    return comments


@router.post(
    "/",
    response_description="Create a new comment",
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    comment: CreateComment,
    comment_store: Annotated[CommentStore, Depends()],
    user: Annotated[User, Depends(current_active_user)],
) -> ReadComment:
    new_comment = await comment_store.create(comment, user.id)
    return new_comment


@router.get(
    "/{comment_id}",
    response_description="Get a single comment",
    dependencies=[Depends(current_active_user)],
)
async def read_comment(
    comment_id: uuid.UUID,
    comment_store: Annotated[CommentStore, Depends()],
) -> ReadComment:
    comment_entry = await comment_store.get(comment_id)
    return comment_entry


@router.delete(
    "/{comment_id}",
    response_description="Delete a single comment",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment_id: uuid.UUID,
    comment_store: Annotated[CommentStore, Depends()],
) -> None:
    await comment_store.delete(comment_id)
    return None


@router.patch(
    "/{comment_id}",
    response_description="Update a single comment",
)
async def update_comment(
    comment_id: uuid.UUID,
    comment: UpdateComment,
    comment_store: Annotated[CommentStore, Depends()],
    user: Annotated[User, Depends(current_active_user)],
) -> ReadComment:
    comment_entry = await comment_store.update(comment_id, comment, user.id)
    return comment_entry
