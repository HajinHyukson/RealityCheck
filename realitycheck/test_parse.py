"""PDF extraction checks; only the hosted OCR boundary is mocked."""
import unittest
from unittest.mock import patch

import pymupdf

import parse


class PdfTests(unittest.TestCase):
    def test_mixed_pdf_keeps_native_text_and_ocr_page_citations(self):
        with pymupdf.open() as scan:
            scan.new_page().insert_text((36, 72), 'Scanned covenant evidence.')
            image = scan[0].get_pixmap().tobytes('png')
        with pymupdf.open() as pdf:
            pdf.new_page().insert_text((36, 72), 'Embedded agreement terms.')
            page = pdf.new_page()
            page.insert_image(page.rect, stream=image)
            page.insert_text((36, 800), 'Page footer')
            content = pdf.tobytes()
        with patch.object(parse, 'parse_image', return_value=[
                {'class': 'Text', 'text': 'Scanned covenant evidence.'}]):
            parsed = parse.parse_upload('mixed.pdf', content)
        self.assertEqual(parsed['pages'], 2)
        self.assertIn('Embedded agreement terms.', parsed['text']['Document, para 1 (p1)'])
        self.assertEqual(parsed['text']['Document, para 2 (p2)'], 'Scanned covenant evidence.')

    def test_pdf_limits_reject_before_hosted_ocr(self):
        for pages, message in ((301, '300 pages'), (21, '20 pages.*OCR')):
            with self.subTest(pages=pages), pymupdf.open() as pdf:
                for _ in range(pages):
                    pdf.new_page()
                with patch.object(parse, 'parse_image', side_effect=AssertionError('Limit must be checked before OCR')):
                    with self.assertRaisesRegex(ValueError, message):
                        parse.parse_upload('oversized.pdf', pdf.tobytes())

    def test_searchable_scans_use_existing_text_layer(self):
        with pymupdf.open() as scan:
            scan.new_page().insert_text((36, 72), 'Annual filing scan')
            image = scan[0].get_pixmap().tobytes('png')
        with pymupdf.open() as pdf:
            for number in range(1, 22):
                page = pdf.new_page()
                page.insert_image(page.rect, stream=image)
                page.insert_textbox(page.rect + (36, 36, -36, -36),
                                    f'Searchable scan page {number}.\n' + 'Annual subscription revenue.\n' * 10,
                                    render_mode=3)
            with patch.object(parse, 'parse_image', side_effect=AssertionError('Existing text layer must be used')):
                parsed = parse.parse_upload('searchable.pdf', pdf.tobytes())
        self.assertEqual(parsed['pages'], 21)
        self.assertIn('Searchable scan page 21.', parsed['text']['Document, para 21 (p21)'])


if __name__ == '__main__':
    unittest.main()
