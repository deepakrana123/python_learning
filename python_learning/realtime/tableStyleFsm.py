# # state = "UNVERIFIED"


# # transition_table = {
# #     ("UNVERIFIED", "SEND_EMAIL"): ("PENDING_VERIFICATION", send_email),
# #     ("UNVERIFIED", "RESEND"): ("PENDING_VERIFICATION", send_email),
# #     ("PENDING_VERIFICATION", "CLICK_LINK"): ("VERIFIED", confirm_account),
# #     ("PENDING_VERIFICATION", "TIMEOUT"): ("EXPIRED", mark_expired),
# #     ("EXPIRED", "RESEND"): ("PENDING_VERIFICATION", send_email),
# #     ("VERIFIED", "*"): ("VERIFIED", None),
# # }

# # INITIATED
# # PROCESSING
# # SUCCESS
# # FAILED
# # CANCELLED

# # PAYMENT_REQUEST
# # PAYMENT_SUCCESS
# # PAYMENT_FAILURE
# # TIMEOUT
# # USER_CANCEL
# # RETRY


# # state = "INITATIED"

# # transition_table = {
# #     ("INITATIED", "PAYMENT_REQUEST"): ("PROCESSING", payment_initated),
# #     ("PROCESSING", "PAYMENT_SUCCESS"): ("SUCCESS", mark_success),
# #     ("SUCCESS", "PAYMENT_FAILURE"): ("FAILED", mark_failed),
# #     ("PROCESSING", "TIMEOUT"): ("FAILED", mark_failed),
# #     ("FAILED", "RETRY"): ("PROCESSING", payment_initated),
# #     ("PROCESSING", "USER_CANCEL"): ("CANCELLED", cancel_payment),
# #     ("SUCCESS", "*"): ("SUCCESS", None),
# #     ("CANCELLED", "*"): ("CANCELLED", None),
# # }

# # IDLE
# # UPLOADING
# # PAUSED
# # COMPLETED
# # FAILED

# # START_UPLOAD
# # CHUNK_UPLOADED
# # PAUSE
# # RESUME
# # ERROR
# # RETRY
# # CANCEL


# state = "IDLE"

# transition_table = {
#     ("IDLE", "START_UPLOAD"): ("UPLOADING", upload_initated),
#     ("UPLOADING", "LAST_CHUNK_UPLOADED"): ("COMPLETED", mark_success),
#     ("UPLOADING", "CHUNK_UPLOADED"): ("PAUSED", mark_paused),
#     ("UPLOADING", "PAUSE"): ("PAUSED", mark_paused),
#     ("UPLOADING", "ERROR"): ("PAUSED", mark_paused),
#     ("UPLOADING", "CANCEL"): ("FAILED", mark_failed),
#     ("PAUSED", "RESUME"): ("UPLOADING", upload_initated),
#     ("PAUSED", "RETRY"): ("UPLOADING", upload_initated),
#     ("COMPLETED", "*"): ("COMPLETED", None),
#     ("FAILED", "*"): ("FAILED", None),
# }


# def handle_event(event):
#     global state
#     key = (state, event)
#     if key not in transition_table:
#         print(f"Ignored invalid event {event} in state")
#         return
#     next_state, action = transition_table[key]
#     if action:
#         action()
#     state = next_state
#     print(f"transitioned to {state} via {event}")


# hfsm

# USER_SESSION_PARENT_RULES = {
#     "LOGOUT": ("LOGIN_IDEAL", "reset_session"),
#     "TIMEOUT": ("FAILED", "mark_timeout"),
# }

# LOGIN_CHILD_RULES = {
#     ("IDLE", "check_credentials"): ("VERIFICATION_WAIT", "start_verfication"),
#     ("VERIFICATION_WAIT", "success"): ("SUCCESS", "mark_success"),
#     ("VERIFICATION_WAIT", "failed"): ("RETRY", "increment_retry"),
#     ("RETRY", "retry_check"): ("IDLE", "reset_retry"),
#     ("VERIFICATION_WAIT", "failed_bad_credentials"): ("IDLE", "log_bad_credentials"),
# }


