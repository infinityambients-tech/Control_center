from __future__ import annotations

from pathlib import Path

from app.modules.invoices.models import Invoice


def generate_invoice_pdf(invoice: Invoice, output_dir: Path) -> Path:
    """
    Generates a simple invoice PDF using reportlab (if installed).
    Raises ImportError if reportlab is missing.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / f"{invoice.invoice_number.replace('/', '_')}.pdf"

    c = canvas.Canvas(str(out), pagesize=A4)
    width, height = A4

    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Invoice {invoice.invoice_number}")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Issue date: {invoice.issue_date.isoformat()}")
    y -= 18
    if invoice.due_date:
        c.drawString(50, y, f"Due date: {invoice.due_date.isoformat()}")
        y -= 18

    c.drawString(50, y, f"Currency: {invoice.currency}")
    y -= 18

    c.drawString(50, y, f"Net: {invoice.net_amount}")
    y -= 18
    c.drawString(50, y, f"VAT {invoice.vat_rate}%: {invoice.vat_amount}")
    y -= 18
    c.drawString(50, y, f"Gross: {invoice.gross_amount}")
    y -= 24

    if invoice.notes:
        c.drawString(50, y, f"Notes: {invoice.notes}")

    c.showPage()
    c.save()
    return out

