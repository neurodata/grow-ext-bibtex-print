from bibtex_print import bibtex_print

BIB_FILE_PATH = "test_data/pubs.bib"


def setup_function(function):
    function.bibtex_entries = bibtex_print.load_bibtex(BIB_FILE_PATH)


def test_print_title():
    good_titles = [
        "Deformably Registering and Annotating Whole CLARITY Brains to an Atlas via Masked LDDMM",
        '<a href="https://neurodata.io/talks/open.html">Global Brain Workshop 2016</a>',
        '<a href="http://arxiv.org/abs/1403.3724">VESICLE : Volumetric Evaluation of Synaptic Interfaces using Computer vision at Large Scale</a>',
        '<a href="https://neurodata.io/talks/src.html">Learning a Data-Driven Nosology:Progress, Challenges & Opportunities</a>',
    ]

    for i, entry in enumerate(test_print_title.bibtex_entries):
        output = bibtex_print.print_title(entry)

        print(output)

        assert output != ""
        assert output in good_titles


def test_print_address():
    good_address = [
        "Kavli Neuroscience Discovery Institute & Center for Imaging Science",
        "Kavli Neuroscience Discovery Institute & Center for Imaging Science @ JHU",
    ]

    for i, entry in enumerate(test_print_address.bibtex_entries):
        output = bibtex_print.print_address(entry)

        assert output != ""

        if output is not None:
            assert output in good_address
