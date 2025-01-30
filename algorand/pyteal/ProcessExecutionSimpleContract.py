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
        Approve()
    ])
    
    # Helper to decode participants from global storage
    def get_participant(index):
        return App.globalGet(Bytes("participant_" + str(index)))

    # Logic for enact function
    def get_id():
        return Btoi(Txn.application_args[0])
    
    def get_cond():
        return Btoi(Txn.application_args[1])
    
    _token_state = ScratchVar(TealType.uint64)  # Temporary variable for token state
    
    manual_transitions = Cond(
        [And(
            get_id() == Int(0),
            _token_state.load() & Int(1) == Int(1),
            Txn.sender() == get_participant(0)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(1)),
            _token_state.store(_token_state.load() | Int(2))
        ])],
        [And(
            get_id() == Int(1),
            _token_state.load() & Int(2) == Int(2),
            Txn.sender() == get_participant(1)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(2)),
            _token_state.store(_token_state.load() | Int(4))
        ])],
        [And(
            get_id() == Int(2),
            _token_state.load() & Int(4) == Int(4),
            Txn.sender() == get_participant(2)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(4)),
            _token_state.store(_token_state.load() | Int(8))
        ])],
        [And(
            get_id() == Int(3),
            _token_state.load() & Int(8) == Int(8),
            Txn.sender() == get_participant(3)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(8)),
            _token_state.store(_token_state.load() | Int(16))
        ])],
        [And(
            get_id() == Int(4),
            _token_state.load() & Int(16) == Int(16),
            Txn.sender() == get_participant(4)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(16)),
            _token_state.store(_token_state.load() | Int(32))
        ])],
        [And(
            get_id() == Int(5),
            _token_state.load() & Int(32) == Int(32),
            Txn.sender() == get_participant(2)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(32)),
            _token_state.store(_token_state.load() | Int(64))
        ])],
        [And(
            get_id() == Int(6),
            _token_state.load() & Int(64) == Int(64),
            Txn.sender() == get_participant(2)
        ), Seq([
            _token_state.store(_token_state.load() & ~Int(64)),
            _token_state.store(_token_state.load() | Int(0))
        ])],
        [Int(1), Seq([Log(Bytes("Default manual transition"))])]
    )
    
    update_token_state = App.globalPut(Bytes("token_state"), _token_state.load())
    
    def token_state_log():
        return Itob(App.globalGet(Bytes("token_state")))
    
    def log_int(log):
        return Seq([
            Log(Bytes("log_int")),
            Log(log),
        ])
    
    reset_state = Seq([
        Log(Bytes("Reset contract")),
        App.globalPut(Bytes("token_state"), Int(1)),
        log_int(token_state_log()),
        Approve()
    ])
    
    program = Cond(
        [Txn.application_id() == Int(0), on_initialize],
        [Txn.on_completion() == OnComplete.NoOp, Cond(
            [Btoi(Txn.application_args[0]) == Int(999), reset_state],
            [Int(1), Seq([
                _token_state.store(App.globalGet(Bytes("token_state"))),  # Load current token state
                manual_transitions,
                # Log(Bytes("manual_transitions done")),
                update_token_state,
                # log_int(token_state_log()),
                # Log(Bytes(" ")),
                Approve()
            ])]
    )])

    return program

def clear_program():
    return Approve()