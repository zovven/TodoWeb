# -*- coding:utf8 -*-
__author__ = 'Zovven'
from flask.ext.script import Manager
from app import create_app
from app.models import db
from app.models import User, Todo, Post, Tag, post_tags, Album, PlanRecord, Plan, Image
import json
from app.jsonutil import TimeEncoder, DecimalEncoder
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import timeutils
from sqlalchemy import func, and_
from datetime import date, datetime, timedelta
import random

manager = Manager(create_app())


@manager.command
def add_plan():
    for x in range(20):
        plan = Plan()
        plan.plan_name = 'test plan' + str(x)
        plan.plan_day = random.randint(3, 999)
        plan.plan_total = random.randint(10, 9999)
        db.session.add(plan)
    db.session.commit()


@manager.command
def add_plan_record():
    plans = Plan.query.filter(Plan.id > 6).all()
    for plan in plans:
        for x in range(random.randint(1, 6)):
            plan_record = PlanRecord()
            plan_record.plan = plan
            plan_record.record_point = x * random.randint(1, 11)
            db.session.add(plan_record)
    db.session.commit()


@manager.command
def change_plan():
    plans = Plan.query.all()
    for plan in plans:
        plan.plan_type = random.randint(0, 3)
    db.session.commit()


@manager.command
def query_plan_num():
    _plan = Plan.query.filter(Plan.id == 1).first()
    # a = db.session.query(func.sum(PlanRecord.record_point)).filter(PlanRecord.plan_id == 2).scalar()
    print _plan.plan_total


@manager.command
def add_todo():
    for x in range(100):
        todo = Todo()
        todo.todo_desc = 'test plan--' + str(x) + str(x) + str(x)
        todo.todo_status = random.randint(0, 1)
        todo.todo_type = random.randint(1, 3)
        todo.todo_date = date(2015, random.randint(1, 12), random.randint(1, 27))
        db.session.add(todo)
    db.session.commit()


@manager.command
def query_todo():
    todos = Todo.query.search_date(date.today(), date.today())
    print list(todos.jsonify())


@manager.command
def complex_query():
    # rs = db.session.query(Todo.todo_type, func.sum(Todo.todo_time)).filter(
    #     and_(Todo.todo_date >= "2015-12-04", Todo.todo_date <= "2015-12-04",
    #          Todo.todo_status == Todo.STATUS_DONE)).all()
    # print rs
    #
    # type_dict = {
    #     "0": "计划",
    #     "1": "紧急",
    #     "2": "优先",
    #     "3": "普通",
    # }
    # print rs
    # json_list = list()
    # for row in rs:
    #     if row[0] is None:
    #         continue
    #     json_dict = dict()
    #     json_dict['value'] = long(row[1] or 0)
    #     json_dict['name'] = type_dict[str(row[0])]
    #     json_list.append(json_dict)
    # print json_list
    _todos = Todo.query.search_date(timeutils.today(), timeutils.today()).filter(
        Todo.todo_status == Todo.STATUS_NOT_DONE).sort_by_type().all()
    print len(_todos)


@manager.command
def advanced_query():
    # month_todo_time = db.session.query(func.sum(Todo.todo_time)).filter(
    #     and_(Todo.todo_date >= timeutils.get_firstday_month(), Todo.todo_date <= timeutils.get_lastday_month(),
    #          Todo.todo_status == Todo.STATUS_DONE)).scalar()

    # month_plan = db.session.query(func.count(Plan.id)).filter(
    #     and_(Plan.plan_end_date >= timeutils.get_firstday_month(), Plan.plan_end_date <= timeutils.get_lastday_month(),
    #          Plan.plan_status == Plan.STATUS_FINISH)).scalar()

    post_count = db.session.query(func.count(Image.id)).scalar()
    print post_count


if __name__ == '__main__':
    manager.run()
