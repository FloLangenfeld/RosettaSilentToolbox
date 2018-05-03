# -*- coding: utf-8 -*-
"""
.. codeauthor:: Jaume Bonet <jaume.bonet@gmail.com>

.. affiliation::
    Laboratory of Protein Design and Immunoengineering <lpdi.epfl.ch>
    Bruno Correia <bruno.correia@epfl.ch>

.. func:: get_id
.. func:: get_available_sequences
.. func:: get_sequence
.. func:: get_available_structures
.. func:: get_structure
.. func:: get_available_structure_predictions
.. func:: get_structure_prediction
.. func:: get_sequential_data
.. func:: get_available_labels
.. func:: get_label
"""
# Standard Libraries

# External Libraries
import pandas as pd
import numpy as np

# This Library


__all__ = ['get_id', 'get_available_sequences', 'get_sequence',
           'get_available_structures', 'get_structure',
           'get_available_structure_predictions', 'get_structure_prediction',
           'get_sequential_data', 'get_available_labels', 'get_label']


def _check_type( obj ):
    if not isinstance(obj, (pd.DataFrame, pd.Series)):
        raise TypeError("Data container has to be a DataFrame/Series or a derived class.")


def _check_column( obj, ctype, seqID ):
    if "{0}_{1}".format(ctype, seqID) not in obj:
        raise KeyError(
            "{0} for {1} not found in data set. ".format(ctype.capitalize(), seqID) +
            "Column `{0}_{1}` is missing.".format(ctype, seqID))
    return "{0}_{1}".format(ctype, seqID)


def _get_available( obj, ctype ):
    if isinstance(obj, pd.DataFrame):
        return ["_".join(x.split("_")[1:]) for x in obj.columns.values if x.startswith(ctype)]
    else:
        return ["_".join(x.split("_")[1:]) for x in obj.index.values if x.startswith(ctype)]


def _get_key_sequence( obj, ctype, seqID, key_residues ):
    from rstoolbox.components import get_selection
    from .reference import _get_reference

    seq = obj[_check_column(obj, ctype, seqID)]
    sft = _get_reference(obj, "sft", seqID)

    if isinstance(obj, pd.Series):
        length = len(seq)
    else:
        length = len(seq.iloc[0])
    kr = get_selection(key_residues, seqID, sft, length)

    if isinstance(obj, pd.Series):
        # -1 because we access string positions
        return "".join(np.array(list(seq))[kr - 1])
    else:
        return seq.apply(lambda seq: "".join(np.array(list(seq))[kr - 1]))


def get_id( self ):
    """Return identifier data for the design(s).

    :return: :class:`str` or :class:`~pandas.Series` - depending on the input

    :raises:
        :TypeError: |indf_error|
        :KeyError: If the column ``description`` cannot be found.

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import parse_rosetta_file
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = parse_rosetta_file("../rstoolbox/tests/data/input_2seq.minisilent.gz")
           ...: df.get_id()
    """
    _check_type(self)
    if "description" not in self:
        raise KeyError("Identifiers not found in data set. Column `description` is missing.")
    return self["description"]


def get_available_sequences( self ):
    """List which **sequence** identifiers are available in the data container

    :return: :func:`list` of :class:`str`

    :raises:
        :TypeError: |indf_error|.

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import parse_rosetta_file
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = parse_rosetta_file("../rstoolbox/tests/data/input_2seq.minisilent.gz",
           ...:                         {'sequence': 'AB'})
           ...: df.get_available_sequences()
    """
    _check_type(self)
    return _get_available(self, "sequence_")


def get_sequence( self, seqID, key_residues=None ):
    """Return the **sequence** data for ``seqID`` available in the container.

    :param str seqID: |seqID_param|.
    :param key_residues: |keyres_param|.
    :type key_residues: |keyres_types|

    :return: :class:`str` or :class:`~pandas.Series` - depending on the input

    :raises:
        :TypeError: |indf_error|.
        :KeyError: |seqID_error|.

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import parse_rosetta_file
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = parse_rosetta_file("../rstoolbox/tests/data/input_2seq.minisilent.gz",
           ...:                         {'sequence': 'AB'})
           ...: df.get_sequence('B')
    """
    _check_type(self)
    if key_residues is None:
        return self[_check_column(self, "sequence", seqID)]
    else:
        return _get_key_sequence(self, "sequence", seqID, key_residues)


def get_available_structures( self ):
    """
    List which **structure** identifiers are available in the data container

    :return: :func:`list` of :class:`str`

    :raises:
        :TypeError: |indf_error|.

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import parse_rosetta_file
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = parse_rosetta_file("../rstoolbox/tests/data/input_ssebig.minisilent.gz",
           ...:                         {'structure': 'C'})
           ...: df.get_available_structures()
    """
    _check_type(self)
    return _get_available(self, "structure_")


