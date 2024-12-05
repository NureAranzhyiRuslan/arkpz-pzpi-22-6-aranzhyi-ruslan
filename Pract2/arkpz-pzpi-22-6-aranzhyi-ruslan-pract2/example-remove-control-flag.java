// Before refactoring
private void realHandle() {
    boolean disconnected = false;
    while (!disconnected) {
        try {
            BasePacket packet = BasePacket.readPacket(reader);
            log("got packet: " + packet + " of type " + packet.getPacketType());
            if(packet instanceof SendMessagePacket messagePacket) {
                server.clientSentMessage(this, messagePacket.text);
            } else if(packet instanceof ShutdownRequestPacket shutdownPacket) {
                server.clientSentShutdown(this, shutdownPacket.password);
            }
        } catch (IOException e) {
            logger.warning("Failed to read packet: " + e);
        } catch (EOFException e) {
            logger.warning("Client " + login + " disconnected!");
            disconnected = true;
        }
    }
    server.clientDisconnected(this);
}

// After refactoring
private void realHandle() {
    while (true) {
        BasePacket packet;
        try {
            packet = BasePacket.readPacket(reader);
        } catch (IOException e) {
            logger.warning("Failed to read packet: " + e);
            continue;
        } catch (EOFException e) {
            logger.warning("Client " + login + " disconnected!");
            break;
        }

        log("got packet: " + packet + " of type " + packet.getPacketType());
        if(packet instanceof SendMessagePacket messagePacket) {
            server.clientSentMessage(this, messagePacket.text);
        } else if(packet instanceof ShutdownRequestPacket shutdownPacket) {
            server.clientSentShutdown(this, shutdownPacket.password);
        }
    }
    server.clientDisconnected(this);
}
