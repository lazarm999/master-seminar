from pyteal import *
import base64

def approval_program():
    # App initialization
    on_initialize = Seq([
        App.globalPut(Bytes("token_state"), Int(1)),  # Set initial token state to 1
        App.globalPut(Bytes("participant_0"), Addr("6W27A7O2EXY3YKMLWRHE33FCAAYBKZYTBBQ4DKRFXLEZ6ZJ6NDKXXQOAFQ")),
        App.globalPut(Bytes("participant_1"), Addr("NBMQE56M7YBL47JUMMEONGGQWWHYW2PXN3EOTR77FCZ422B2SVSSBVGJYU")),
        App.globalPut(Bytes("participant_2"), Addr("SOXTOUVCY6ONLK4BXHRTDOKIT3RB76ACQXGK24METQ6IBGGEXO4ICSGVVA")),
        App.globalPut(Bytes("participant_3"), Addr("UEBIKDB5A2EHZTSNLCP6VQMDNQDT24S3ZLVJWGTL77APAUZSTTDX3TMGUQ")),
        App.globalPut(Bytes("participant_4"), Addr("AYYE5MQUSBXWXKVFFIDHBSS3WWF3DIUYLCILDO5X4JJLNIHQIH6WZ2WPZ4")),
        App.globalPut(Bytes("to_manufacturer_amount"), Int(0)),
        App.globalPut(Bytes("to_distributor_amount"), Int(0)),
        App.globalPut(Bytes("resolve_timestamp"), Int(0)),
        Approve()
    ])
    
    # Helper to decode participants from global storage
    def get_participant(index):
        return App.globalGet(Bytes("participant_" + str(index)))

    # Logic for enact function
    def get_action_code():
        return If(
            Txn.application_args.length() > Int(0),
            Btoi(Txn.application_args[0]),
            Int(0)          
        )
    
    def is_order_in_progress():
        return Or(
            App.globalGet(Bytes("to_manufacturer_amount")) != Int(0),
            App.globalGet(Bytes("to_distributor_amount")) != Int(0)
        )
    
    def get_cond():
        return If(
            Txn.application_args.length() > Int(1),
            Btoi(Txn.application_args[1]),
            Int(0)          
        )
    
    def get_to_distributor_amount():
        return If(
            Txn.application_args.length() > Int(1),
            Btoi(Txn.application_args[1]),
            Int(0)          
        )
    
    def get_to_manufacturer_amount():
        return If(
            Txn.application_args.length() > Int(2),
            Btoi(Txn.application_args[2]),
            Int(0)          
        )
        
    _token_state = ScratchVar(TealType.uint64)
    
    def payment_transaction(amount, sender, receiver):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.sender: sender,
                TxnField.receiver: receiver,
                TxnField.amount: amount,
            }),
            InnerTxnBuilder.Submit(),
        )
    
    def token_state_log():
        return Itob(App.globalGet(Bytes("token_state")))
    
    def to_distributor_amount_log():
        return Itob(App.globalGet(Bytes("to_distributor_amount")))
    
    def to_manufacturer_amount_log():
        return Itob(App.globalGet(Bytes("to_manufacturer_amount")))
    
    def log_int(log):
        return Seq([
            Log(Bytes("log_int")),
            Log(log),
        ])
        
    def get_confirmation():
        return If(
            Txn.application_args.length() > Int(1),
            Btoi(Txn.application_args[1]),
            Int(0)          
        )
    
    manual_transitions = Cond(
        [And(
            _token_state.load() & Int(1) == Int(1),
            Txn.sender() == get_participant(0)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(1)),
            _token_state.store(_token_state.load() | Int(2))
        ])],
        [And(
            get_cond() == Int(1),
            _token_state.load() & Int(2) == Int(2),
            Txn.sender() == get_participant(1)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(2)),
            _token_state.store(_token_state.load() | Int(4))
        ])],
        [And(
            get_cond() == Int(2),
            _token_state.load() & Int(2) == Int(2),
            Txn.sender() == get_participant(1),
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(2)),
            _token_state.store(_token_state.load() | Int(8)),
            App.globalPut(Bytes("start_balance"), Balance(Global.current_application_address())),
            log_int(Itob(App.globalGet(Bytes("start_balance"))))
        ])],
        [And(
            _token_state.load() & Int(4) == Int(4),
            Txn.sender() == get_participant(2)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(4)),
            _token_state.store(_token_state.load() | Int(0))
        ])],
        [And(
            _token_state.load() & Int(8) == Int(8),
            App.globalGet(Bytes("start_balance")) + get_to_distributor_amount() * Int(2) + get_to_manufacturer_amount() == Balance(Global.current_application_address()),
            Txn.sender() == get_participant(2)
        ), Seq([
            App.globalPut(Bytes("to_distributor_amount"), get_to_distributor_amount()),
            App.globalPut(Bytes("to_manufacturer_amount"), get_to_manufacturer_amount()),
            log_int(to_distributor_amount_log()),
            log_int(to_manufacturer_amount_log()),
            _token_state.store(_token_state.load() & ~Int(8)),
            _token_state.store(_token_state.load() | Int(16))
        ])],
        [And(
            _token_state.load() & Int(16) == Int(16),
            Txn.sender() == get_participant(3)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(16)),
            _token_state.store(_token_state.load() | Int(96))
        ])],
        [And(
            _token_state.load() & Int(32) == Int(32),
            Txn.sender() == get_participant(3)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(32)),
            _token_state.store(_token_state.load() | Int(128))
        ])],
        [And(
            _token_state.load() & Int(64) == Int(64),
            Txn.sender() == get_participant(3)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(64)),
            _token_state.store(_token_state.load() | Int(256))
        ])],
        [And(
            _token_state.load() & Int(512) == Int(512),
            Txn.sender() == get_participant(4)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(512)),
            _token_state.store(_token_state.load() | Int(1024)),
        ])],
        [And(
            _token_state.load() & Int(1024) == Int(1024),
            get_confirmation() == Int(1),
            Txn.sender() == get_participant(2)
        ), Seq([
            payment_transaction(App.globalGet(Bytes("to_distributor_amount")) * Int(2), Global.current_application_address(), get_participant(4)),
            App.globalPut(Bytes("to_distributor_amount"), Int(0)),
            _token_state.store(_token_state.load() & ~Int(1024)),
            _token_state.store(_token_state.load() | Int(2048)),
        ])],
        [And(
            _token_state.load() & Int(2048) == Int(2048),
            get_confirmation() == Int(1),
            Txn.sender() == get_participant(2)
        ), Seq([
            payment_transaction(App.globalGet(Bytes("to_manufacturer_amount")), Global.current_application_address(), get_participant(3)),
            App.globalPut(Bytes("to_manufacturer_amount"), Int(0)),
            _token_state.store(_token_state.load() & ~Int(2048)),
            _token_state.store(_token_state.load() | Int(4096)),
        ])],
        [And(
            _token_state.load() & Int(4096) == Int(4096),
            Txn.sender() == get_participant(2),
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(4096)),
            _token_state.store(_token_state.load() | Int(0)),
        ])],
        [Int(1), Seq([Log(Bytes("Default manual transition"))])]
    )
    
    combine_parallel_states = If(
        _token_state.load() & Int(384) == Int(384),
        Seq([
            _token_state.store(_token_state.load() & ~Int(384)),
            _token_state.store(_token_state.load() | Int(512))
        ]),
        Seq([])
    )
    
    reset_state = Seq([
        Log(Bytes("Reset contract")),
        App.globalPut(Bytes("token_state"), Int(1)),
        App.globalPut(Bytes("to_distributor_amount"), Int(0)),
        App.globalPut(Bytes("to_manufacturer_amount"), Int(0)),
        App.globalPut(Bytes("resolve_timestamp"), Int(0)),
        log_int(token_state_log()),
        log_int(to_distributor_amount_log()),
        log_int(to_manufacturer_amount_log()),
        Approve()
    ])
    
    # action code 200 = resolve_conflict
    resolve_conflict = If(
        And(
            get_action_code() == Int(200),
            App.globalGet(Bytes("resolve_timestamp")) != Int(0),
            Or(Txn.sender() == get_participant(2),
               Txn.sender() == get_participant(3),
               Txn.sender() == get_participant(4)),
            Global.latest_timestamp() > App.globalGet(Bytes("resolve_timestamp")) 
        ),
        Seq([
            payment_transaction(App.globalGet(Bytes("to_distributor_amount")) / Int(3) + App.globalGet(Bytes("to_manufacturer_amount")) / Int(2), Global.current_application_address(), get_participant(2)),
            payment_transaction(App.globalGet(Bytes("to_distributor_amount")) / Int(3)  + App.globalGet(Bytes("to_manufacturer_amount")) / Int(2), Global.current_application_address(), get_participant(3)),
            payment_transaction(App.globalGet(Bytes("to_distributor_amount")) / Int(3), Global.current_application_address(), get_participant(4)),
            reset_state
        ]),
        Seq([Log(Bytes("Uslovi nisu ispunjeni"))])
    )

    # action code 100 = set_resolve_timestamp action
    set_resolve_timestamp = If(
        And(
            get_action_code() == Int(100),
            is_order_in_progress(),
            Or(Txn.sender() == get_participant(2),
               Txn.sender() == get_participant(3),
               Txn.sender() == get_participant(4)),
            App.globalGet(Bytes("resolve_timestamp")) == Int(0)
        ),
        Seq([
            # 2592000 seconds = 30 days
            App.globalPut(Bytes("resolve_timestamp"), Global.latest_timestamp() + Int(2592000)),
            Log(Bytes("resolve_timestamp set"))
        ]),
        Seq([])
    )
    
    # action code 101 = set_amounts action
    set_amounts = If(
        And(
            get_action_code() == Int(101),
        ),
        Seq([
            App.globalPut(Bytes("to_manufacturer_amount"), Int(10)),
            App.globalPut(Bytes("to_distributor_amount"), Int(10)),
            log_int(to_distributor_amount_log()),
            log_int(to_manufacturer_amount_log()),
            Log(Bytes("amounts set"))
        ]),
        Seq([])
    )
    
    # Update the token state in global storage
    update_token_state = App.globalPut(Bytes("token_state"), _token_state.load())
    
    program = Cond(
        [Txn.application_id() == Int(0), on_initialize],
        [Txn.on_completion() == OnComplete.NoOp, Cond(
            [Btoi(Txn.application_args[0]) == Int(999), reset_state],
            [Int(1), Seq([ 
                # Log(Bytes("Arguments length: ")),
                # log_int(Itob(Txn.application_args.length())),
                 _token_state.store(App.globalGet(Bytes("token_state"))),  # Load current token state
                manual_transitions,
                Log(Bytes("manual_transitions done")),
                combine_parallel_states,
                resolve_conflict,
                set_resolve_timestamp,
                set_amounts,
                update_token_state,
                log_int(token_state_log()),
                Log(Bytes(" ")),
                Approve()
            ])]
    )])

    return program

def clear_program():
    return Approve()