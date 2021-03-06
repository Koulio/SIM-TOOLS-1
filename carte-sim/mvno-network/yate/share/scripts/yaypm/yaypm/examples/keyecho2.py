chdir /tmp
screen -t BTS 0 /etc/osmocom/respawn.sh /usr/bin/l1fwd-proxy
detach
                                                                                                                                                                                                                                                                                                                                                                                                                                                 ate.msg("call.answered",
                 {"id": targetid,
                  "targetid": callid}).enqueue()

        logger.debug("Call %s answered." % callid)

        while True:
            dtmf = yield yate.onmsg("chan.dtmf",
                                    lambda m : m["id"] == callid,
                                    end)

            logger.debug("Dtmf %s received." % dtmf["text"])

            yate.msg("chan.masquerade",
                {"message" : "chan.attach",
                 "id": targetid,
                 "source": "wave/play/./sounds/digits/pl/%s.gsm" % \
                 dtmf["text"]}).enqueue()

            dtmf.ret(True)

    except AbandonedException, e:
        logger.debug("Call %s abandoned." % callid)

@defer.inlineCallbacks
def route(yate):
    while True:
        route = yield yate.onmsg("call.route", lambda m : m["called"] == "ivr")
        ivr(yate, route["id"])
        route.ret(True, "dumb/")

if __name__ in ["__main__", "__embedded_yaypm_module__"]:
    logger.setLevel(logging.DEBUG)
    yaypm.utils.setup(lambda yate: route(yate))

