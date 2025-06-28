import json
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from lxml.etree import tostring

def export_report_xml(report_id):
    connection = UnixSocketConnection(path="/run/gvm/gvmd.sock")

    with Gmp(connection) as gmp:
        gmp.authenticate('admin', 'your-password')

        # ดึงรายการ format ทั้งหมด และหา ID ของ XML
        formats = gmp.get_report_formats()
        xml_format_id = None
        for report_format in formats:
            if report_format.name == "XML":
                xml_format_id = report_format.id
                break

        if not xml_format_id:
            raise Exception("XML format not found.")

        # ดึง report แบบ XML
        response = gmp.get_report(
            report_id=report_id,
            report_format_id=xml_format_id,
            details=True
        )

        xml_bytes = tostring(response.to_etree(), pretty_print=True)
        path = f'/home/unitvas/APP/report/{report_id}.xml'

        with open(path, 'wb') as f:
            f.write(xml_bytes)

        return json.dumps({
            "status": True,
            "id": f"{report_id}.xml"
        })

# ตัวอย่างเรียกใช้:
# print(export_report_xml("12345678-xxxx-xxxx-xxxx-xxxxxxxxxxxx"))
