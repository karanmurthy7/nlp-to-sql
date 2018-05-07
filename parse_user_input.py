import json
import torch
from sqlnet.utils import *
from sqlnet.model.seq2sql import Seq2SQL
from sqlnet.model.sqlnet import SQLNet
import numpy as np
import datetime
import os

import argparse

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class UserInputUtility(object):
    USE_SMALL = True
    GPU = True
    BATCH_SIZE = 15
    TEST_ENTRY = (True, True, True)  # (AGG, SEL, COND)
    N_word = 300
    B_word = 42
    model = None
    word_emb = None
    test_table_data = None
    USE_CA = False
    args =  Namespace(dataset= 0, baseline = False, 
                      use_ca = False, train_emb = False, 
                      rl=False, toy= True, ca=False)
    
    
    def __init__(self):      
        
        print(os.getcwd())
            
        UserInputUtility.word_emb = load_word_emb('glove/glove.%dB.%dd.txt' % (UserInputUtility.B_word, UserInputUtility.N_word), \
                                 load_used=True, use_small=UserInputUtility.USE_SMALL)  # load_used can speed up loading
        
        sql_data, table_data, val_sql_data, val_table_data, \
            test_sql_data, self.test_table_data, \
            TRAIN_DB, DEV_DB, self.TEST_DB = load_dataset(
                    0, use_small=UserInputUtility.USE_SMALL)
        
        UserInputUtility.model = SQLNet(UserInputUtility.word_emb, N_word=UserInputUtility.N_word, \
                                        use_ca=UserInputUtility.args.use_ca, gpu=UserInputUtility.GPU, trainable_emb=True)
        
        agg_m, sel_m, cond_m = best_model_name(UserInputUtility.args)
        print("Loading from %s" % agg_m)
        UserInputUtility.model.agg_pred.load_state_dict(torch.load(agg_m))
        print("Loading from %s" % sel_m)
        UserInputUtility.model.sel_pred.load_state_dict(torch.load(sel_m))
        print("Loading from %s" % cond_m)
        UserInputUtility.model.cond_pred.load_state_dict(torch.load(cond_m))
        print("Done loading...")
        
    def fetch_response_from_model(self, input):
        if input is None:
            return 'Invalid input'
        
        test_sql_data = self.format_input(input)
        # print('------->>> table data', self.test_table_data)
        return epoch_exec_acc_from_user(
            UserInputUtility.model, UserInputUtility.BATCH_SIZE, \
                test_sql_data, self.test_table_data, self.TEST_DB)
     
        
    def format_input(self, input):
        test_format = [{
                "question": "how many schools or teams had jalen rose",
                "query_tok": [""],
                "query_tok_space": [" ", "", "", " ", "", " ", " ", " ", " ", " ", ""],
                "table_id": "1-10015132-16",
                "question_tok_space": [" ", " ", " ", " ", " ", " ", " ", ""],
                "sql": {
                    "agg": 0,
                    "sel": 0,
                    "conds": [
                        [0, 0, "Jalen Rose"]
                    ]
                },
                "phase": 1,
                "query": "",
                "question_tok": ["how", "many", "schools", "or", "teams", "had", "jalen", "rose"]
            },
            {
                "question": "how many schools or teams had jalen rose",
                "query_tok": [""],
                "query_tok_space": [" ", "", "", " ", "", " ", " ", " ", " ", " ", ""],
                "table_id": "1-10015132-16",
                "question_tok_space": [" ", " ", " ", " ", " ", " ", " ", ""],
                "sql": {
                    "agg": 3,
                    "sel": 5,
                    "conds": [
                        [0, 0, "Jalen Rose"]
                    ]
                },
                "phase": 1,
                "query": "",
                "question_tok": ["how", "many", "schools", "or", "teams", "had", "jalen", "rose"]
            }]          
#         user_input = 'What is the capital of Portugal?'
#         input_list = user_input.split()
#         test_format[0]["question_tok"] = input_list
#         test_format[1]["question_tok"] = input_list
        return test_format


