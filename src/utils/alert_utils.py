def format_alert_message(alert_type: str, src_ip: str) -> str:
    """
    Memformat pesan notifikasi serangan.
    """
    return (
        f"⚠️ Peringatan Keamanan: Serangan terdeteksi!\n"
        f"Jenis Serangan: {alert_type}\n"
        f"Sumber: {src_ip}\n"
        f"Harap segera lakukan tindakan."
    )
