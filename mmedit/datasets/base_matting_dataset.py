from collections import defaultdict

from .base_dataset import BaseDataset
from .registry import DATASETS


@DATASETS.register_module
class BaseMattingDataset(BaseDataset):
    """Base image matting dataset.
    """

    def __init__(self, ann_file, pipeline, data_prefix=None, test_mode=False):
        super(BaseMattingDataset, self).__init__(pipeline, test_mode)
        self.ann_file = str(ann_file)
        self.data_prefix = str(data_prefix)
        self.data_infos = self.load_annotations()

    def evaluate(self, results, logger=None):
        """Evaluating with different metrics.

        Args:
            results (list[tuple]): The output of forward_test() of the model.

        Return:
            eval_results (dict): Evaluation results dict.
        """
        if not isinstance(results, list):
            raise TypeError('results must be a list, but got {}'.format(
                type(results)))
        assert len(results) == len(self), (
            'The length of results is not equal to the dataset len: {} != {}'.
            format(len(results), len(self)))

        results = [res[1] for res in results]  # a list of dict

        eval_results = defaultdict(list)  # a dict of list
        for res in results:
            for metric, val in res.items():
                eval_results[metric].append(val)
        for metric, val_list in eval_results.items():
            assert len(val_list) == len(self), (
                'Length of evaluation result of {} is {}, should be {}'.format(
                    metric, len(val_list), len(self)))

        # average the results
        eval_results = {
            metric: sum(values) / len(self)
            for metric, values in eval_results.items()
        }

        return eval_results
