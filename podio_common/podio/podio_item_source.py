from podio_common.utilities import SuperEnum


class PodioItemSource(SuperEnum):
    """Sources Explanation:
    SyncroComment: JSON dict returned by Syncro API
    PodioJSON: JSON dict returned by Podio API
    Values: instantiated by values
    """

    SyncroComment = "Syncro Comment"
    PodioJSON = "Podio JSON"
    Values = "Values"
