# Before refactoring
@interactions.post("/<int:interaction>/<string:token>/callback", body_cls=InteractionRespond)
async def respond_to_interaction(data: InteractionRespond, interaction: Interaction = DepInteraction):
    d = data.data
    if interaction.status != 1:
        raise InteractionAlreadyAck
    if data.type == 4:
        if not d.content:
            raise CannotSendEmptyMessage
        await send_interaction_response(interaction, d.flags & 64, d.content)
    elif data.type == 5:
        flags = (d.flags & 64) if d is not None else 0
        await send_interaction_response(interaction, flags | 128, "")

    return "", 204

# After refactoring
@interactions.post("/<int:interaction>/<string:token>/callback", body_cls=InteractionRespond)
async def respond_to_interaction(data: InteractionRespond, interaction: Interaction = DepInteraction):
    T = InteractionCallbackType
    d = data.data
    if interaction.status != InteractionStatus.PENDING:
        raise InteractionAlreadyAck
    if data.type == T.CHANNEL_MESSAGE_WITH_SOURCE:
        if not d.content:
            raise CannotSendEmptyMessage
        flags = d.flags & MessageFlags.EPHEMERAL
        await send_interaction_response(interaction, flags, d.content)
    elif data.type == T.DEFFERED_CHANNEL_MESSAGE_WITH_SOURCE:
       	flags = d.flags & MessageFlags.EPHEMERAL if d is not None else 0
        flags |= MessageFlags.LOADING
        await send_interaction_response(interaction, flags, "")

    return "", 204
