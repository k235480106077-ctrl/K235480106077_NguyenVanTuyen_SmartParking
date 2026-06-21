from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ParkingSlot:
    slot_id: int
    slot_name: str
    is_occupied: bool = False


@dataclass
class ParkingTicket:
    ticket_id: Optional[int]
    plate_number: str
    slot_name: str
    check_in_time: str
    check_out_time: Optional[str] = None
    fee: float = 0.0
    status: str = "Đang gửi"


class ParkingFeeCalculator:
    """Tính phí gửi xe theo thời gian thực tế."""

    def __init__(self, first_hour_fee: int = 5000, next_hour_fee: int = 3000):
        self.first_hour_fee = first_hour_fee
        self.next_hour_fee = next_hour_fee

    def calculate_fee(self, check_in_time: str, check_out_time: str) -> int:
        fmt = "%Y-%m-%d %H:%M:%S"
        start = datetime.strptime(check_in_time, fmt)
        end = datetime.strptime(check_out_time, fmt)

        total_seconds = max((end - start).total_seconds(), 0)
        hours = int(total_seconds // 3600)
        if total_seconds % 3600 > 0:
            hours += 1

        if hours <= 0:
            hours = 1

        if hours == 1:
            return self.first_hour_fee

        return self.first_hour_fee + (hours - 1) * self.next_hour_fee
