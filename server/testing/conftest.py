#!/usr/bin/env python3

import pytest
from ..app import app, db
from ..models import Article, User
from faker import Faker
from random import randint

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    with app.app_context():
        db.create_all()
        fake = Faker()
        print("Creating users...")
        users = [User(name=fake.name()) for i in range(25)]
        db.session.add_all(users)
        print("Creating articles...")
        articles = []
        for i in range(100):
            content = fake.paragraph(nb_sentences=8)
            preview = content[:25] + '...'
            article = Article(
                author=fake.name(),
                title=fake.sentence(),
                content=content,
                preview=preview,
                minutes_to_read=randint(1,20),
            )
            articles.append(article)
        db.session.add_all(articles)
        db.session.commit()
        print("Database setup complete.")
