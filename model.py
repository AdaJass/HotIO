import sqlalchemy as sa
import asyncio

metadata = sa.MetaData()

obj = sa.Table('objects', metadata,
               sa.Column('id', sa.Integer, primary_key=True),
               sa.Column('main', sa.String(255),  nullable=False),
               sa.Column('weight',sa.Integer, nullable=True),
               sa.Column('andDescript',sa.String(255), nullable=True),
               sa.Column('orDescript',sa.String(255), nullable=True),
               )

cur = sa.Table('current', metadata,
            sa.Column('objectid',sa.Integer, sa.ForeignKey('object.id')),
            sa.Column('dtime', sa.DateTime),
            sa.Column('baidu_pages',sa.Integer),
            sa.Column('sogou_pages',sa.Integer),
            sa.Column('_360_pages',sa.Integer),
            # sa.Column('zhihu_comments',sa.Integer),
            # sa.Column('votes_36kr',sa.Integer),
            # sa.Column('weibo_hot',sa.Integer),
            # sa.Column('tieba_hot',sa.Integer),
            sa.PrimaryKeyConstraint('objectid' , 'dtime' ,name=' mytable_pk')           
    )

his = sa.Table('history', metadata,
            sa.Column('objectid',sa.Integer, sa.ForeignKey('object.id' )),
            sa.Column('dtime', sa.DateTime),
            sa.Column('baidu_pages',sa.Integer),
            sa.Column('sogou_pages',sa.Integer),
            sa.Column('_360_pages',sa.Integer),
            # sa.Column('zhihu_comments',sa.Integer),
            # sa.Column('votes_36kr',sa.Integer),
            # sa.Column('weibo_hot',sa.Integer),
            # sa.Column('tieba_hot',sa.Integer),
            sa.PrimaryKeyConstraint('objectid' , 'dtime' ,name=' mytable_pk')          
    )

com = sa.Table('comments',metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('domain', sa.String(21)),
            sa.Column('title', sa.String(45)),
            sa.Column('url', sa.String(45)),
            sa.Column('mongo_str', sa.String(255))
    )                      