from collections import defaultdict

import PyPDF2
import csv


def write_pdf(data, name):
    with open(name, "w+") as f:
        writer = csv.writer(f)
        cols = ['number'] + list(data.keys())
        writer.writerow(cols)

        number_payments = defaultdict(dict)
        for k, v in data.items():
            for num, nv in v.items():
                number_payments[num][k] = nv

        for number, nums in number_payments.items():
            r = [number]
            for m in data.keys():
                r.append(round(nums.get(m, 0), 2))
            writer.writerow(r)


if __name__ == "__main__":
    doc = PyPDF2.PdfReader("apple.pdf")

    payments = defaultdict(lambda: defaultdict(int))
    received = defaultdict(lambda: defaultdict(int))
    number = ''
    kind = ''
    month = ''

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    with open("out.csv", "w+") as f:
        for row in doc.pages:
            text = row.extract_text()

            print_text_line = False
            for line in text.splitlines():

                if "Transactions" in line:
                    month = line.strip().split(" ", 1)[1]

                if "Payment to" in line:
                    number = line.split('+')[-1]
                    kind = 'payment'
                    print_text_line = True
                elif "Received from" in line:
                    number = line.split('+')[-1]
                    kind = 'received'
                    print_text_line = True
                elif print_text_line:
                    print_text_line = False
                    value = line.split("$")[1]
                    value = float(value)

                    if kind == 'payment':
                        payments[month][number] += value
                    else:
                        received[month][number] += value

    write_pdf(payments, "payments.csv")
    write_pdf(received, "received.csv")