# def reset_session():
#     print("Session reset")


# def mark_timeout():
#     print("Timeout occured")


# def start_verification():
#     print("Verification start")


# def mark_success():
#     print("Login successful")


# def increment_retry():
#     print("Retry incremented")


# def reset_retry():
#     print("Retry reset")


# def log_bad_credentials():
#     print("Bad credentials logged")


# ACTIONS = {
#     "reset_session": reset_session,
#     "mark_timeout": mark_timeout,
#     "mark_success": mark_success,
#     "increment_retry": increment_retry,
#     "reset_retry": reset_retry,
#     "log_bad_credentials": log_bad_credentials,
# }


# class HFSM:
#     def __init__(self):
#         self.parent_state = "USER_SESSION"
#         self.child_state = "IDLE"

#     def handle_event(self, event):
#         if event in USER_SESSION_PARENT_RULES:
#             next_state, action_name = USER_SESSION_PARENT_RULES[event]
#             ACTIONS[action_name]()
#             self.child_state = next_state
#             print(f"[Parent] Transitioned to {self.child_state}")
#             return
#         key = (self.child_state, event)
#         if key in LOGIN_CHILD_RULES:
#             next_state, action_name = LOGIN_CHILD_RULES[key]
#             ACTIONS[action_name]()
#             self.child_state = next_state
#             print(f"[Child] Transitioned to {self.child_state}")
#             return

#         print(f"No transition for event '{event}' in state '{self.child_state}'")


FSM_TABLE = {
    ("IDLE", "check_credentials"): ("VERIFICATION_WAIT", "start_verification"),
    ("VERIFICATION_WAIT", "success"): ("VERIFICATION_WAIT", "marked_success"),
    ("VERIFICATION_WAIT", "failed"): ("RETRY", "increment_retry"),
    ("RETRY", "retry_check"): ("IDLE", "reset_retry"),
    ("VERIFICATION_WAIT", "failed_bad_credentials"): ("IDLE", "log_bad_credentials"),
    ("IDLE", "LOGOUT"): ("IDLE", "reset_session"),
    ("VERIFICATION_WAIT", "LOGOUT"): ("IDLE", "reset_session"),
    ("RETRY", "LOGOUT"): ("IDLE", "reset_session"),
    ("SUCCESS", "LOGOUT"): ("IDLE", "reset_session"),
    ("IDLE", "TIMEOUT"): ("FAILED", "mark_timeout"),
    ("VERIFICATION_WAIT", "TIMEOUT"): ("FAILED", "mark_timeout"),
    ("RETRY", "TIMEOUT"): ("FAILED", "mark_timeout"),
}


def start_verification():
    print("Verification started")


def mark_success():
    print("Login sccess")


def increment_retry():
    print("Retry increment")


def reset_retry():
    print("Retry reset")


def log_bad_credentials():
    print("Bad credential")


def reset_session():
    print("Session reset")


def mark_timeout():
    print("Timeout")


ACTIONS = globals()


class FSM:
    def __init__(self):
        self.state = "IDLE"

    def handle_event(self, event):
        key = (self.state, event)
        if key not in FSM_TABLE:
            print("Invalid transition")
            return
        next_state, action = FSM_TABLE[key]
        ACTIONS[action]()
        self.state = next_state
        print(f"State -> {self.state}")


# /state machine


class State:
    def handle(self, ctx, event):
        raise NotImplementedError


class Idle(State):
    def handle(self, ctx, event):
        if event == "check_credentials":
            print("Verfication started")
            ctx.state = VerificationWait()


class VerificationWait(State):
    def handle(self, ctx, event):
        if event == "success":
            print("Login success")
            ctx.state = Success()
        elif event == "failed":
            print("Retry incremented")
            ctx.state = Retry()
        elif event == "failed_bad_credentials":
            print("Bad credentials")
            ctx.state = Idle()


class Retry(State):
    def handle(self, ctx, event):
        if event == "retry_check":
            print("Retry reset")
            ctx.state = Idle()


class Success(State):
    def handle(self, ctx, event):
        if event == "LOGOUT":
            print("Session reset")
            ctx.state = Idle()


