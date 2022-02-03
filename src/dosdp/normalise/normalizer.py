import logging
from dosdp.normalise.element_order_normaliser import ElementOrderNormaliser
from dosdp.normalise.new_line_normaliser import NewLineNormaliser
from dosdp.normalise.util import read_yaml_file, write_yaml_to_file

logging.basicConfig(level=logging.INFO)


class CompositeNormaliser(object):

    normalisers = [ElementOrderNormaliser(), NewLineNormaliser()]
    # normalisers = [NewLineNormaliser()]

    def normalise(self, pattern):
        for normalizer in self.normalisers:
            pattern = normalizer.normalise(pattern)
        return pattern


def normalise(input_file, output_file):
    logging.info("Normalising %s" % input_file)
    pattern = read_yaml_file(input_file)
    pattern = CompositeNormaliser().normalise(pattern)
    write_yaml_to_file(pattern, output_file)



