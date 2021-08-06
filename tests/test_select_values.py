
import data_algebra

from data_algebra.data_ops import *  # https://github.com/WinVector/data_algebra
import data_algebra.util
import data_algebra.test_util

import data_algebra.SQLite


def select_values_direct():
   db_handle = data_algebra.SQLite.example_handle()
   sql = """
   SELECT 
     "column1" AS "c1",
     "column2" AS "c2"
   FROM 
     (VALUES 
       ('A', 'B'), 
       ('C', 'D'), 
       ('E', 'F'))
   """
   res = db_handle.read_query(sql)

   expect = data_algebra.default_data_model.pd.DataFrame({
    'c1': ['A', 'C', 'E'],
    'c2': ['B', 'D', 'F'],
    })

   assert data_algebra.test_util.equivalent_frames(res, expect)


def select_values_db_sqlite():
   db_handle = data_algebra.SQLite.example_handle()

   d = data_algebra.default_data_model.pd.DataFrame({
    'c1': ['A', 'C', 'E'],
    'c2': ['B', 'D', 'F'],
    })

   sql = db_handle.table_values_to_sql(d)
   res = db_handle.read_query(sql)

   assert data_algebra.test_util.equivalent_frames(res, d)