import json
import datetime
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transformers import EtreeCheckCommandTransform
from lxml.etree import tostring
from gvm.errors import GvmError

# === CONFIG ===
GVM_USERNAME = "admin"   # แก้ตาม config จริง
GVM_PASSWORD = "admin"   # แก้ตาม config จริง
GVM_SOCKET_PATH = "/run/gvm/gvmd.sock"  # default path
EXPORT_DIR = "/home/unitvas/APP/report/"  # เปลี่ยนได้ตามต้องการ

def export_report_by_id(report_id):
    try:
        connection = UnixSocketConnection(path=GVM_SOCKET_PATH)
        transform = EtreeCheckCommandTransform()

        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username=GVM_USERNAME, password=GVM_PASSWORD)

            # ค้นหา report format ที่เป็น XML
            formats = gmp.get_report_formats()
            xml_format_id = None
            for fmt in formats.xpath("report_format"):
                if fmt.findtext("name") == "XML":
                    xml_format_id = fmt.get("id")
                    break

            if not xml_format_id:
                raise Exception("ไม่พบ XML report format")

            # ดึงรายงานด้วย format XML และ details ครบ
            response = gmp.get_report(
                report_id=report_id,
                report_format_id=xml_format_id,
                details=True
            )

            output_path = f"{EXPORT_DIR}{report_id}.xml"
            with open(output_path, "wb") as f:
                f.write(tostring(response, pretty_print=True))

            print(f"[✓] Exported report: {output_path}")
            return {
                "status": True,
                "path": output_path,
                "report_id": report_id
            }

    except GvmError as e:
        print("[✗] GVM Error:", str(e))
    except Exception as ex:
        print("[✗] General Error:", str(ex))

    return {
        "status": False,
        "message": "Failed to export report"
    }

# === Example Usage ===
if __name__ == "__main__":
    # เปลี่ยนเป็น report_id จริงที่ต้องการดึง
    report_id = "1119c300-0cfd-402e-a5f7-443a66665db4"
    result = export_report_by_id(report_id)
    print(json.dumps(result, indent=2))
