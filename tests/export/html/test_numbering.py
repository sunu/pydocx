# coding: utf-8

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from pydocx.test import DocumentGeneratorTestCase
from pydocx.test.utils import WordprocessingDocumentFactory
from pydocx.openxml.packaging import (
    MainDocumentPart,
    NumberingDefinitionsPart,
    StyleDefinitionsPart,
)


class NumberingTestBase(object):
    simple_list_item = '''
        <p>
            <pPr>
                <numPr>
                    <ilvl val="{ilvl}" />
                    <numId val="{num_id}" />
                </numPr>
            </pPr>
            <r><t>{content}</t></r>
        </p>
    '''

    simple_list_definition = '''
        <num numId="{num_id}">
            <abstractNumId val="{num_id}"/>
        </num>
        <abstractNum abstractNumId="{num_id}">
            <lvl ilvl="0">
                <numFmt val="{num_format}"/>
            </lvl>
        </abstractNum>
    '''


class NumberingTestCase(NumberingTestBase, DocumentGeneratorTestCase):
    def test_lowerLetter_numbering_format_is_handled(self):
        num_id = 1
        numbering_xml = self.simple_list_definition.format(
            num_id=num_id,
            num_format='lowerLetter',
        )

        document_xml = self.simple_list_item.format(
            content='AAA',
            num_id=num_id,
            ilvl=0,
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_single_level_list_with_surrounding_paragraphs(self):
        num_id = 1
        numbering_xml = self.simple_list_definition.format(
            num_id=num_id,
            num_format='lowerLetter',
        )

        document_xml = '''
            <p><r><t>Foo</t></r></p>
            {aaa}
            {bbb}
            <p><r><t>Bar</t></r></p>
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=num_id,
                ilvl=0,
            ),
            bbb=self.simple_list_item.format(
                content='BBB',
                num_id=num_id,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <p>Foo</p>
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
                <li>BBB</li>
            </ol>
            <p>Bar</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_multi_level_list_with_surrounding_paragraphs(self):
        num_id = 1
        numbering_xml = '''
            <num numId="{num_id}">
                <abstractNumId val="{num_id}"/>
            </num>
            <abstractNum abstractNumId="{num_id}">
                <lvl ilvl="0">
                    <numFmt val="lowerLetter"/>
                </lvl>
                <lvl ilvl="1">
                    <numFmt val="decimal"/>
                </lvl>
                <lvl ilvl="2">
                    <numFmt val="upperLetter"/>
                </lvl>
            </abstractNum>
        '''.format(num_id=num_id)

        document_xml = '''
            <p><r><t>Foo</t></r></p>
            {aaa}
            {bbb}
            {ccc}
            <p><r><t>Bar</t></r></p>
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=num_id,
                ilvl=0,
            ),
            bbb=self.simple_list_item.format(
                content='BBB',
                num_id=num_id,
                ilvl=1,
            ),
            ccc=self.simple_list_item.format(
                content='CCC',
                num_id=num_id,
                ilvl=2,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <p>Foo</p>
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA
                    <ol class="pydocx-list-style-type-decimal">
                        <li>BBB
                            <ol class="pydocx-list-style-type-upperLetter">
                                <li>CCC</li>
                            </ol>
                        </li>
                    </ol>
                </li>
            </ol>
            <p>Bar</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_adjacent_lists(self):
        numbering_xml = '''
            {letter}
            {decimal}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
            decimal=self.simple_list_definition.format(
                num_id=2,
                num_format='decimal',
            ),
        )

        document_xml = '''
            <p><r><t>Foo</t></r></p>
            {aaa}
            {bbb}
            <p><r><t>Bar</t></r></p>
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            bbb=self.simple_list_item.format(
                content='BBB',
                num_id=2,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <p>Foo</p>
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
            </ol>
            <ol class="pydocx-list-style-type-decimal">
                <li>BBB</li>
            </ol>
            <p>Bar</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_basic_list_followed_by_list_that_is_heading_and_paragraph(self):
        numbering_xml = '''
            {letter}
            {decimal}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
            decimal=self.simple_list_definition.format(
                num_id=2,
                num_format='decimal',
            ),
        )

        style_xml = '''
            <style styleId="style1" type="paragraph">
              <name val="Heading 1"/>
            </style>
        '''

        list_item_with_parent_style_heading = '''
            <p>
                <pPr>
                    <pStyle val="style1" />
                    <numPr>
                        <ilvl val="{ilvl}" />
                        <numId val="{num_id}" />
                    </numPr>
                </pPr>
                <r><t>{content}</t></r>
            </p>
        '''

        document_xml = '''
            {aaa}
            {bbb}
            <p><r><t>Bar</t></r></p>
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            bbb=list_item_with_parent_style_heading.format(
                content='BBB',
                num_id=2,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(StyleDefinitionsPart, style_xml)
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
            </ol>
            <h1>BBB</h1>
            <p>Bar</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_separate_lists_with_paragraph_in_between_and_after(self):
        numbering_xml = '''
            {letter}
            {decimal}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
            decimal=self.simple_list_definition.format(
                num_id=2,
                num_format='decimal',
            ),
        )

        document_xml = '''
            <p><r><t>Foo</t></r></p>
            {aaa}
            <p><r><t>Bar</t></r></p>
            {bbb}
            <p><r><t>Baz</t></r></p>
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            bbb=self.simple_list_item.format(
                content='BBB',
                num_id=2,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <p>Foo</p>
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
            </ol>
            <p>Bar</p>
            <ol class="pydocx-list-style-type-decimal">
                <li>BBB</li>
            </ol>
            <p>Baz</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_single_list_followed_by_paragraph(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p><r><t>Foo</t></r></p>
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
            </ol>
            <p>Foo</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_single_list_with_bare_paragraph_between_items(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p><r><t>Foo</t></r></p>
            {bbb}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            bbb=self.simple_list_item.format(
                content='BBB',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA<br />Foo</li>
                <li>BBB</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_list_with_empty_numbering_xml(self):
        numbering_xml = ''

        document_xml = '''
            {aaa}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <p>AAA</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_single_paragraph_missing_level_definition(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            <p>
                <pPr>
                    <numPr>
                        <numId val="1" />
                    </numPr>
                </pPr>
                <r><t>foo</t></r>
            </p>
        '''

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <p>foo</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_multiple_paragraphs_with_one_missing_level_definition(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            <p><r><t>foo</t></r></p>
            <p>
                <pPr>
                    <numPr>
                        <numId val="1" />
                    </numPr>
                </pPr>
                <r><t>bar</t></r>
            </p>
        '''

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <p>foo</p>
            <p>bar</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_paragraph_with_valid_list_level_followed_by_missing_level(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p>
                <pPr>
                    <numPr>
                        <numId val="1" />
                    </numPr>
                </pPr>
                <r><t>foo</t></r>
            </p>
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
            </ol>
            <p>foo</p>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_missing_level_in_between_valid_levels(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p>
                <pPr>
                    <numPr>
                        <numId val="1" />
                    </numPr>
                </pPr>
                <r><t>foo</t></r>
            </p>
            {bbb}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            bbb=self.simple_list_item.format(
                content='BBB',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>
                    AAA
                    <br />
                    foo
                </li>
                <li>BBB</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_empty_paragraph_after_list_item(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p />
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_empty_paragraph_in_between_list_items(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p />
            {bbb}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            bbb=self.simple_list_item.format(
                content='BBB',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
                <li>BBB</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_paragraph_and_run_with_empty_text_in_between_list_items(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p>
                <r><t></t></r>
            </p>
            {bbb}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            bbb=self.simple_list_item.format(
                content='BBB',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
                <li>BBB</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_paragraph_with_empty_run_in_between_list_items(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p>
                <r></r>
            </p>
            {bbb}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            bbb=self.simple_list_item.format(
                content='BBB',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
                <li>BBB</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_paragraph_with_empty_run_followed_by_non_empty_paragraph(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p>
                <r></r>
            </p>
            <p>
                <r><t>BBB</t></r>
            </p>
            {ccc}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            ccc=self.simple_list_item.format(
                content='CCC',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA<br />BBB</li>
                <li>CCC</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_paragraph_with_multiple_empty_runs_followed_by_non_empty_paragraph(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p>
                <r></r>
            </p>
            <p>
                <r></r>
            </p>
            <p>
                <r></r>
            </p>
            <p>
                <r><t>BBB</t></r>
            </p>
            {ccc}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            ccc=self.simple_list_item.format(
                content='CCC',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA<br />BBB</li>
                <li>CCC</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_paragraph_empty_run_paragraph_empty_run_paragraph(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p>
                <r></r>
            </p>
            <p>
                <r><t>Foo</t></r>
            </p>
            <p>
                <r></r>
            </p>
            <p>
                <r><t>Bar</t></r>
            </p>
            {ccc}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            ccc=self.simple_list_item.format(
                content='CCC',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA<br />Foo<br />Bar</li>
                <li>CCC</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_paragraph_followed_by_paragraph_with_only_whitespace(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
            <p>
                <r><t> </t></r>
            </p>
            {ccc}
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
            ccc=self.simple_list_item.format(
                content='BBB',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li>AAA</li>
                <li>BBB</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_empty_item(self):
        numbering_xml = '''
            {letter}
        '''.format(
            letter=self.simple_list_definition.format(
                num_id=1,
                num_format='lowerLetter',
            ),
        )

        document_xml = '''
            {aaa}
        '''.format(
            aaa=self.simple_list_item.format(
                content='',
                num_id=1,
                ilvl=0,
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-lowerLetter">
                <li></li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)


class FakedNumberingTestCase(NumberingTestBase, DocumentGeneratorTestCase):
    def test_real_list_plus_fake_list(self):
        document_xml = '''
            {foo}
            <p><r><t>2. Bar</t></r></p>
            <p><r><t>3. Baz</t></r></p>
        '''.format(
            foo=self.simple_list_item.format(
                content='Foo',
                num_id=1,
                ilvl=0,
            ),
        )

        numbering_xml = '''
            {decimal}
        '''.format(
            decimal=self.simple_list_definition.format(
                num_id=1,
                num_format='decimal',
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-decimal">
                <li>Foo</li>
                <li>Bar</li>
                <li>Baz</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_real_list_plus_nested_fake_list_with_mixed_formats(self):
        document_xml = '''
            {aaa}
            <p><r><tab /><t>a. BBB</t></r></p>
            <p><r><tab /><t>b. CCC</t></r></p>
        '''.format(
            aaa=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
        )

        numbering_xml = '''
            {decimal}
        '''.format(
            decimal=self.simple_list_definition.format(
                num_id=1,
                num_format='decimal',
            ),
        )

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-decimal">
                <li>AAA
                    <ol class="pydocx-list-style-type-lowerLetter">
                        <li>BBB</li>
                        <li>CCC</li>
                    </ol>
                </li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)

    def test_initial_faked_list_plus_real_list(self):
        document_xml = '''
            <p><r><t>1. Foo</t></r></p>
            <p><r><t>2. Bar</t></r></p>
            {foo}
        '''.format(
            foo=self.simple_list_item.format(
                content='AAA',
                num_id=1,
                ilvl=0,
            ),
        )

        numbering_xml = '''
            <num numId="1">
                <abstractNumId val="1"/>
            </num>
            <abstractNum abstractNumId="1">
                <lvl ilvl="0">
                    <numFmt val="decimal"/>
                    <start val="3" />
                </lvl>
            </abstractNum>
        '''

        document = WordprocessingDocumentFactory()
        document.add(NumberingDefinitionsPart, numbering_xml)
        document.add(MainDocumentPart, document_xml)

        expected_html = '''
            <ol class="pydocx-list-style-type-decimal">
                <li>Foo</li>
                <li>Bar</li>
                <li>AAA</li>
            </ol>
        '''
        self.assert_document_generates_html(document, expected_html)


class FakedNestedNumberingBase(object):
    def setUp(self):
        super(FakedNestedNumberingBase, self).setUp()

        self.document_xml = '''
            <p><r><t>{0}AAA</t></r></p>
            <p><r><t>{1}BBB</t></r></p>
            <p><r>
                <tab />
                <t>{2}CCC</t>
            </r></p>
            <p><r>
                <tab />
                <t>{3}DDD</t>
            </r></p>
            <p><r>
                <tab />
                <tab />
                <t>{4}EEE</t>
            </r></p>
            <p><r>
                <tab />
                <tab />
                <t>{5}FFF</t>
            </r></p>
            <p><r>
                <tab />
                <t>{6}GGG</t>
            </r></p>
            <p><r><t>{7}HHH</t></r></p>
        '''

        self.expected_html = '''
            <ol class="pydocx-list-style-type-{0}">
                <li>AAA</li>
                <li>BBB
                    <ol class="pydocx-list-style-type-{1}">
                        <li>CCC</li>
                        <li>DDD
                            <ol class="pydocx-list-style-type-{2}">
                                <li>EEE</li>
                                <li>FFF</li>
                            </ol>
                        </li>
                        <li>GGG</li>
                    </ol>
                </li>
                <li>HHH</li>
            </ol>
        '''

    def assert_html_using_pattern(self, pattern):
        document_xml_format = [
            pattern.format(digit)
            for digit in self.document_xml_sequence
        ]
        document_xml = self.document_xml.format(*document_xml_format)
        expected_html = self.expected_html.format(*self.expected_html_format)
        self.assert_main_document_xml_generates_html(document_xml, expected_html)

    def test_format_digit_dot(self):
        self.assert_html_using_pattern('{0}. ')

    def test_format_digit(self):
        self.assert_html_using_pattern('{0} ')

    def test_digit_paren(self):
        self.assert_html_using_pattern('{0}) ')

    def test_parent_digit_paren(self):
        self.assert_html_using_pattern('({0}) ')


class FakedNestedDecimalTestCase(FakedNestedNumberingBase, DocumentGeneratorTestCase):
    expected_html_format = ['decimal', 'decimal', 'decimal']
    document_xml_sequence = [1, 2, 1, 2, 1, 2, 3, 3]


class FakedNestedLowerLetterTestCase(FakedNestedNumberingBase, DocumentGeneratorTestCase):
    expected_html_format = ['lowerLetter', 'lowerLetter', 'lowerLetter']
    document_xml_sequence = ['a', 'b', 'a', 'b', 'a', 'b', 'c', 'c']


class FakedNestedUpperLetterTestCase(FakedNestedNumberingBase, DocumentGeneratorTestCase):
    expected_html_format = ['upperLetter', 'upperLetter', 'upperLetter']
    document_xml_sequence = ['A', 'B', 'A', 'B', 'A', 'B', 'C', 'C']


class FakedNestedLowerRomanTestCase(FakedNestedNumberingBase, DocumentGeneratorTestCase):
    expected_html_format = ['lowerRoman', 'lowerRoman', 'lowerRoman']
    document_xml_sequence = ['i', 'ii', 'i', 'ii', 'i', 'ii', 'iii', 'iii']


class FakedNestedUpperRomanTestCase(FakedNestedNumberingBase, DocumentGeneratorTestCase):
    expected_html_format = ['upperRoman', 'upperRoman', 'upperRoman']
    document_xml_sequence = ['I', 'II', 'I', 'II', 'I', 'II', 'III', 'III']
