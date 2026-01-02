# routes/item_csv_download.py

from flask import Response, stream_with_context, Blueprint
import csv
from io import StringIO
from sqlalchemy import or_, and_

from extensions import db
from model.item_csv_model import ItemData


item_csv_bp = Blueprint("item_csv", __name__)


@item_csv_bp.route("/items/incomplete/csv", methods=["GET"])
def download_incomplete_csv():

    def generate():
        try:
            query = (
                db.session.query(ItemData)
                .filter(
                    or_(
                        # name missing
                        ItemData.name.is_(None),
                        ItemData.name == "",

                        # all phones missing
                        and_(
                            or_(ItemData.phone_no_1.is_(None), ItemData.phone_no_1 == ""),
                            or_(ItemData.phone_no_2.is_(None), ItemData.phone_no_2 == ""),
                            or_(ItemData.phone_no_3.is_(None), ItemData.phone_no_3 == ""),
                            or_(ItemData.whatsapp_no.is_(None), ItemData.whatsapp_no == ""),
                            or_(ItemData.virtual_phone_no.is_(None), ItemData.virtual_phone_no == ""),
                        ),

                        # category missing
                        ItemData.category.is_(None),
                        ItemData.category == "",

                        # sub category missing
                        ItemData.sub_category.is_(None),
                        ItemData.sub_category == "",

                        # address / area missing
                        or_(
                            and_(ItemData.address.is_(None), ItemData.area.is_(None)),
                            and_(ItemData.address == "", ItemData.area == ""),
                        ),

                        # city missing
                        ItemData.city.is_(None),
                        ItemData.city == "",
                    )
                )
                .yield_per(100000)  # stream 1 lakh rows per batch
            )

            buffer = StringIO()
            writer = csv.writer(buffer)

            # Header row
            writer.writerow([c.name for c in ItemData.__table__.columns])
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)

            count = 0
            for row in query:
                writer.writerow(
                    [getattr(row, c.name) for c in ItemData.__table__.columns]
                )
                count += 1

                if count % 100000 == 0:
                    yield buffer.getvalue()
                    buffer.seek(0)
                    buffer.truncate(0)

            # Flush remaining rows
            if buffer.tell() > 0:
                yield buffer.getvalue()

        finally:
            # ensure session cleanup
            db.session.remove()

    headers = {
        "Content-Disposition": "attachment; filename=incomplete_items.csv"
    }

    return Response(
        stream_with_context(generate()),
        mimetype="text/csv",
        headers=headers,
    )
