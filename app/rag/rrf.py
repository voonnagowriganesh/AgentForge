from collections import defaultdict


def reciprocal_rank_fusion(
    vector_docs,
    bm25_docs,
    k=60,
):

    scores = defaultdict(float)

    for rank, doc in enumerate(vector_docs):

        scores[doc] += 1 / (k + rank + 1)

    for rank, doc in enumerate(bm25_docs):

        scores[doc] += 1 / (k + rank + 1)

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    return ranked
