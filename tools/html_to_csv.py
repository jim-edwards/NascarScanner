from html.parser import HTMLParser
from pathlib import Path


class TRTDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tr = False
        self.in_td = False
        self.current_td = []
        self.current_row = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'tr':
            self.in_tr = True
            self.current_row = []
        elif tag.lower() == 'td' and self.in_tr:
            self.in_td = True
            self.current_td = []

    def handle_endtag(self, tag):
        if tag.lower() == 'td' and self.in_td:
            self.in_td = False
            text = ''.join(self.current_td).strip()
            # collapse multiple spaces/newlines
            text = ' '.join(text.split())
            self.current_row.append(text)
        elif tag.lower() == 'tr' and self.in_tr:
            self.in_tr = False
            if self.current_row:
                self.rows.append(self.current_row)

    def handle_data(self, data):
        if self.in_td:
            self.current_td.append(data)


def quote_if_needed(s):
    if ',' in s or '\n' in s:
        return '"' + s.replace('"', '""') + '"'
    return s


import argparse


def main():
    ap = argparse.ArgumentParser(description="Convert an HTML table to src CSV format")
    ap.add_argument("--html", "-i", required=True, help="Path to input HTML file")
    ap.add_argument("--csv", "-o", required=True, help="Path to output CSV file")
    args = ap.parse_args()

    html_path = Path(args.html)
    csv_path = Path(args.csv)
    html = html_path.read_text(encoding='utf-8')

    parser = TRTDParser()
    parser.feed(html)

    header = "Car,Driver,Primary,Tone,Secondary,Tone,Other,Tone"
    lines = [header]

    for cols in parser.rows:
        # normalize
        car = cols[0] if len(cols) > 0 else ""
        driver = cols[1] if len(cols) > 1 else ""
        primary = cols[2] if len(cols) > 2 else ""
        alt1 = cols[3] if len(cols) > 3 else ""
        alt2 = cols[4] if len(cols) > 4 else ""
        # replace '*' frequency markers with empty entries (keep '*' in car field)
        if primary == '*':
            primary = ''
        if alt1 == '*':
            alt1 = ''
        if alt2 == '*':
            alt2 = ''
        csv_cols = [car, driver, primary, "", alt1, "", alt2, ""]
        lines.append(','.join(quote_if_needed(c) for c in csv_cols))

    csv_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"Wrote {len(lines)-1} rows to {csv_path}")


if __name__ == '__main__':
    main()
