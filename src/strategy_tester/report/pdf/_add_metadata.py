from datetime import datetime

from matplotlib.backends.backend_pdf import PdfPages


def _add_metadata(pdf: PdfPages, pdf_title = "", author = "", subject = "", keyworkds = ""):
  pdf_dict = pdf.infodict()
  if pdf_title != "":
    pdf_dict["Title"] = pdf_title
  if author != "":
    pdf_dict["Author"] = author
  if subject != "":
    pdf_dict["Subject"] = subject
  if keyworkds != "":
    pdf_dict["Keywords"] = keyworkds
  pdf_dict["CreationDate"] = datetime.today()
  pdf_dict["ModificationDate"] = datetime.today()