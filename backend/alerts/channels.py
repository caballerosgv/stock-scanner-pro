from __future__ import annotations

import logging
from dataclasses import dataclass

from backend.scanner.types import ScanOutcome

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AlertMessage:
    symbol: str
    score: float
    text: str


class TelegramAlertSender:
    async def send(self, alert: AlertMessage) -> None:
        logger.info("telegram_alert", extra={"symbol": alert.symbol, "score": alert.score, "text": alert.text})


class EmailAlertSender:
    async def send(self, alert: AlertMessage) -> None:
        logger.info("email_alert", extra={"symbol": alert.symbol, "score": alert.score, "text": alert.text})


class WebNotificationSender:
    async def send(self, alert: AlertMessage) -> None:
        logger.info("web_alert", extra={"symbol": alert.symbol, "score": alert.score, "text": alert.text})


class AlertDispatcher:
    def __init__(self) -> None:
        self._telegram = TelegramAlertSender()
        self._email = EmailAlertSender()
        self._web = WebNotificationSender()

    async def dispatch_for(self, outcome: ScanOutcome) -> None:
        if outcome.score < 8:
            return
        message = AlertMessage(
            symbol=outcome.symbol,
            score=outcome.score,
            text=f"{outcome.symbol} score={outcome.score} signals={','.join(outcome.signals)}",
        )
        await self._telegram.send(message)
        await self._email.send(message)
        await self._web.send(message)
