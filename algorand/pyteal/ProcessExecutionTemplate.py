from pyteal import *
import base64

def approval_program():
    # App initialization
    on_initialize = Seq([
        App.globalPut(Bytes("token_state"), Int(1)),  # Set initial token state to 1
        {{#participants}}
        App.globalPut(Bytes("participant_{{{id}}}"), Addr("__address{{{id}}}__")),
        {{/participants}}
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
    
    def token_state_log():
        return Itob(App.globalGet(Bytes("token_state")))
    
    def log_int(log):
        return Seq([
            Log(Bytes("log_int")),
            Log(log),
        ])
    
    _token_state = ScratchVar(TealType.uint64)  # Temporary variable for token state
    
    {{#hasManualTransitions}}
    manual_transitions = Cond(
        {{#manualTransitions}}
        [And(
            {{#condition}}
            (cond & {{{condition}}} == {{{condition}}}),
            {{/condition}}
            get_id() == Int({{{id}}}),
            _token_state.load() & Int({{{consume}}}) == Int({{{consume}}}),
            {{#initiator}}
            Txn.sender() == get_participant({{{initiator}}})
            {{/initiator}}
        ), Seq([
            Log(Bytes("{{{index}}}. cond")),
            _token_state.store(_token_state.load() & ~Int({{{consume}}})),
            _token_state.store(_token_state.load() | Int({{{produce}}}))
        ])],
        {{/manualTransitions}}
        [Int(1), Seq([Log(Bytes("Default manual transition"))])]
    )
    {{/hasManualTransitions}}
    
    {{#hasAutonomousTransitions}}
    autonomous_transitions = While(_token_state.load() != Int(0)).Do(Seq([
        {{#autonomousTransitions}}
        If(And(
            {{#condition}}
            get_cond() & Int({{{condition}}}) == Int({{{condition}}}),
            {{/condition}}
            _token_state.load() & Int({{{consume}}}) == Int({{{consume}}})),
        Seq([
            Log(Bytes("{{{index}}}. cond")),
            _token_state.store(_token_state.load() & ~Int({{{consume}}})),
            _token_state.store(_token_state.load() | Int({{{produce}}})),
            {{#isEnd}}
            Break(),
            {{/isEnd}}
            {{^isEnd}}
            Continue()
            {{/isEnd}}
        ])),
        {{/autonomousTransitions}}
        Break()
    ]))
    {{/hasAutonomousTransitions}}
    
    reset_state = Seq([
        Log(Bytes("Reset contract")),
        App.globalPut(Bytes("token_state"), Int(1))
    ])

    # Update the token state in global storage
    update_token_state = App.globalPut(Bytes("token_state"), _token_state.load())
        
    program = Cond(
        [Txn.application_id() == Int(0), on_initialize],
        [Txn.on_completion() == OnComplete.NoOp, Cond(
            [Btoi(Txn.application_args[0]) == Int(999), Seq([reset_state, log_int(token_state_log())])],
            [Int(1), Seq([
                _token_state.store(App.globalGet(Bytes("token_state"))),  # Load current token state
                {{#hasManualTransitions}}
                manual_transitions,
                Log(Bytes("manual_transitions done")),
                {{/hasManualTransitions}}
                {{#hasAutonomousTransitions}}
                autonomous_transitions,
                Log(Bytes("autonomus_transitions done")),
                {{/hasAutonomousTransitions}}
                update_token_state,
                log_int(token_state_log()),
                Log(Bytes(" ")),
                Approve()
            ])]
    )])

    return program

def clear_program():
    return Approve()