def get_structure( self, seqID, key_residues=None ):
    """Return the **structure** data for ``seqID`` available in the container.

    :param str seqID: |seqID_param|.
    :param key_residues: |keyres_param|.
    :type key_residues: |keyres_types|

    :return: :class:`str` or :class:`~pandas.Series` - depending on the input

    :raises:
        :TypeError: |indf_error|.
        :KeyError: If the column ``structure_<seqID>`` cannot be found.

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import parse_rosetta_file
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = parse_rosetta_file("../rstoolbox/tests/data/input_ssebig.minisilent.gz",
           ...:                         {'structure': 'C'})
           ...: df.get_structure('C').iloc[:5]
    """
    _check_type(self)
    if key_residues is None:
        return self[_check_column(self, "structure", seqID)]
    else:
        return _get_key_sequence(self, "structure", seqID, key_residues)


def get_available_structure_predictions( self ):
    """ List which **structure prediction** identifiers are available in the data container.

    :return: :func:`list` of :class:`str`

    :raises:
        :TypeError: |indf_error|.
    """
    _check_type(self)
    return _get_available(self, "psipred_")


def get_structure_prediction( self, seqID, key_residues=None ):
    """
    Return the structure prediction(s) data.

    :param str seqID: |seqID_param|.
    :param key_residues: |keyres_param|.
    :type key_residues: |keyres_types|

    :return: :class:`str` or :class:`~pandas.Series` - depending on the input

    :raises:
        :TypeError: |indf_error|.
        :KeyError: If the column ``psipred_<seqID>`` cannot be found.
    """
    _check_type(self)
    if key_residues is None:
        return self[_check_column(self, "psipred", seqID)]
    else:
        return _get_key_sequence(self, "psipred", seqID, key_residues)


def get_sequential_data( self, query, seqID ):
    """Provides data on the requested query.

    Basically, this allows :class:`str` access to the other getters.

    :param str query: Query type: ``sequence``, ``structure``, ``structure_prediction``.
    :param str seqID: |seqID_param|.

    :return: :class:`str` or :class:`~pandas.Series` - depending on the input

    :raises:
        :TypeError: |indf_error|.
        :KeyError: If ``query`` has a non-accepted value.

    .. seealso::
        :meth:`.DesignFrame.get_sequence`
        :meth:`.DesignFrame.get_structure`
        :meth:`.DesignFrame.get_structure_prediction`
        :meth:`.DesignSeries.get_sequence`
        :meth:`.DesignSeries.get_structure`
        :meth:`.DesignSeries.get_structure_prediction`

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import parse_rosetta_file
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = parse_rosetta_file("../rstoolbox/tests/data/input_ssebig.minisilent.gz",
           ...:                         {'sequence': 'C', 'structure': 'C'})
           ...: df.get_sequential_data('sequence', 'C').iloc[:5]
           ...: df.get_sequential_data('structure', 'C').iloc[:5]
    """
    queries = ["sequence", "structure", "structure_prediction"]
    if query.lower() not in queries:
        raise KeyError("Available queries are: {}".format(",".join(queries)))

    if query.lower() == "sequence":
        return self.get_sequence(seqID)
    if query.lower() == "structure":
        return self.get_structure(seqID)
    if query.lower() == "structure_prediction":
        return self.get_structure_prediction(seqID)


def get_available_labels( self ):
    """
    List which slabels are available in the data container.

    :return: :func:`list` of :class:`str`

    :raises:
        :TypeError: |indf_error|.

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import parse_rosetta_file
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = parse_rosetta_file("../rstoolbox/tests/data/input_2seq.minisilent.gz",
           ...:                         {'labels': ['MOTIF', 'CONTACT', 'CONTEXT'],
           ...:                          'sequence': 'A'})
           ...: df.get_available_labels()
    """
    _check_type(self)
    return _get_available(self, "lbl_")


def get_label( self, label, seqID=None ):
    """Return the content(s) of the **labels** of interest as a :class:`.Selection`
    for a given sequece.

    If only one ``seqID`` is available, it will automatically pick labels for that,
    even if other data is present; otherwise, ``seqID`` must be provided. This takes
    into account availability of sequence, structure and psipred data.

    :param str label: Label identifier. Will be uppercased.
    :param str seqID: |seqID_param|.

    :return: :class:`.Selection`

    :raises:
        :TypeError: |indf_error|.
        :KeyError: If ``seqID`` is not specified and more than one ``seqID`` is possible.
        :KeyError: If the column ``lbl_<label>`` cannot be found.

    .. rubric:: Example

    .. ipython::

        In [1]: from rstoolbox.io import parse_rosetta_file
           ...: import pandas as pd
           ...: pd.set_option('display.width', 1000)
           ...: df = parse_rosetta_file("../rstoolbox/tests/data/input_2seq.minisilent.gz",
           ...:                         {'labels': ['MOTIF', 'CONTACT', 'CONTEXT'],
           ...:                          'sequence': 'A'})
           ...: df.get_label('CONTACT', 'A')
           ...: df.get_label('CONTACT', 'B')
    """
    _check_type(self)
    if seqID is None:
        ss = set(get_available_sequences(self))
        sr = set(get_available_structures(self))
        sp = set(get_available_structure_predictions(self))
        sa = ss.union(sr).union(sp)
        if len(sa) > 1:
            raise KeyError("Information for multiple seqID is present. Choose one.")
        else:
            seqID = sa.pop()
    data = self[_check_column(self, "lbl", label.upper())]
    if isinstance(self, pd.DataFrame):
        return data.apply(lambda x: x[seqID])
    else:
        return data[seqID]
