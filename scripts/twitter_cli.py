import random

import typer

from owntwitter.models.factories import CommentFactory, PostFactory, UserFactory
from owntwitter.services.db import DatabaseConnector


def fill_db(
    number_of_users: int = 100, posts_per_user: int = 10, comments_per_post: int = 50
):
    db = DatabaseConnector()

    users = UserFactory.batch(number_of_users)
    [db.create_new_user(u) for u in users]
    typer.echo(f"added all {number_of_users} users")

    for idx, u in enumerate(users):

        typer.echo(f"adding posts and comments for user {idx + 1} of {len(users)}")

        users_posts = PostFactory.batch(posts_per_user)

        for p in users_posts:
            p.username = u.username
            db.create_new_post(p)

            comments_of_post = CommentFactory.batch(comments_per_post)
            for c in comments_of_post:
                c.username = random.choice(users).username
                c.post_id = p.post_id
                db.create_new_comment(c)

    typer.echo("job completed")


if __name__ == "__main__":
    typer.run(fill_db)
