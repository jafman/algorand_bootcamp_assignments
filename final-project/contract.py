from pyteal import *

# CROWD FUNDING SMART CONTRACT

def approval_program():
    on_creation = Seq(
        [
            App.globalPut(Bytes("Creator"), Txn.sender()),
            Assert(Txn.application_args.length() == Int(1)),
            App.globalPut(Bytes("FundRaised"), Int(0)),
            App.globalPut(Bytes("FundingEnd"), Btoi(Txn.application_args[0])),
            Return(Int(1)),
        ]
    )

    is_creator = Txn.sender() == App.globalGet(Bytes("Creator"))

    on_closeout = Seq(
        [
            Return(Int(1)),
        ]
    )

    fund_raised = App.globalGet(Bytes("FundRaised"))
    amount_donated = Txn.application_args[1]
    on_donate = Seq(
        [
            Assert(is_creator), # Assert that the creator is calling,
            If(
                Global.round() <= App.globalGet(Bytes("FundingEnd")),
                App.globalPut(Bytes("FundRaised"), fund_raised + Btoi(amount_donated))
            ),
            Return(Int(1))
        ]
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.application_args[0] == Bytes("donate"), on_donate],
    )

    return program


def clear_state_program():
    program = Seq(
        [
            Return(Int(1)),
        ]
    )

    return program


if __name__ == "__main__":
    with open("vote_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), Mode.Application, version=6)
        f.write(compiled)

    with open("vote_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), Mode.Application, version=6)
        f.write(compiled)