def user_input():
        return
        test_format = [{
                "question": 'What is the capital of Portugal',
                "query_tok": [""],
                "query_tok_space": None,
                "table_id": "1-10015132-16",
                "question_tok_space": [" ", " ", " ", " ", " ", ""],
                "sql": {
                    "agg": 0,
                    "sel": 2,
                    "conds": []
                },
                "phase": 1,
                "query": '',
                "question_tok": None
            },
            {
                "question": 'What is the capital of Portugal',
                "query_tok": [""],
                "query_tok_space": None,
                "table_id": "1-10015132-16",
                "question_tok_space": [" ", " ", " ", " ", " ", ""],
                "sql": {
                    "agg": 0,
                    "sel": 2,
                    "conds": []
                },
                "phase": 1,
                "query": '',
                "question_tok": None
            }]          
        user_input = 'What is the capital of Portugal?'
        input_list = user_input.split()
        test_format[0]["question_tok"] = input_list
        test_format[1]["question_tok"] = input_list
        test_table_data = 'data/test_tok.tables.jsonl'
        return test_format


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--toy', action='store_true',
            help='If set, use small data; used for fast debugging.')
    parser.add_argument('--ca', action='store_true',
            help='Use conditional attention.')
    parser.add_argument('--dataset', type=int, default=0,
            help='0: original dataset, 1: re-split dataset')
    parser.add_argument('--rl', action='store_true',
            help='Use RL for Seq2SQL.')
    parser.add_argument('--baseline', action='store_true',
            help='If set, then test Seq2SQL model; default is SQLNet model.')
    parser.add_argument('--train_emb', action='store_true',
            help='Use trained word embedding for SQLNet.')
    args = parser.parse_args()
    print('--------------->>>>>>>>>>', args)
    N_word = 300
    B_word = 42
    if args.toy:
        USE_SMALL = True
        GPU = False
        BATCH_SIZE = 15
    else:
        USE_SMALL = False
        GPU = False
        BATCH_SIZE = 64
    TEST_ENTRY = (True, True, True)  # (AGG, SEL, COND)
    
    
    
    sql_data, table_data, val_sql_data, val_table_data, \
            test_sql_data, test_table_data, \
            TRAIN_DB, DEV_DB, TEST_DB = load_dataset(
                    args.dataset, use_small=USE_SMALL)

    word_emb = load_word_emb('glove/glove.%dB.%dd.txt' % (B_word, N_word), \
        load_used=True, use_small=USE_SMALL)  # load_used can speed up loading

    if args.baseline:
        model = Seq2SQL(word_emb, N_word=N_word, gpu=GPU, trainable_emb=True)
    else:
        model = SQLNet(word_emb, N_word=N_word, use_ca=args.ca, gpu=GPU,
                trainable_emb=True)

    if args.train_emb:
        agg_m, sel_m, cond_m, agg_e, sel_e, cond_e = best_model_name(args)
        print("Loading from %s" % agg_m)
        model.agg_pred.load_state_dict(torch.load(agg_m))
        print("Loading from %s" % sel_m)
        model.sel_pred.load_state_dict(torch.load(sel_m))
        print("Loading from %s" % cond_m)
        model.cond_pred.load_state_dict(torch.load(cond_m))
        print("Loading from %s" % agg_e)
        model.agg_embed_layer.load_state_dict(torch.load(agg_e))
        print("Loading from %s" % sel_e)
        model.sel_embed_layer.load_state_dict(torch.load(sel_e))
        print("Loading from %s" % cond_e)
        model.cond_embed_layer.load_state_dict(torch.load(cond_e))
    else:
        agg_m, sel_m, cond_m = best_model_name(args)
        print("Loading from %s" % agg_m)
        model.agg_pred.load_state_dict(torch.load(agg_m))
        print("Loading from %s" % sel_m)
        model.sel_pred.load_state_dict(torch.load(sel_m))
        print("Loading from %s" % cond_m)
        model.cond_pred.load_state_dict(torch.load(cond_m))

    test_sql_data = user_input()
    print("Test execution acc: %s" % epoch_exec_acc_from_user(
            model, BATCH_SIZE, test_sql_data, test_table_data))
    
