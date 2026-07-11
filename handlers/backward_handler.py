import renderers
from config import states, buttons, message_templates
from core.context import RequestContext
from handlers import handlers_mapping


def backward_handler(ctx: RequestContext):
    previous_state = ctx.session.go_back()
    new_handler = handlers_mapping.get(previous_state)
    print(ctx.session.get_states())
    new_handler(ctx)
    # renderer = renderers.STATE_RENDERERS.get(previous_state)
    # renderer(ctx)