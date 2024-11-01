# src/utils/alert_utils.py

def format_alert_message(alert_type, src_ip):
    """
    Memformat pesan notifikasi serangan.

    Parameters:
        alert_type (str): Jenis serangan yang terdeteksi.
        src_ip (str): Alamat IP sumber serangan.

    Returns:
        str: Pesan yang diformat untuk notifikasi.
    """
    return f"⚠️ Peringatan Keamanan: Serangan terdeteksi!\nJenis Serangan: {alert_type}\nSumber: {src_ip}\nHarap segera lakukan tindakan."