class LoginStateMachine:
    def __init__(self):
        self.state = Idle()

    def handle_event(self, event):
        self.state.handle(self, event)


# CREATED
# PAYMENT_PENDING
# PAID
# SHIPPED
# DELIVERED
# CANCELLED

FSM_TABLE_ORDER = {
    ("CREATED", "order_created"): ("PAYMENT_VERFICATION", "payment_verfication"),
    ("PAYMENT_VERFICATION", "payment_done"): ("PAYMENT_SUCCESS", "payment_success"),
    ("PAYMENT_VERFICATION", "Cancel"): ("PAYMENT_FAILURE", "payment_failure"),
    ("PAYMENT_VERFICATION", "retry"): ("PAYMENT_RETRY", "payment_increament_retry"),
    ("PAYMENT_RETRY", "retry"): ("PAYMENT_VERFICATION", "payment_retry"),
    ("PAYMENT_FAILURE", "order_cancelled"): ("CREATED", "order_created"),
    ("PAYMENT_SUCCESS", "order_ready_for_transist"): (
        "TRANSIST",
        "order_ready_for_shipped",
    ),
    ("TRANSIST", "Cancel"): ("CANCELLED", "order_cancelled"),
    ("TRANSIST", "order_shipped"): ("SHIPPED", "order_delivery"),
    ("SHIPPED", "Cancel"): ("CANCELLED", "order_cancelled"),
    ("SHIPPED", "delivered"): ("DELIVERED", "order_delivered"),
    ("CANCELLED", "*"): ("CANCELLED", "order_cancelled"),
    ("DELIVERED", "*"): ("DELIVERED", "order_delivered"),
}


def start_payment():
    print("payment started")


def order_shipped():
    print("order_shipped")


def increment_retry():
    print("Retry increment")


def reset_retry():
    print("Retry reset")


def reset_order():
    print("Order Reset")


def order_delivered():
    print("order_delivered")


ACTIONSORDER = globals()


class FSMORDER:
    def __init__(self):
        self.state = "IDLE"

    def handle_event(self, event):
        key = (self.state, event)
        if key not in FSM_TABLE:
            print("Invalid transition")
            return
        next_state, action = FSM_TABLE[key]
        ACTIONSORDER[action]()
        self.state = next_state
        print(f"State -> {self.state}")


# RED → GREEN → YELLOW → RED
# states
# events ->timer


class State:
    def on_event(self, context, event):
        raise NotImplementedError


class Red(State):
    def on_event(self, context, event):
        if event == "TIMER":
            context.state = Green()


class Green(State):
    def on_event(self, context, event):
        if event == "TIMER":
            context.state = Yellow()


class Yellow(State):
    def on_event(self, context, event):
        if event == "TIMER":
            context.state = Red()


class TrafficLight:
    def __init__(self):
        self.state = Red()

    def handle_event(self, event):
        self.state.on_event(self, event)
        print(f"Current State: {self.state.__class__.__name__}")


class PaymentFSM:
    def __init__(self):
        self.state = "VERIFYING"
        self.retry_count = 0
        self.MAX_RETRY = 3

    def handle_event(self, event):
        if self.state == "VERIFYING":
            if event == "payment_successful":
                self.state = "SUCCESS"
            elif event == "payment_failed":
                if self.retry_count < self.MAX_RETRY:
                    self.retry_count += 1
                    self.state = "RETRY"
                else:
                    self.state = "FAILED"
        elif self.state == "RETRY":
            if event == "retry":
                self.state = "VERIFYING"
        return self.state


class ShippingFSM:
    def __init__(self):
        self.state = "IN_TRANSIT"

    def handle_event(self, event):
        if self.state == "IN_TRANSIT":
            if event == "delivered":
                self.state = "Delivered"
        return self.state


class OrderHSM:
    def __init__(self):
        self.state = "CREATED"
        self.payment_fsm = None
        self.shipping_fsm = None

    def handle_event(self, event):
        if event == "cancel":
            self.state = "CANCELLED"
            return self.state
        
        if self.state=="CREATED":
            if event=="start_payment":
